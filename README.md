CTF Anti cheat
==========
This is a deterministic anti-cheat/unique binaries generator specially tailored
to CTFs. It creates a regex per challenge to load into your flag platform. 
The flag itself is a sha2 of the challenge name plus a secret on top of 4 bytes
at a different position for each challenge identifying uniquely the team in a
sneaky fashion.   
The setup also includes ways to add junk code to binaries and have more
convoluted setup done to them through a python script.  
All the flags and binaries are deterministic, so as long as you don't re-roll
your secrets you will get the same result each time.  
The cheat detection part detects those bytes to see who cheated with who,
probabilistically or definitely, or simply who cheated if the identifying bytes
cannot be found. The whole idea is to have hashes that looks the most alike
possible while still being fairly certain about the origin of said flag.

## Setup:
Put your challengess in  the folder called "chals". One folder per challenge, each folder must contain
a setup.py setting up the challenge final folder and removing unecessary files.  
You will end up with a folder tree such as:
```
chals_out/
├── access_security
│   ├── regex.txt
│   ├── test_team
│   │   ├── access_security
│   │   └── flag.txt
│   └── test_team2
│       ├── access_security
│       └── flag.txt
```
You can thus automate deployment of the binaries onto your VMs however you like.  
This setup works well with binaries that won't be executed remotely too and whatnot.


## RE CTF Edition:
challenges list: 
- reverse_rop
- simple_rop
- simple_rop_2
- web_server
- snake_oil 
- snake_oil_2
- access_security
- web_server_2
- modern_rop
