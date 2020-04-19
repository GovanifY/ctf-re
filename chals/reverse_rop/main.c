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
  strcat(test,"FLAG_PART_1");
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
    strcat(test,"FLAG_PART_4");
  }
  if (arg_check1 == 0xAABBCCD3) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD4) {
    strcat(test,"FLAG_WRONG");
  }
  if (arg_check1 == 0xAABBCCD5) {
    strcat(test,"FLAG_PART_5");
  }

}


void flag6(unsigned int arg_check2, unsigned int arg_check3) {
  if (arg_check2 == 0xBBCCDDE7) {
    if(arg_check3==0xBBCCDDE1){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE2){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE3){
        strcat(test,"FLAG_WRONG");
    }
  }
  if (arg_check2 == 0xBBCCDDE8) {
    if(arg_check3==0xBBCCDDE1){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE2){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE3){
        strcat(test,"FLAG_WRONG");
    }
  }
  if (arg_check2 == 0xBBCCDDE9) {
    if(arg_check3==0xBBCCDDE1){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE2){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE3){
        strcat(test,"FLAG_PART_6");
    }
  }
  if (arg_check2 == 0xBBCCDDEA) {
    if(arg_check3==0xBBCCDDE1){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE2){
        strcat(test,"FLAG_WRONG");
    }
     if(arg_check3==0xBBCCDDE3){
        strcat(test,"FLAG_WRONG");
    }
  }




}

void xor(){
    int i;
    for (i = 0; i < 80; i++) {
        if(test[i] == 0x00){
            return;
        }
       test[i] = (unsigned int)test[i] ^ (i%256);
    }
}

void xor2(){
    int i;
    for (i = 0; i < 80; i++) {
        if(test[i] == 0x00){
            return;
        }
       test[i] = (unsigned int)test[i] ^ (i%256);
    }
}

void xor3(){
    int i;
    for (i = 0; i < 80; i++) {
        if(test[i] == 0x00){
            return;
        }
       test[i] = (unsigned int)test[i] ^ (i%256);
    }
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
  vuln();
}
