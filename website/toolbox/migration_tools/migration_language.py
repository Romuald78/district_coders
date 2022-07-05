
#----------------------------------------------
import os

from district.models.language import Language

defaultC = """
#include <stdio.h>

int main(int argc, char** argv){
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
            "name" :"JS",
            "value":"js",
            "code" :defaultJS
         },
         {
            "name" :"Java",
            "value":"java",
            "code" :defaultJava
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

def language_migration():
    # Create default languages
    print()
    print("  [DATA MIGRATION][LANGUAGES]")
    for lang in migrate_langs:
        # prepare table field values
        name  = lang["name"]
        value = lang["value"]
        file  = os.path.join("icons", "languages", f"logo_{value}.png")
        prog  = f"{value.upper()}Program"
        # Create language object
        obj = Language()
        # Set fields
        obj.name = name
        obj.icon = file
        obj.default_code = lang["code"]
        obj.language_program = prog
        # Save it to DB
        obj.save()
        # print
        print(f"    > Language [{obj.id}]:'{name}' added !")
