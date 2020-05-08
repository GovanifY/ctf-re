#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>
#include <stdint.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>

//--JUNK CODE--

//--JUNK CODE--
int main(int argc, char **argv)
{
  char *file;
  char *host;

  file = argv[1];
  host = argv[2];

  if(access(argv[1], R_OK) == 0) {
      int fd;
      int ffd;
      int rc;
      struct sockaddr_in sin;
      char buffer[4096];

      printf("Connection à %s... ", host); fflush(stdout);

      fd = socket(AF_INET, SOCK_STREAM, 0);

      memset(&sin, 0, sizeof(struct sockaddr_in));
      sin.sin_family = AF_INET;
//--JUNK CODE--

//--JUNK CODE--
      sin.sin_addr.s_addr = inet_addr(host);
      sin.sin_port = htons((unsigned int)strtoul(getenv("PORT"), NULL, 0));

      if(connect(fd, (void *)&sin, sizeof(struct sockaddr_in)) == -1) {
          printf("Impossible de se connecter\n");
          exit(EXIT_FAILURE);
      }

#define HITHERE "SCP PROTOCOL REIMPLEMENTATION\n---TOP SECRET---\n"
//--JUNK CODE--

//--JUNK CODE--
      if(write(fd, HITHERE, strlen(HITHERE)) == -1) {
          exit(EXIT_FAILURE);
      }
#undef HITHERE

      printf("Connecté!\nOn envoie le fichier...\n"); fflush(stdout);

      ffd = open(file, O_RDONLY);
      if(ffd == -1) {
          exit(EXIT_FAILURE);
      }
//--JUNK CODE--

//--JUNK CODE--
      rc = read(ffd, buffer, sizeof(buffer));
      if(rc == -1) {
          exit(EXIT_FAILURE);
      }

      write(fd, buffer, rc);

  } else {
      printf("PIRATAGE DETECTE\n");
  }
}

