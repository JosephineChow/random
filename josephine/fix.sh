#!/bin/bash
#
# ATTENTION:
# ----------
# IGNORE THIS FILE.
# DO NOT MODIFY THIS FILE.
#


# This is a modified version of:
# https://github.com/hellman/fixenv
export PWD=`pwd`
IFS=" "
unsetenv=(`echo -n 'env -u SSH_CLIENT -u SSH_TTY -u USER -u MAIL -u SSH_CONNECTION -u LOGNAME -u HOME -u LANG -u _ -u TERM COLUMNS=157 LINES=32'`)
envlist=()
fname=""

# -----------------------------------------------------
# put envorder.c source 
# -----------------------------------------------------
function put_envorder_source {
cat > .envorder.c <<EOF
#include <stdio.h>
#include <string.h>
extern char ** environ;
int main(int argc, char *argv[]) {
    int i,j;
    FILE * fd = fopen(".gdblist", "w");
    for (i = 0; environ[i] != NULL; i++) {
        unsigned char *q, *p;
        p = strchr(environ[i],(int)'=');
        q = environ[i];
        while (q != p)
            fprintf(fd, "\\\\x%02x", *q++);
        q++;
        fprintf(fd, "=");
        while (*q)
            fprintf(fd, "\\\\x%02x", *q++);
        fprintf(fd, "\\\\x0a\n");
    }
    fclose(fd);
    return 0;
}
EOF
}

# -----------------------------------------------------
# gets env-vars, ordered as env-vars in gdb
#   resulting array is in envlist (global)
# -----------------------------------------------------
function getenvs {
    if [ ! -f ".envorder.c" ]; then
        put_envorder_source
        rm -f .envorder
    fi
    if [ ! -f ".envorder" ]; then
        gcc .envorder.c -o .envorder
    fi
    IFS=""
    "${unsetenv[@]}" gdb "`pwd`/.envorder" >/dev/null 2>&1 <<EOF
r
q
EOF
    IFS=$'\x0a'
    envs=$(cat .gdblist)
    envlist=()
    for env in $envs; do
        IFS=""
        envlist=("${envlist[@]}" "`printf "$env"`")
    done
}


# -----------------------------------------------------
# runs arguments in gdb
# -----------------------------------------------------
function rungdb {
    rm -f "`pwd`/.launcher"
    checkprog "$1"
    ln -s "$fname" ".launcher"
    IFS=""
    "${unsetenv[@]}" gdb --args "`pwd`/.launcher" "${@:2}"
}


# -----------------------------------------------------
# runs program directly
#   env-vars are ordered like in gdb
# -----------------------------------------------------
function runprog {
    rm -f "`pwd`/.launcher"
    getenvs
    checkprog "$1"
    ln -s "$fname" ".launcher"
    IFS=""
    if [ "$preprog" ]; then
        env -i "${envlist[@]}" "$preprog" "`pwd`/.launcher" "${@:2}"    
    else
        env -i "${envlist[@]}" "`pwd`/.launcher" "${@:2}"
    fi
}


# -----------------------------------------------------
# checks program for existance
#   and returns fullpath
# -----------------------------------------------------
function checkprog {
    fname="`which $1`" #full path
    if [ "${1:0:2}" = "./" ]; then
        fname="`readlink -f "${1:2}"`"
    fi
    if [ ! -e "$fname" ]; then
        echo "Error: cant find program '$fname'"
        exit
    fi
}

IFS=""
case $1 in
    gdb)
        if [ $2 = "--args" ]; then 
            prog="$3"
            args=("${@:3}")
        else
            prog="$2"
            args=("${@:2}")
        fi
        rungdb "${args[@]}"
    ;;
    strace|ltrace)
        preprog="$1"
        runprog "${@:2}"
    ;;
    clean)
        rm -f .envorder .envorder.c
        rm -f .dump.c .dump
        rm -f .gdblist .launcher
    ;;
    ""|"-h"|"--help")
        echo "Usage:"
        echo
        echo "  $0 ./program - run program"
        echo "  $0 strace ./program - run program in strace"
        echo "  $0 ltrace ./program - run program in ltrace"
        echo "  $0 gdb ./program [arg1 [arg2 [ ... ]]] - run program in gdb"
        echo
    ;;
    *) 
        runprog "${@:1}"
    ;;
esac
rm -f .launcher
