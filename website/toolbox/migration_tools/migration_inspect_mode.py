

#----------------------------------------------
import os

from district.models.inspector_mode import InspectorMode

migrate_inspect_mode = [{
            "name" :"mode_stdio",
         },
         {
            "name" :"mode_include",
         }
    ]

def mode_migration():
    # create default inspector modes
    print()
    print("  [DATA MIGRATION][INSPECTOR MODES]")
    for mode in migrate_inspect_mode:
        # prepare table field values
        name = mode["name"]
        file = os.path.join("icons", "modes", f"{name}.png")
        # Create language object
        obj = InspectorMode()
        # Set fields
        obj.name = name
        obj.icon = file
        # Save it to DB
        obj.save()
        # print
        print(f"    > Mode [{obj.id}]:'{name}' added !")
