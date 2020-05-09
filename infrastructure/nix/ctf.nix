{ pkgs, configPath }:
with builtins;
with pkgs.lib;
/*

Activation script will just unzip.

*/

/**

Catalog:

— Web server challenge: systemd unit to run the webserver with a flag.txt under read only flag.
— Binary challenge: flag.txt under readonly flag permission, the binary is under SUID flag permission.
— Reverse challenge: the binary is under user's own permission.

**/

let
  readJSON = p: fromJSON (readFile p);
  mkChallenge = tags: c: {
    inherit (c) name;
    value = {
      inherit (c) name;
      type = tags.${toString c.id};
      id = toString c.id;
      idInteger = c.id;
    };
  };
  mkChallengeTag = t: {
    name = (toString t.challenge_id);
    value = t.value;
  };
  flagUserFor = teamName: challengeId: "flags-${teamName}-${challengeId}";
  readChallengeDesc = tags: cfgPath: listToAttrs (map (mkChallenge tags) (readJSON (cfgPath.challenges)).results);
  readChallengeTags = cfgPath: listToAttrs (map mkChallengeTag (readJSON (cfgPath.tags)).results);
  challengesTags = readChallengeTags configPath;
  challenges = readChallengeDesc challengesTags configPath;
  challengesWithFlags = filterAttrs (n: v: v.type == "exploit" || v.type == "webserver") challenges;
  teamConfiguration = (readJSON configPath.teams).results;
  binaries = import ./binaries.nix {
    inherit pkgs;
    challengesBinarySources = ../chals_out;
    binaryConfiguration = (crossLists (team: challenge: {
      teamName = team.name;
      challengeMeta = challenge;
    }) [ teamConfiguration (attrValues challenges) ]);
  };
  mkFlagKey = { name, flagPath, teamName, chalId }: {
    inherit name;
    value = {
      text = builtins.readFile flagPath;
      user = flagUserFor teamName chalId;
      permissions = "0600";
    };
  };
  mkFlags = 
  teamConfiguration: challenges: listToAttrs (
    map mkFlagKey (crossLists (team: chal: {
      name = "${team.name}-${chal.id}";
      flagPath = configPath.generatedChallenges + ("/" + chal.name + "/" + team.name + "/flag.txt");
      teamName = team.name;
      chalId = chal.id;
    }) [ teamConfiguration (attrValues challenges) ])
  );
  mkTeamUser = name: sshKeyPubFile: challengeNumber: {
    name = "${name}-${challengeNumber}";
    value = {
      isNormalUser = true;
      openssh.authorizedKeys.keyFiles = [
        (./. + "/${sshKeyPubFile}")
        ./govanify.pub
        ./raito.pub
      ];
      packages = [ binaries."${name}-${challengeNumber}" ];
    };
  };
  mkFlagUser = teamName: { id, ... }: {
    name = flagUserFor teamName id;
    value = {
      createHome = false;
      isSystemUser = false;
      useDefaultShell = true;
      group = "users";
      extraGroups = ["keys" "ctf"];
    };
  };
  mkTeamUsers = { id, name, email, sshPubKeyPath, ... }: 
  let
    mkUser = mkTeamUser name sshPubKeyPath;
  in
  map (challenge: mkUser (toString challenge.id)) (attrValues challenges)
  ++
  map (mkFlagUser name) (attrValues challenges);

  setupFlagForUser = chals: { id, name, ... }: map (setupFlagPerChallengeForUser name) chals;
  setupBinaryForUser = chals: { id, name, ... }: map (setupBinaryPerChallengeForUser name) chals;
  setupFlagPerChallengeForUser = teamName: { id, ... }: "symlink_user_flag ${teamName} ${id}";
  setupBinaryPerChallengeForUser = teamName: { id, name, ... }:
  let
    binaryPath = binaries."${teamName}-${id}";
    unpatchedBinaryPath = binaries."${teamName}-${id}-unpatched";
    chalName = name;
    flagUser = flagUserFor teamName id;
  in
  "symlink_user_challenge ${teamName} ${id} ${chalName} ${binaryPath} ${unpatchedBinaryPath} ${flagUser}";
  amountOfChallenges = length (attrValues challenges);
  buildTeamUsers = config: listToAttrs (concatMap mkTeamUsers teamConfiguration);
  mkIndication = { teamId, teamName }: { id, idInteger, ... }: ''
    if [ -f /home/${teamName}-${id}/.bashrc ]; then
      rm -f /home/${teamName}-${id}/.bashrc
    fi

    cat <<EOF > /home/${teamName}-${id}/.profile
    echo "Bienvenue sur le serveur CTF des gens qui vont vous faire souffrir."
    echo "Attention, ce n'est pas votre *average* système UNIX. Ne prenez pas tout pour acquis!"

    echo "Vous remarquerez que vous devez exploiter ce qu'il y a dans challenge/, ce qu'il y a dans unpatched/"
    echo "Ce n'est rien de plus que la version exploitable sur vos machines \"standards\", c'est exactement le même code."

    export PORT=${toString (1300 + teamId*amountOfChallenges + idInteger)}
    EOF
  '';
  mkIndications = chals: {id, name, ... }: map (mkIndication { teamId = id; teamName = name; }) chals;
in
{
  system.activationScripts = {
    # Place binaries with SUID flag and flags.
    setupBinariesAndFlags = 
    let
      binariesSymlinks = flatten (map (setupBinaryForUser (attrValues challenges)) teamConfiguration);
      profilesInjections = flatten (map (mkIndications (attrValues challenges)) teamConfiguration);
    in
    stringAfter ["users" "groups" "wrappers"] ''
        ${builtins.readFile ./setup-binaries.sh}
        ${concatStringsSep "\n" profilesInjections}
        ${concatStringsSep "\n" binariesSymlinks}
        chmod 701 /home
        chmod -w /home/*-12/
        chmod +w /home/*-12/.bash_history
        '';
  };

  environment.systemPackages = with pkgs; [
    file
    python3
    gdb
  ];

  # Set up webservers.
  # systemd.user.services = mkWebserversChallenges teamConfiguration;
  users.users = buildTeamUsers teamConfiguration;
  users.groups.ctf = {};
  deployment.keys = mkFlags teamConfiguration challengesWithFlags;
}
