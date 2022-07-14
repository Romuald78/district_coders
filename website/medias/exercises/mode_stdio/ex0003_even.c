#include <stdio.h>
#include <stdlib.h>

#include <genDC.h>

int getValue(){
    int v = (rand()%1000) - 500;
    return v & 0xFFFFFFFE;
}

int getN(){
    return rand()%191 + 10;
}

Result generate(int seed){
    int N = 0;
    srand(seed);
    N = getN();
    printf("%d\n", N);
    for(int i=0; i<N; i++){
        printf("%d\n", getValue());
    }
    // Generation return is always ok 
    return RES_OK;
}

Result verify(int seed, float* result_perc){
    int    answer = 0;
    int    user   = 0;
    int    N      = 0;
    int    total  = 0;
    int    good   = 0;
    Result res    = RES_OK;
    srand(seed);
    N = getN();

    // We dont stop the verification if one value is not correct
    // So it is easier for the user to see which values work and which don't 
    // unless there is no [INFO] displayed for this exercice or we don't want.
    // to flood the stderr    
    for(int i=0; i<N; i++){
        answer = getValue();
        if(answer%2 == 1){
            continue;
        }
        total++;
        // If we cannot read from the stdin: we stop the verification
        if( fscanf(stdin, "%d\n", &user ) != 1){
            error("Impossible to read standard input !\n");
            *result_perc = (100.0*good)/total;
            return RES_ERR;
        }
        if(user != answer){
            error("Received '%d' / Expected '%d'\n", user, answer);
        }
        else{
            good++;
        }
    }
    // return result of verification
    *result_perc = (100.0*good)/total;
    return RES_OK;
}

