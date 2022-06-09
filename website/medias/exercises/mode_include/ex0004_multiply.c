#include <stdio.h>
#include <stdlib.h>

#include <genDC.h>

int multiply2ints(int a, int b);

int getValue(){
    int v = (rand()%1000) - 500;
    return v & 0xFFFFFFFE;
}

int getN(){
    return rand()%191 + 10;
}

// Mode include : generation will call the user functions
Result generate(int seed){
    int N = 0;
    int x = 0;
    int y = 0;
    int r = 0;
    srand(seed);
    N = getN();
    for(int i=0; i<N; i++){
        x = getValue();
        y = getValue();
        // Call user function
        r = multiply2ints(x, y);
        printf("%d\n", r);
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
    N = getN();

    // We dont stop the verification if one value is not correct
    // So it is easier for the user to see which values work and which don't 
    // unless there is no [INFO] displayed for this exercice or we don't want.
    // to flood the stderr    
    for(int i=0; i<N && res==RES_OK; i++){
        answer = getValue() * getValue();
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

