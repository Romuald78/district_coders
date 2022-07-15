#ifndef GEN_DC_H
    #define GEN_DC_H
    
    #define CLR_NORMAL "\33[0m"
    #define CLR_RED    "\33[38;2;255;0;0m"
    #define CLR_GREEN  "\33[38;2;0;255;0m"
    #define CLR_YELLOW "\33[38;2;255;255;0m"

    typedef enum{
        RES_OK  = 0xA5,
        RES_ERR = 0x5A
    } Result;

    typedef enum{
        MODE_NONE     = 0x00,
        MODE_GENERATE = 0x49,
        MODE_VERIFY   = 0x94
    } Mode;
    
    // Implement the following functions
    Result generate(int seed);
    Result verify  (int seed, float* result_perc);
    void   error   (const char* format, ...); 
    void   message (const char* format, ...); 

#endif
