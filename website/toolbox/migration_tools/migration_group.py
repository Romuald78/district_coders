

#----------------------------------------------
import os

from district.models.group import GroupDC
from website.settings import DEFAULT_GROUP_KEY

migrate_group = [{
            "name" : DEFAULT_GROUP_KEY.title(),
            "key"  : DEFAULT_GROUP_KEY,
            "descr": "This is the default group. It gathers all District Coders."
         }
    ]

def group_migration(apps, schema_editor):
    # create default groups
    print()
    print("  [DATA MIGRATION][GROUPS]")
    for mode in migrate_group:
        # prepare table field values
        name  = mode["name"]
        key   = mode["key"]
        descr = mode["descr"]
        file = os.path.join("icons", "groups", f"group_{key}.png")
        # Create language object
        obj = GroupDC()
        # Set fields
        obj.name = name
        obj.register_key = key
        obj.icon = file
        obj.description = descr
        # Save it to DB
        obj.save()
        # print
        print(f"    > Group [{obj.id}]:'{name}' added !")
