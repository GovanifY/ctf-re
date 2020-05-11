#include <unistd.h>
#include <sys/types.h>
#include <linux/limits.h>
#include <libgen.h>

int main(int argc, char *argv[]) {
    setreuid(geteuid(), geteuid());
    setregid(getegid(), getegid());
    // ensure CWD is the current folder path to avoid using the SUID bit on
    // another script
    char buf[PATH_MAX];
    readlink("/proc/self/exe", buf, PATH_MAX);
    chdir(dirname(buf));
    return system("python3 web_server.py");
}

