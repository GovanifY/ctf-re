let
  configPath = {
    challenges = ../db/challenges_nix.json;
    tags = ../db/tags.json;
    teams = ../db/teams.json;
    generatedChallenges = ../chals_out;
  };
in
  {
    network = {
      description = "CTF Machine network description";
      enableRollback = true;
    };

    defaults = {
      imports = [];
    };

    ctf-machine = { pkgs, lib, ... }:
    (import ./ctf.nix {
      inherit pkgs;
      inherit configPath;
    });
  }
