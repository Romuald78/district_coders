#include <stdio.h>
#include <stdlib.h>

#include <genDC.h>

int getValue(){
    return (rand()%1000) - 500;
}

Result generate(int seed){
    int N = 0;
    srand(seed);
    N = rand()%91 + 10;
    printf("%d\n", N);
    for(int i=0; i<N; i++){
        printf("%d\n", getValue());
    }
    // Generation return is always ok 
    return RES_OK;
}

Result verify(int seed){
    int    answer = 0;
    int    user   = 0;
    int    N      = 0;
    Result res    = RES_OK;
    srand(seed);
    N = rand()%91 + 10;

    // We dont stop the verification if one value is not correct
    // So it is easier for the user to see which values work and which don't 
    // unless there is no [INFO] displayed for this exercice or we don't want.
    // to flood the stderr    
    for(int i=0; i<N && res==RES_OK; i++){
        answer = getValue();
        if(answer%2 == 1){
            continue;
        }
        // If we cannot read from the stdin: we stop the verification
        if( fscanf(stdin, "%d\n", &user ) != 1){
            error("Impossible to read standard input !\n");            
            res = RES_ERR;
            //break;
        }
        // Check user answer
        if(user != answer){
            error("Received '%d' / Expected '%d'\n", user, answer);            
            res = RES_ERR;
        }
    }
    // return result of verification
    return res;
}

