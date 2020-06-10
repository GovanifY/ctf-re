#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>

#define BUFSIZE 16


//--JUNK CODE--

//--JUNK CODE--

void execute_me() {

//--JUNK CODE--

//--JUNK CODE--

    system("cat flag.txt");
//--JUNK CODE--

//--JUNK CODE--

}

void vuln() {
  char buf[16];
  printf("Vous savez quoi faire :) : ");
  return gets(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
//--JUNK CODE--

//--JUNK CODE--
  vuln();
}
