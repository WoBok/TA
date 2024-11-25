a = [x for x in range(0,100,2)]
for i,x in enumerate(a):
    print(i,x)

e = enumerate(a)
print(list(e))