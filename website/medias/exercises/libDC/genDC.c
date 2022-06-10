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
    TITLE = malloc(sizeof(char) * 384);
    if(TITLE == NULL){
        error("Internal error 100 !\n", stderr);
        exit(100); 
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
    displayTitleOnce();
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
int main(int argc, char** argv){
    // Local variables
    int    seed_index = -1;
    int    mode_index = -1;
    int    L1     = 0;
    int    L2     = 0;
    Mode   mode   = 0;
    Result result = RES_ERR;
    unsigned long seed = 0;
    // prepare title
    prepareTitle();
    // Check number of arguments
    if(argc != 3){
        error("Bad number of arguments (%d-1) !\n", argc);
        exit(1);
    }  
    // Check argv are ok
    if(argv[1] == NULL || argv[2] == NULL){
        error("Empty arguments (%p/%p) !\n", argv[1], argv[2]);
        exit(2);    
    }  
    // Check argv lengths are ok
    L1 = strlen(argv[1]);
    L2 = strlen(argv[2]);
    if(L1 < 2 || L2 < 2){
        error("Bad argument lengths (%d/%d) !\n", L1, L2);
        exit(3);    
    }
    // Check option starts
    if( argv[1][0] != '-' || argv[2][0] != '-' ){
        error("Bad argument starts (%c/%c) !\n", argv[1][0], argv[2][0]);
        exit(4);    
    }
    // Check seed position
    if ( argv[1][1] == 's'){
        seed_index = 1;
        mode_index = 2;
    }
    else if( argv[2][1] == 's'){
        seed_index = 2;
        mode_index = 1;    
    }
    else{
        error("Seed option cannot be found (%s/%s) !\n", argv[1], argv[2]);
        exit(5);    
    }  
    // Now check mode position
    if( argv[mode_index][1] == 'g' ){
        mode = MODE_GENERATE;
    }
    else if( argv[mode_index][1] == 'v' ){
        mode = MODE_VERIFY;
    }    
    else{
        error("Bad mode value (-%c) !\n", argv[mode_index][1]);
        exit(5);    
    }  
    // Check mode argument length
    if( strlen(argv[mode_index]) != 2 ){
        error("Bad option (%s) !\n", argv[mode_index]);
        exit(6);    
    }    
    // Check seed characters
    for(int i=2; i<strlen(argv[seed_index]); i++){
        if(argv[seed_index][i] < '0' || argv[seed_index][i] > '9'){
            error("Bad seed characters (%s) !\n", argv[seed_index]);
            exit(7); 
        }
    }
    // Check seed length (max 9 digits)
    if( strlen(argv[seed_index]) > 11 ){
        error("Bad seed length (%s) !\n", argv[seed_index]);
        exit(8);    
    }    
    // Check seed value
    if( sscanf(argv[seed_index]+2, "%ld", &seed) != 1 ){
        error("Impossible to retrieve seed !\n", stderr);
        exit(9); 
    }
    // Now we can call the exercice function and retrieve result
    if( mode == MODE_GENERATE ){
        result = generate(seed);
        if(result != RES_OK){
            error("Internal error 10 !\n", stderr);
            exit(10);   
        }
    }        
    else if( mode == MODE_VERIFY ){
        result = verify(seed);
        // Display title
        displayTitleOnce();
        // display result
        fputs("Test result ", stdout);
        if(result == RES_OK){
            fputs(CLR_GREEN"[PASS]", stdout);
        }        
        else{
            fputs(CLR_RED"[FAIL]", stdout);
        }
        fputs(CLR_NORMAL"\n", stdout);
    }
    else{
        error("Internal error 11 !\n", stderr);
        exit(11); 
    }
    // Free title
    free(TITLE);
    // Return result of process
    return (result != RES_OK);    
}

