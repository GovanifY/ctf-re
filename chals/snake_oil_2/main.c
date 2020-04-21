#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>


#define FLAG_ENCRYPTED "FLAG_ENC_C"

#define RANDOM_VAL RANDOM_C

//--JUNK CODE--

//--JUNK CODE--

void snake_oil_crypto(char **argv) {
    char flag_encrypted[68] = FLAG_ENCRYPTED;

    const char* pos = argv[1];
    unsigned char val[4];

     /* WARNING: no sanitization or error-checking whatsoever */
    for (size_t count = 0; count < sizeof val/sizeof *val; count++) {
        sscanf(pos, "%2hhx", &val[count]);
        pos += 2;
    }

    for(int i=0; i<sizeof flag_encrypted/sizeof *flag_encrypted; i+=4){
        flag_encrypted[i]=(char)((unsigned int)flag_encrypted[i]^(val[0]^(unsigned char)RANDOM_VAL));
//--JUNK CODE--

//--JUNK CODE--
        flag_encrypted[i+1]=(char)((unsigned int)flag_encrypted[i+1]^(val[1]^(unsigned char)RANDOM_VAL));
//--JUNK CODE--

//--JUNK CODE--
        flag_encrypted[i+2]=(char)((unsigned int)flag_encrypted[i+2]^(val[2]^(unsigned char)RANDOM_VAL));
//--JUNK CODE--

//--JUNK CODE--
        flag_encrypted[i+3]=(char)((unsigned int)flag_encrypted[i+3]^(val[3]^(unsigned char)RANDOM_VAL));
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



