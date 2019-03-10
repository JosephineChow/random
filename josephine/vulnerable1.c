#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#define BUFFER_SIZE 512
#define FMT "String '%s' has size: %d"

void build_info(char *s, size_t sz)
{
    char *fmt = FMT;
    char dbg_str[strlen(FMT) - 1];
    /* The following allows a buffer overflow */
    sprintf(dbg_str, fmt, s, sz);
}

int main(int argc, char *argv[], char *envp[])
{
    /* Get Input */
    char input[BUFFER_SIZE] = {0};
    FILE *bf = fopen("badfile", "r");
    fread(input, sizeof(char), BUFFER_SIZE, bf);
    input[strcspn(input, "\n")] = '\0'; /* Strip newline */
    build_info(input, strlen(input));
    puts("Returned Properly: attack failed");
    return EXIT_FAILURE;
}

