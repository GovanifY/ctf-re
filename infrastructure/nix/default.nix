{ pkgs ? import <nixpkgs>, lib ? pkgs.lib }:
with builtins;
let
  readJSON = p: fromJSON (readFile p);
  readChallengeDesc = cfgPath: listToAttrs (map (c: {
    inherit (c) name;
    value = {
      inherit (c) name;
      type = c.category;
      id = toString c.id;
    };
  })) ((readJSON cfgPath).results);
  readTeamConfiguration = cfgPath: (readJSON cfgPath.teamConfig).results;
  cfgPath = {
    challenges = ../db/challenges_nix.json;
    teams = ../db/teams.json;
  };
  challenges = readChallengeDesc cfgPath.challenges;
in
{
  binaries = import ./binaries.nix { inherit pkgs;
    challengesBinarySources = ../chals_out;
    config = (crossLists (team: challenge: {
      teamName = team.name;
      challengeMeta = challenge;
    }) [ (readTeamConfiguration cfgPath.teams) (attrValues challenges) ]);
  };
}
