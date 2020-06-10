#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>

#define BUFSIZE 16

char *test[80];

//--JUNK CODE--

//--JUNK CODE--

void flag1() {
//--JUNK CODE--

//--JUNK CODE--
  strcat(test,"FLAG_PART_1");
//--JUNK CODE--

//--JUNK CODE--

}

void flag2(unsigned int arg_check1) {
  if (arg_check1 == 0xAABBCCD1) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD2) {
    strcat(test,"FLAG_PART_2");
  }
  if (arg_check1 == 0xAABBCCD3) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD4) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD5) {
    strcat(test,"FLAG_WRONG");
  }

}

void flag3(unsigned int arg_check1) {
  if (arg_check1 == 0xAABBCCD1) {
    strcat(test,"FLAG_PART_3");
  }
  if (arg_check1 == 0xAABBCCD2) {
//--JUNK CODE--

//--JUNK CODE--
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD3) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD4) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD5) {
    strcat(test,"FLAG_WRONG");
  }

}

void xor(){
    memset(test,0,strlen(test));
}

void xor2(){
    memset(test,0,strlen(test));
}

void xor3(){
    memset(test,0,strlen(test));
}

void vuln() {
    flag1();
    xor();
    flag2(0xAABBCCD2);
    xor2();
    xor3();
    flag3(0xAABBCCD1);
    xor();
}

int main(int argc, char **argv){
  setvbuf(stdout, NULL, _IONBF, 0);

  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
}



