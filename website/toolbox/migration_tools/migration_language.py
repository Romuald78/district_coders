
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
console.log("answer");
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
public class User {
    public static void main(String[] args){
        System.out.println("answer");
    }
}
"""


#----------------------------------------------
migrate_langs = [
    {"name":"C",                    "value":"c",        "code":defaultC     },
    {"name":"C++",                  "value":"cpp",      "code":defaultCPP   },
    {"name":"C#",                   "value":"csharp",   "code":defaultCSharp},
    {"name":"Javascript",           "value":"js",       "code":defaultJS    },
    {"name":"Java",                 "value":"java",     "code":defaultJava  },
    {"name":"PHP",                  "value":"php",      "code":defaultPHP   },
    {"name":"Python",               "value":"python",   "code":defaultPython},
    {"name":"Visual Basic .NET",    "value":"vbnet",    "code":""           },
    {"name":"R",                    "value":"r",        "code":""           },
    {"name":"Go",                   "value":"go",       "code":""           },
    {"name":"Visual Basic",         "value":"vb",       "code":""           },
    {"name":"Swift",                "value":"swift",    "code":""           },
    {"name":"Ruby",                 "value":"ruby",     "code":""           },
    {"name":"Perl",                 "value":"perl",     "code":""           },
    {"name":"Objective-C",          "value":"objc",     "code":""           },
    {"name":"Rust",                 "value":"rust",     "code":""           },
    {"name":"Kotlin",               "value":"kotlin",   "code":""           },
    {"name":"Dart",                 "value":"dart",     "code":""           },
    {"name":"Scala",                "value":"scala",    "code":""           },
    {"name":"Prolog",               "value":"prolog",   "code":""           },
    {"name":"Bash",                 "value":"bash",     "code":""           },
    {"name":"Haskell",              "value":"haskell",  "code":""           },
    {"name":"Lua",                  "value":"lua",      "code":""           }
]

def language_migration():
    print("coding language creation ...")
    # Create default languages
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
#        print(f"    > Language [{obj.id}]:'{name}' added !")
