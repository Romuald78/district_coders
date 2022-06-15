#include <stdio.h>
#include <stdlib.h>

int main(){

    int N = 0;
    int V = 0;
    int mini =  1000000000;
    int maxi = -1000000000;
    srand(0);
    if( fscanf(stdin, "%d\n", &N ) != 1){
        return 1;
    }
    for(int i=0; i<N;i++){
        if( fscanf(stdin, "%d\n", &V ) != 1){
            return 1;
        }    
        if(mini > V){
            mini = V;
        }
        if(maxi < V){
            maxi = V;
        }
    }
    printf("%d\n", mini);
    printf("%d\n", maxi);
    return 0;
}
