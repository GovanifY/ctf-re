#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>

#define BUFSIZE 16

bool win1 = false;
bool win2 = false;


//--JUNK CODE--

//--JUNK CODE--

void win_function1() {

//--JUNK CODE--

//--JUNK CODE--

  win1 = true;
}

void win_function2(unsigned int arg_check1) {

//--JUNK CODE--

//--JUNK CODE--

  if (win1 && arg_check1 != 0xAABBCCDD) {
    win2 = true;
  }
}

void flag(unsigned int arg_check4) {
  char flag[80];
  FILE *file;
  file = fopen("flag.txt", "r");

  fgets(flag, sizeof(flag), file);
  if (win1 && win2 && arg_check4 == 0xABADBABE) {
    printf("%s", flag);
    return;
  }
}

void vuln() {
  char buf[16];
  printf("Enter your input> ");
  return gets(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
}
