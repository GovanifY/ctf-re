let
  scaleway-machine = { host, port ? 22, name }: {pkgs, lib, ...}@args:
  {
    imports = [
      ./baseline.nix
      ./scaleway.nix
    ];

    deployment.targetHost = host;
    deployment.targetPort = port;

    networking.hostName = name;
  };
  qemu-machine = { host, gwIP, port ? 22, name }: { pkgs, lib, ... }@args:
  {
    imports = [
      ./baseline.nix
    ];

    deployment.targetHost = host;
    deployment.targetPort = port;
    networking.hostName = name;
    deployment.hasFastConnection = true; # indeed, it's local.
    fileSystems."/" = {
      device = "/dev/disk/by-label/nixos";
      fsType = "ext4";
    };

    boot.loader.grub.device = "nodev"; # qemu boot directly the stuff.

    networking.interfaces.eth0.useDHCP = false;
    networking.interfaces.eth0.ipv4.addresses = [
      {
        address = host;
        prefixLength = 24;
      }
    ];
    networking.defaultGateway = gwIP;
    networking.nameservers = [ "1.1.1.1" "8.8.8.8" ];
    networking.publicIPv4 = host;

    boot.initrd.availableKernelModules = [ "virtio_net" "virtio_pci" "virtio_mmio" "virtio_blk" "virtio_scsi" "9p" "9pnet_virtio" ];
    boot.initrd.kernelModules = [ "virtio_balloon" "virtio_console" "virtio_rng" ];

    boot.initrd.postDeviceCommands =
    ''
      # Set the system time from the hardware clock to work around a
      # bug in qemu-kvm > 1.5.2 (where the VM clock is initialised
      # to the *boot time* of the host).
      hwclock -s
    '';

    security.rngd.enable = false;

  };
in
  {
    ctf-machine = scaleway-machine {
      host = "212.47.244.250";
      name = "ragnarok";
    };
  }
