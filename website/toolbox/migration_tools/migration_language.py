
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
console.log("answer);
"""

#----------------------------------------------
defaultPHP = """
<?php
    echo("answer");
?>
"""

#----------------------------------------------
defaultPython = """
print("answer")
"""

#----------------------------------------------
defaultJava = """
default Java code 
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
            "name" :"Java",
            "value":"java",
            "code" :defaultJava
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
