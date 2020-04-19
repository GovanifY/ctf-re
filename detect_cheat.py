import os
import json
import pathlib
import hashlib
import errno
import shutil
import subprocess

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))


ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def small_hash(name):
    checksum=0
    for byte in name:
        # get last bit of checksum
        b=checksum & 0b11111111
        # addition on 8bits
        b+=ord(byte)
        b&= 0b11111111
        #clear last bits of checksum
        checksum = checksum & 0b11111111111111111111111100000000
        # checksum last 8 bits = b
        checksum = checksum | b
        # rol checksum
        checksum=rol(checksum, 3, 32)

    return checksum.to_bytes(4, byteorder='big')

team_count=0
teams={}
team_names=[]
submissions=[]
chals=[]
chals_data={}
flags=[]
uni_bytes=[]
for i in next(os.walk('chals'))[1]:
    chals.append(i)

with open("teams.json", "r") as read_file:
    data = json.load(read_file)
    team_count=data['count']
    for i in range(0, team_count):
        teams[data['results'][i]['id']] = data['results'][i]['name']
        team_names.append(data['results'][i]['name'])

with open("challenges.json", "r") as read_file:
    data = json.load(read_file)
    chal_count=data['count']
    for i in range(0, chal_count):
        chals_data[data['results'][i]['id']] = data['results'][i]['name']


with open("submissions.json", "r") as read_file:
    data = json.load(read_file)
    sub_count=data['count']
    for i in range(0, sub_count):
        submissions.append([data['results'][i]['provided'],
            data['results'][i]['team_id'], data['results'][i]['challenge_id'],
            data['results'][i]['type']])


# flag creation is a bit complex: in theory we do a sha2 for each challenge
# name, but also calculate through a custom hash team name + chal name that we
# add inside this flag at random bytes for each chal
for i in chals:
    regex_done=False

    # we calculate the location of the identifying bytes
    salt_chal=small_hash(i)
    salts=[]
    for z in range(0, 4):
        salts.append(salt_chal[z]%32)
        if(salts[z]==0):
            salts[z]+=2
        elif(z==32):
            salts[z]-=2

    for y in team_names:
        uni_hash=small_hash(i+y)
        # make it a bit harder to guess the format of the sha2
        chal_name=i+"1378528"
        hash_final=bytearray(bytes.fromhex(hashlib.sha256(chal_name.encode()).hexdigest()))
        # we replace by the identifying bytes
        hash_final[salts[0]]=uni_hash[0]
        hash_final[salts[1]]=uni_hash[1]
        hash_final[salts[2]]=uni_hash[2]
        hash_final[salts[3]]=uni_hash[3]
        hash_final_str=hash_final.hex()
        uni_bytes.append([salts[0], uni_hash[0], salts[1], uni_hash[1],
            salts[2], uni_hash[2], salts[3], uni_hash[3], y, i]) 
        flag = "GY{" + hash_final_str + "}"
        flags.append([y, flag])


for i in submissions:
    found_flag=False
    done_flag=False
    # if flag is directly copied
    for y in flags:
        if(i[0]==y[1]):
            found_flag=True
            if(y[0]!=teams[i[1]]):
                print(teams[i[1]] + " has cheated with " + y[0] + " on challenge "
                + chals_data[i[2]] + " with 100% probability!")
                done_flag=True

    if(done_flag):
        continue

    # if we only found the identifying bytes used at some point
    i_hash=i[0].replace("GY{", "")
    i_hash=i_hash.replace("}", "")
    i_hash=bytes.fromhex(i_hash)
    for y in uni_bytes:
        if(i_hash[y[0]] == y[1] and i_hash[y[2]] == y[3] and i_hash[y[4]] ==
                y[5] and i_hash[y[6]] == y[7] and teams[i[1]]!=y[8]):
            print("identifying bytes from team " + y[8] + " in challenge " +
                    y[9] + " used by " +
                    teams[i[1]] + " on challenge " + chals_data[i[2]] + 
                    "; this has a 0.0000000002% (1/256**4) chance of happening"
                    + " approximately, a manual verification is needed")
    if(done_flag):
        continue

    # otherwise if the flag validated but we have no clue who they stole from
    if(i[3]=="correct" and found_flag==False):
        print(teams[i[1]] + " has somehow removed indentifying bytes on challenge "
                + chals_data[i[2]] + " and validated it, they most likely" +
                " cheated but are somewhat smart!")

