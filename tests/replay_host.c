#include <stdio.h>
#include <stdlib.h>
void cmo_fail(void){fputs("Portable replay failed\n",stderr);abort();}
#define main replay_main
#include "portable_replay.c"
#undef main
int main(void){int rc=replay_main();printf("Portable replay: PASS; %llu checks\n",(unsigned long long)cmo_checks);return rc;}
