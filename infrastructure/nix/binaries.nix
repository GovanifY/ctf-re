{ pkgs, lib ? pkgs.lib, challengesBinarySources, binaryConfiguration }:
let
  architecturesForBinaries = {
    modern_rop = 64;
    reverse_rop = 32;
    simple_rop = 32;
    simple_rop_2 = 64;
    snake_oil = 64;
    snake_oil_2 = 64;
    web_server = 64;
    web_server_2 = 32;
    access_security = 64;
    intro_reverse = 32;
    intro_rop = 32;
  };
  mkBinarySourcePath = teamName: challengeMeta: challengesBinarySources + "/${challengeMeta.name}/${teamName}";
  genericInstallPhase = ''
    cp -r $src $out
  '';
  architectures = archi: 
  let
    stdenv = if archi == 32 then pkgs.pkgsi686Linux.stdenv else pkgs.stdenv;
    autoPatchelfHook = if archi == 32 then pkgs.pkgsi686Linux.autoPatchelfHook else pkgs.autoPatchelfHook;
  in
  {
    mkReverseBinary = {patched, binaryIdentifier}: src: stdenv.mkDerivation {
      name = if patched then "reverse-challenge-${binaryIdentifier}" else "reverse-challenge-${binaryIdentifier}-unpatched";
      unpackPhase = "true";
      nativeBuildInputs = if patched then [ autoPatchelfHook ] else [];
      inherit src;
      installPhase = ''
        cp -r $src $out
      '';
    };
    mkExploitBinary = {patched, binaryIdentifier }: src: stdenv.mkDerivation {
      name = if patched then "exploit-challenge-${binaryIdentifier}" else "exploit-challenge-${binaryIdentifier}-unpatched";
      nativeBuildInputs = if patched then [ autoPatchelfHook ] else [];
      unpackPhase = "true";
      inherit src;
      installPhase = ''
        ${genericInstallPhase}
      '';
    };
    mkWebserverBinary = { patched, binaryIdentifier }: src: stdenv.mkDerivation {
      name = if patched then "webserver-challenge-${binaryIdentifier}" else "webserver-challenge-${binaryIdentifier}-unpatched";
      nativeBuildInputs = if patched then [ autoPatchelfHook ] else [];
      unpackPhase = "true";
      inherit src;
      installPhase = ''
        ${genericInstallPhase}
      '';
    };
  };
  mkBinary = patched: { teamName, challengeMeta }: 
  with (architectures architecturesForBinaries.${challengeMeta.name});
  let
    name = if patched then "${teamName}-${challengeMeta.id}" else "${teamName}-${challengeMeta.id}-unpatched";
    filteredSource = builtins.filterSource (p: t: t == "regular" -> (builtins.baseNameOf p) != "flag.txt") (mkBinarySourcePath teamName challengeMeta);
  in
  {
    inherit name;
    value = (
      if challengeMeta.type == "reverse" then mkReverseBinary { binaryIdentifier = name; inherit patched; } filteredSource
      else if challengeMeta.type == "exploit" then mkExploitBinary { binaryIdentifier = name; inherit patched; } filteredSource
      else if challengeMeta.type == "webserver" then mkWebserverBinary { binaryIdentifier = name; inherit patched; } filteredSource
      else throw "Undefined type of challenge: ${challengeMeta.type}!"
    );
  };
in
  builtins.listToAttrs ((map (mkBinary true) binaryConfiguration) ++ map (mkBinary false) binaryConfiguration)
