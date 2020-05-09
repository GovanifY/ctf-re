#!/usr/bin/env bash
nix-build '<nixpkgs/nixos>' -A vm -I nixos-config=./qemu.nix
