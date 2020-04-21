#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>

#define VERIF_STRING "VERIF_C"

#define FLAG_ENCRYPTED "FLAG_ENC_C"

//--JUNK CODE--

//--JUNK CODE--

void snake_oil_crypto(char **argv) {
    char verif_string[68] = VERIF_STRING;
    char flag_encrypted[68] = FLAG_ENCRYPTED;

    const char* pos = argv[1];
    unsigned char val[4];

     /* WARNING: no sanitization or error-checking whatsoever */
    for (size_t count = 0; count < sizeof val/sizeof *val; count++) {
        sscanf(pos, "%2hhx", &val[count]);
        pos += 2;
    }

    for(int i=0; i<sizeof verif_string/sizeof *verif_string; i+=4){
        verif_string[i]=(char)((unsigned int)verif_string[i]^val[0]);
        verif_string[i+1]=(char)((unsigned int)verif_string[i+1]^val[1]);
//--JUNK CODE--

//--JUNK CODE--
        verif_string[i+2]=(char)((unsigned int)verif_string[i+2]^val[2]);
        verif_string[i+3]=(char)((unsigned int)verif_string[i+3]^val[3]);

        if(!(verif_string[i] == 0x00 && verif_string[i+1] == 0x00 &&
                verif_string[i+2] == 0x00 && verif_string[i+3] == 0x00)) {
//--JUNK CODE--

//--JUNK CODE--
            printf("Raté!\n");
            return;
        }
        flag_encrypted[i]=(char)((unsigned int)flag_encrypted[i]^val[0]);
        flag_encrypted[i+1]=(char)((unsigned int)flag_encrypted[i+1]^val[1]);
//--JUNK CODE--

//--JUNK CODE--
        flag_encrypted[i+2]=(char)((unsigned int)flag_encrypted[i+2]^val[2]);
        flag_encrypted[i+3]=(char)((unsigned int)flag_encrypted[i+3]^val[3]);
    }
    printf("Gagné! Voici le flag:\n");
//--JUNK CODE--

//--JUNK CODE--
    printf(flag_encrypted);
}

int main(int argc, char **argv){
  setvbuf(stdout, NULL, _IONBF, 0);

  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  snake_oil_crypto(argv);
}



