#include <unistd.h>
#include <sys/types.h>

int main(int argc, char *argv[]) {
    setreuid(geteuid(), geteuid());
    setregid(getegid(), getegid());
    return system("python3 web_server.py");
}

