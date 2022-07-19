#include <stdio.h>
#include <stdlib.h>

int main(){

    int N = 0;
    int V = 0;
    srand(0);
    if( fscanf(stdin, "%d\n", &N ) != 1){
        return 1;
    }
    for(int i=0; i<N;i++){
        if( fscanf(stdin, "%d\n", &V ) != 1){
            return 1;
        }    
        if(V < 0){
            V = -V;
        }
/*
        if(i==5){
            V = 666;
        }
        if(i==8) break;
*/
        printf("%d\n", -V);
    }
    return 0;
}
