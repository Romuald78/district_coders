#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "genDC.h"

char* TITLE = NULL;
int   titleSent = 0;

void prepareTitle(){
    // Locals
    char tmp[] = "[DISTRICT CODERS]";
    int  N = strlen(tmp);
    int  R = 0;
    int  G = 0;
    int  B = 255;
    int  j = 0;
    // allocate title string
    TITLE = malloc(sizeof(char) * 512);
    if(TITLE == NULL){
        error("Internal error -1000 !\n", stderr);
        exit(0xFF);
    }    
    // Process each character
    for(int i=0;i<17;i++){
        if(tmp[i] != ' '){
            j += sprintf(TITLE+j, "\33[38;2;%d;%d;%dm", R, G, B);  
            R += 16;
            G += 16;
            B -= 16;
            if(R>255) R=255;  
            if(G>255) G=255;  
            if(B<0  ) B=0;
        }
        TITLE[j++] = tmp[i];
    }
    TITLE[j] = '\0';
}

// Result of verification : stdout
void displayTitleOnce(){
    // Display title
    if(titleSent == 0){
        fprintf(stdout, "%s\n", TITLE);
        titleSent = 1;
    }
    fputs(CLR_NORMAL, stdout);
}

// Debug + Error : STDERR
void display(Result res, const char* format, va_list args){
    // Display title
    // displayTitleOnce();
    // display line header
    if(res != RES_ERR){
        fputs (CLR_NORMAL "[INFO] ", stderr);
    }
    else{
        fputs (CLR_RED "[ERROR] ", stderr);
    }
    // display information (if format string is ok)
    if(format != NULL){
        // Start retrieving arguments and display
        vfprintf(stderr, format, args );       
    }
    fputs(CLR_NORMAL, stderr);
    fflush(stderr);    
}

void error(const char* format, ...){
    // List of arguments
    va_list args;
    if(format != NULL){
        // Start retrieving arguments
        va_start(args, format );
        // display
        display(RES_ERR, format, args);
        // Clean up list
        va_end  (args);
    }
}

void message(const char* format, ...){
    // List of arguments
    va_list args;
    if(format != NULL){
        // Start retrieving arguments
        va_start(args, format );
        // display
        display(RES_OK, format, args);
        // Clean up list
        va_end  (args);
    }
}

// parameters are :
// -g : generation
// -v : verification
// -sxxx : xxx is the seed used for the process  
// -txxx : xxx i the threshold to indicate if exercice is either passed or failed
// output will be a positive value from 0 to 200 [0.0% to 100.0%] if no error encountered
// else it will be a negative value for errors
// That means the program gives a score with 0.5% precision, rounded to the nearest 0.5%
int main(int argc, char** argv){
    // Local variables
    Mode   mode        =  MODE_NONE;
    Result result      =  RES_ERR;
    float  result_perc =  0.0;
    int    ret_val     =  0;
    float  thres_perc  =  0.0;
    unsigned long seed =  0;
    int seed_index     =  0;
    int thres_index    =  0;

    // prepare title
    // prepareTitle();
    // Check number of arguments
    if(argc != 4){
        error("Bad number of arguments (%d-1) !\n", argc);
        exit(-1);
    }  
    // Check argv are ok
    if(argv[1] == NULL || argv[2] == NULL || argv[3] == NULL){
        error("Empty arguments (%p/%p) !\n", argv[1], argv[2]);
        exit(-2);
    }  
    // Check option starts
    if( argv[1][0] != '-' || argv[2][0] != '-'  || argv[3][0] != '-'){
        error("Bad argument starts (%c/%c/%c) !\n", argv[1][0], argv[2][0], argv[3][0]);
        exit(-3);
    }
    // Get parameters
    for(int i=1; i<argc; i++){
        if (argv[i][1] == 's'){
            // Check seed length
            if(strlen(argv[i])<=2){
                error("Bad param length (-s) !\n");
                exit(-4);
            } 
            seed_index = i;            
        }
        else if (argv[i][1] == 't'){
            // Check seed length
            if(strlen(argv[i])<=2){
                error("Bad param length (-t) !\n");
                exit(-5);
            } 
            thres_index = i;            
        }
        else if (argv[i][1] == 'g'){
            if (mode != MODE_NONE){
                error("Bad mode (impossible to generate AND verify at the same time) !\n");
                exit(-6);
            }
            if(strlen(argv[i])!=2){
                error("Bad param length (-g) !\n");
                exit(-7);
            } 
            mode = MODE_GENERATE;
        }
        else if (argv[i][1] == 'v'){
            if (mode != MODE_NONE){
                error("Bad mode (impossible to generate AND verify at the same time) !\n");
                exit(-8);
            }
            if(strlen(argv[i])!=2){
                error("Bad param length (-v) !\n");
                exit(-9);
            } 
            mode = MODE_VERIFY;
        }
        else{
            error("Bad mode value (-%c) !\n", argv[i][1]);
            exit(-10);
        }  
    }

    // Check seed characters
    for(int i=2; i<strlen(argv[seed_index]); i++){
        if(argv[seed_index][i] < '0' || argv[seed_index][i] > '9'){
            error("Bad seed characters (%s) !\n", argv[seed_index]);
            exit(-11);
        }
    }
    // Check seed length (max 9 digits)
    if( strlen(argv[seed_index]) > 11 ){
        error("Bad seed length (%s) !\n", argv[seed_index]);
        exit(-12);
    }    
    // Check seed value
    if( sscanf(argv[seed_index]+2, "%ld", &seed) != 1 ){
        error("Impossible to retrieve seed !\n");
        exit(-13);
    }

    // Check threshold characters
    for(int i=2; i<strlen(argv[thres_index]); i++){
        if( argv[thres_index][i] != '.' && (argv[thres_index][i] < '0' || argv[thres_index][i] > '9') ){
            error("Bad threshold characters (%s) !\n", argv[thres_index]);
            exit(-14);
        }
    }
/*
    // Check seed length (max 9 digits)
    if( strlen(argv[thres_index]) > 11 ){
        error("Bad threshold length (%s) !\n", argv[thres_index]);
        exit(-13);
    }
*/
    // Check threshold value
    if( sscanf(argv[thres_index]+2, "%f", &thres_perc) != 1 ){
        error("Impossible to retrieve threshold !\n");
        exit(-15);
    }
    if (thres_perc < 0 || thres_perc > 100){
        error("Threshold must be between 0 and 100 included !\n");
        exit(-16);
    }

    // Now we can call the exercice function and retrieve result
    if( mode == MODE_GENERATE ){
        result = generate(seed);
        if(result != RES_OK){
            error("Internal error !\n");
            exit(-17);
        }
        result_perc = 100.0;
    }        
    else if( mode == MODE_VERIFY ){
        result = verify(seed, &result_perc);
        // TODO check the user does not send too much data
        // Display title
        // displayTitleOnce();
        // display result
        fputs("Test result ", stdout);
        if((result == RES_OK) && (result_perc >= thres_perc)){
            fputs(CLR_GREEN"[PASS]", stdout);
        }
        else if(result_perc >= thres_perc){
            fputs(CLR_YELLOW"[WARNING]", stdout);
        }
        else{
            fputs(CLR_RED"[FAIL]", stdout);
        }
        float disp_perc = ((int)(2*result_perc+0.5))/2.0;
        fprintf(stdout, CLR_NORMAL" (result=%.1f%%/target=%.1f%%)\n", disp_perc, thres_perc);
    }
    else{
        error("Internal error !\n");
        exit(-18);
    }
    // Check result percent is between 0 and 100.0
    if(result_perc < 0 || result_perc > 100){
        error("Internal error : result percent is not between 0 and 100 (%.1f)!\n", result_perc);
        exit(-19);
    }
    // Free title
    // free(TITLE);
    return (int)(2*result_perc + 0.5);
}
