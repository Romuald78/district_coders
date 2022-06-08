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
    int    mini   = 0;
    int    maxi   = 0;
    srand(seed);
    N = rand()%91 + 10;

    // We dont stop the verification if one value is not correct
    // So it is easier for the user to see which values work and which don't 
    // unless there is no [INFO] displayed for this exercice or we don't want.
    // to flood the stderr    
    for(int i=0; i<N ; i++){
        answer = getValue();
        if(i == 0){
            mini = answer;
            maxi = answer;
        }
        if(mini > answer){
            mini = answer;
        }
        if(maxi < answer){
            maxi = answer;
        }
    }

    // If we cannot read from the stdin: we stop the verification
    if( fscanf(stdin, "%d\n", &user ) != 1){
        error("Impossible to read standard input !\n");            
        return RES_ERR;
    }
    // Check user answer
    if(user != mini){
        error("Received '%d' / Expected '%d'\n", user, mini);            
        return RES_ERR;
    }
    // If we cannot read from the stdin: we stop the verification
    if( fscanf(stdin, "%d\n", &user ) != 1){
        error("Impossible to read standard input !\n");            
        return RES_ERR;
    }
    // Check user answer
    if(user != maxi){
        error("Received '%d' / Expected '%d'\n", user, maxi);            
        return RES_ERR;
    }
    // return result of verification
    return RES_OK;
}

