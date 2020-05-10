#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>

//--JUNK CODE--

//--JUNK CODE--

int main(int argc, const char **argv)
{
  char s[16];
 
  printf("Qui êtes vous? ");
  fgets(s, 32, stdin);
  long buffer[80];
  for(int i=0; i<80; i++){
      buffer[i]=0x4141414141414141;
      if(i==37){
//--JUNK CODE--

//--JUNK CODE--
          long p_tgr = (long)&printf;
//--JUNK CODE--

//--JUNK CODE--

          buffer[i]=p_tgr;
//--JUNK CODE--

//--JUNK CODE--
      }
  }
  printf("Vous êtes donc: ");
  printf(s, 32);
  printf(" !\nQuel est votre mot du jour? ");
//--JUNK CODE--

//--JUNK CODE--
  fgets(s, 256, stdin);
  printf("\nAh, quel dommage :/");
  return 0;
}
