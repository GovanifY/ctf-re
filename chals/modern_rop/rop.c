#include <stdio.h>
int main(int argc, const char **argv)
{
  char s[8];
 
  printf("Enter name : ");
  fgets(s, 16, stdin);
  puts("Hello");
  printf(s, 16);
  printf("Enter sentence : ");
  fgets(s, 256, stdin);
  return 0;
}
