#!/usr/bin/env python3
import smtplib
import json
import pathlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from subprocess import check_output

DEBUG = False
LINK = "https://ctf.govanify.com"

def attach_textfile(outer, path, filename):
    with open(path, 'r') as fp:
        msg = MIMEText(fp.read())
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        outer.attach(msg)

def password():
    return check_output("[XXX]", shell=True).splitlines()[0].decode('utf8')

def build_email(team):
    subject = '[ESGI] Examen final — Ten Desires Drive'

    emails = [u['email'] for u in team['users']]
    msg = MIMEMultipart()
    msg['From'] = '[XXX]'
    msg['To'] = ', '.join(emails) if not DEBUG else '[XXX]'
    msg['Subject'] = subject

    names = ', '.join([u['name'] for u in team['users']])

    body = f'''
    Messieurs, Mesdames, {names},

    Si vous recevez cet email, c'est que dans les prochaines heures, vous serez au bout de votre vie.
    En effet, votre mission [1], si vous l'acceptez, c'est de prendre les clefs SSH ED25519 ci-jointes.

    Et de vous connecter à {LINK} afin de recevoir vos futures instructions.

    Polissez vos arts du ROP et de l'exploitation obscure, cela vous sera utile apparamment.

    Ayant hâte de voir vos messages afflués,

    [1]: Un peu cliché, mais fait l'affaire.
    --
    Ryan Lahfa
    Gauvain Roussel-Tarbouriech
    '''
    msg.attach(MIMEText(body, 'plain'))
    keysPath = pathlib.Path('./keys') / team['name']
    pubKeyPath = keysPath / "id_ed25519.pub"
    privKeyPath = keysPath / "id_ed25519"
    attach_textfile(msg,
            pubKeyPath,
            'id_ed25519.pub')
    attach_textfile(msg,
            privKeyPath,
            'id_ed25519')


    return msg, (emails if not DEBUG else ['[XXX]'])

def bulk_send(emails):
    server = smtplib.SMTP('[XXX]', 587)
    server.starttls()
    server.login('[XXX]', password())
    for email, to in emails:
        server.sendmail('[XXX]',
                to,
                email.as_string())
        if DEBUG:
            break
    server.quit()

def main():
    with open('./db/teams.json', 'r') as f:
        teams = json.load(f)['results']
    with open('./db/users.json', 'r') as f:
        users = json.load(f)['results']

    for team in teams:
        team['users'] = []
        for user in users:
            if user['team_id'] == team['id']:
                team['users'].append(user)
    emails = [None] * len(teams)
    for i, team in enumerate(teams):
        emails[i] = build_email(team)

    bulk_send(emails)

if __name__ == '__main__':
    main()
