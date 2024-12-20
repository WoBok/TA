import os

suffix = input("Input your suffix string:")

names = os.listdir()

for name in names:
    extension = os.path.splitext(name)[1]
    newName = name.replace(extension, suffix + extension)
    os.rename(name, newName)
