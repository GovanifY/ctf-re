{
  services.openssh.enable = true;
  networking.firewall.allowedTCPPorts = [ 22 ];
  users = {
    mutableUsers = false;
    users.root.openssh.authorizedKeys.keyFiles = [
      ./raito.pub
      ./govanify.pub
    ];
  };

  security.hideProcessInformation = false;
}
