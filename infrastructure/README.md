# Comment déployer

- S'assurer que dans ce repertoire il y a un `chals_out` (généré par le système)
- S'assurer qu'il y a `db/` (`RE_XXXX.zip`, vient de CTFd)
- Faire tourner `mk-ssh-keys` pour générer les clefs et patcher le `teams.json`
- Attention aux bugs d'Unicode sur les `challenges.json`, il faut filtrer la description.
- Créer un déploiement NixOps: `nixops create ./logical.nix ./physical.nix -s state_file.nixops`
- Lancer le déploiement NixOps: `nixops deploy -s state_file.nixops`
