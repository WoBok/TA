import os

prefix = input("Input your prefix string:")

names = os.listdir()

names_default = [name for name in names if os.path.splitext(name)[1] != ".meta"]
names_meta = [name for name in names if os.path.splitext(name)[1] == ".meta"]

index = 1
for name in names_default:
    if name != "Renamer.py":
        ext = name.split(".")[-1]
        os.rename(name, f"{prefix}_{index:02}.{ext}")
        index += 1

index = 1
for name in names_meta:
    ext = name.split(".")[-2:]
    os.rename(name, f"{prefix}_{index:02}.{ext[0]}.{ext[1]}")
    index += 1
