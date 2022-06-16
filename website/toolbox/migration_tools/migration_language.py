
#----------------------------------------------
defaultC = """
#include <stdio.h>

int main(int argc, char** argc){
    printf("answer");
    return 0;
}
"""

#----------------------------------------------
defaultCPP = """
default C++ code 
"""

#----------------------------------------------
defaultCSharp = """
default C# code 
"""

#----------------------------------------------
defaultJS = """
default JS code 
"""

#----------------------------------------------
defaultPHP = """
default PHP code 
"""

#----------------------------------------------
defaultPython = """
default Python code 
"""

#----------------------------------------------
migrate_langs = [{
            "name" :"C",
            "value":"c",
            "code" :defaultC
         },
         {
            "name" :"C++",
            "value":"cpp",
            "code" :defaultCPP
         },
         {
            "name" :"C#",
            "value":"csharp",
            "code" :defaultCSharp
         },
         {
            "name" :"JS",
            "value":"js",
            "code" :defaultJS
         },
         {
            "name" :"PHP",
            "value":"php",
            "code" :defaultPHP
         },
         {
            "name" :"Python",
            "value":"python",
            "code" :defaultPython
         }
    ]
