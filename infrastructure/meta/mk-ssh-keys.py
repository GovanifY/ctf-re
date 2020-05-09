#!/usr/bin/env python3
#
import os
import click
from plumbum import local
import json
import pathlib

SUPPORTED_KEY_TYPES = ["ed25519", "ecdsa", "rsa"]


def write_ssh_key(username: str, out_path: str, key_type: str, debug: bool):
    if key_type == "ed25519":
        command = f"-t ed25519 -N lol -f {out_path} -C {username}@ctf"
    elif key_type == "ecdsa":
        command = f"-t ecdsa -b 521 -N lol -f {out_path} -C {username}@ctf"
    elif key_type == "rsa":
        command = f"-t rsa -b 4096 -N lol -f {out_path} -C {username}@ctf"
    else:
        click.echo(f"Unsupported key type: {key_type}")
        raise click.Abort()

    if debug:
        click.echo("ssh-keygen " + command)

    ssh_keygen = local["ssh-keygen"]
    ssh_keygen(command.split())

    with open(f"{out_path}.pub") as pubkey:
        return pubkey.read()

@click.command()
@click.option('--teams', prompt="Teams JSON path")
@click.option('--out', prompt="Out directory well-structured")
@click.option('--key-type', default="ed25519", type=click.Choice(SUPPORTED_KEY_TYPES))
@click.option('--debug', is_flag=True, default=False)
def cli(teams: str, out: str, key_type: str, debug: bool):
    """
    Generate new SSH keypair for a remote service (and copy to clipboard).
    """
    username = os.path.expanduser("~").split("/").pop()
    ssh_key_path = os.path.expanduser(out)

    if os.path.exists(ssh_key_path):
        click.echo(f"{ssh_key_path} exists!")
        raise click.Abort()

    with open(teams, "r") as teams_file:
        teams_structure = json.load(teams_file)

    for i, team in enumerate(teams_structure['results']):
        name = team['name']
        path = os.path.join(ssh_key_path, team['name'])
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        write_ssh_key(name, os.path.join(path, f'id_{key_type}'), key_type, debug)
        click.echo(f"Public key for {name} saved.")
        teams_structure['results'][i]['sshPubKeyPath'] = os.path.join(path, f'id_{key_type}.pub')

    with open(teams, "w") as teams_file:
        json.dump(teams_structure, teams_file)

cli()
