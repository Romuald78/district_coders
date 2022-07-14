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

Result verify(int seed, float* result_perc){
    int    answer = 0;
    int    user   = 0;
    int    N      = 0;
    int    good   = 0;
    Result res    = RES_OK;
    srand(seed);
    N = rand()%91 + 10;

    // We dont stop the verification if one value is not correct
    // So it is easier for the user to see which values work and which don't 
    // unless there is no [INFO] displayed for this exercice or we don't want.
    // to flood the stderr    
    for(int i=0; i<N ; i++){
        answer = getValue();
        if(answer < 0){
            answer = -answer;
        }
        // If we cannot read from the stdin: we stop the verification
        if( fscanf(stdin, "%d\n", &user ) != 1){
            error("Impossible to read standard input !\n");            
            res = RES_ERR;
            //break;
        }
        // Check user answer
        else if(user != answer){
            error("Received '%d' / Expected '%d'\n", user, answer);            
            res = RES_ERR;
        }
        else{
            // Displaying message when an answer is correct
            //message("Received '%d' / Expected '%d'\n", user, answer);
            good++;
        }
    }
    // return result of verification
    *result_perc = (100.0*good)/N;
    return RES_OK;
}

