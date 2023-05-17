import sys
from pathlib import Path
import datetime
import shutil
import json

# Welcome msg
print("Yark archive v4 to v3 migrator")

# Get path
path = Path(input("Path to archive directory: "))
print(f"Actual path to use: {path.resolve()}")
if (input("Are you sure? (y/n): ")).lower() != "y":
    print("Exiting..")
    sys.exit(0)
if not path.exists():
    print("Archive directory doesn't exist", file=sys.stderr)
    sys.exit(1)
elif not path.is_dir():
    print("Archive directory isn't a directory", file=sys.stderr)
    sys.exit(1)

# Backup
backup_name = f"yark-v4v3-{datetime.datetime.utcnow().isoformat()}.bak"
print(f"Backing up your yark.json as {backup_name}")
path_yark = path / "yark.json"
path_backup = path / backup_name
shutil.copyfile(path_yark, path_backup)

# Modify archive top-level
print("Modifying archive top-level")
archive = json.load(open(path_yark, "r"))
archive["version"] = 3
del archive["comment_authors"]


# Modify archive video lists
def mig_videos_list(ib: dict) -> list[dict]:
    buf = []
    for id in ib.keys():
        video = ib[id]
        video["id"] = id
        del video["comments"]
        buf.append(video)
    return buf


print("Modifying archive videos list")
archive["videos"] = mig_videos_list(archive["videos"])
print("Modifying archive livestreams list")
archive["livestreams"] = mig_videos_list(archive["livestreams"])
print("Modifying archive shorts list")
archive["shorts"] = mig_videos_list(archive["shorts"])

# Save archive
with open(path_yark, "w+") as file:
    print("Saving yark.json")
    json.dump(archive, file)

# Rename directory
print("Renaming images directory back to thumbnails")
path_images = path / "images/"
path_images.rename(path / "thumbnails/")

# End
print("Hope this helps!")
