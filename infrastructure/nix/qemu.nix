{ pkgs, lib, ... }:
with lib;
let mkVM = { local-ip, macAddress, hostname, networkId ? "nixos", memorySize ? "4G", diskSpace ? 10*1024, tapInterface ? "tap0" }:
{                           
  imports = [
    <nixpkgs/nixos/modules/profiles/qemu-guest.nix>
  ];                    
                                 
  config = {                                                      
    fileSystems."/" = {                                           
      device = "/dev/disk/by-label/nixos";
      fsType = "ext4";
      autoResize = true;                                          
    };

    services.openssh.enable = true;
    networking.firewall.enable = false;
    networking.firewall.allowPing = true;
    environment.systemPackages = with pkgs; [
      wget vim
    ];

    networking.hostName = hostname;
    networking.nameservers = ["1.1.1.1" "8.8.8.8"];
    networking.interfaces.eth0.useDHCP = false;
    networking.interfaces.eth0.ipv4.addresses = [
      { address = local-ip; prefixLength = 24; }
    ];
    networking.defaultGateway = "10.0.2.1";

    virtualisation.qemu.networkingOptions = ["-netdev tap,id=${networkId},ifname=${tapInterface},script=no,downscript=no" "-device virtio-net-pci,netdev=${networkId},mac=${macAddress}"];
    virtualisation.memorySize = memorySize;
    virtualisation.diskSize = diskSpace;
    virtualisation.writableStoreUseTmpfs = false;
    virtualisation.qemu.options = ["-display sdl"];

    boot.growPartition = true;
    boot.kernelParams = [ "console=ttyS0" ];                      
    boot.loader.grub.device = "/dev/vda";
    boot.loader.timeout = 0;
    boot.extraModulePackages = [ pkgs.linuxPackages.wireguard ];

    users.extraUsers.root.password = "";
    users.extraUsers.root.openssh.authorizedKeys.keys = [
      ''ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcEkYM1r8QVNM/G5CxJInEdoBCWjEHHDdHlzDYNSUIdHHsn04QY+XI67AdMCm8w30GZnLUIj5RiJEWXREUApby0GrfxGGcy8otforygfgtmuUKAUEHdU2MMwrQI7RtTZ8oQ0USRGuqvmegxz3l5caVU7qGvBllJ4NUHXrkZSja2/51vq80RF4MKkDGiz7xUTixI2UcBwQBCA/kQedKV9G28EH+1XfvePqmMivZjl+7VyHsgUVj9eRGA1XWFw59UPZG8a7VkxO/Eb3K9NF297HUAcFMcbY6cPFi9AaBgu3VC4eetDnoN/+xT1owiHi7BReQhGAy/6cdf7C/my5ehZwD raito@RaitoBezarius-Laptop-OverDrive''
    ];
  };
};
in
  mkVM {
    local-ip = "10.0.2.2";
    hostname = "qemu-ctf";
    macAddress = "DE:AD:BE:EF:12:25";
    tapInterface = "tap1";
    memorySize = "2G";
  }
