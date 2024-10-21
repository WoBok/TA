import os

targetStr = input('Input your target string:')
replacementStr = input("Input your replacement string:")

names = os.listdir()

for name in names:
    newName = name.replace(targetStr,replacementStr)
    os.rename(name,newName)