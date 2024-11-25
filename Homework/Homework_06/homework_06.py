def fiboDictGenerator():
    counter = 2
    yield {0: [0]}
    yield {1: [1]}
    fiboDict = {0: [0], 1: [1]}
    while True:
        fiboDict[counter] = fiboDict[counter - 2] + fiboDict[counter - 1]
        counter += 1
        yield fiboDict.copy()  # 使用copy()返回字典的副本，防止外部修改字典


fiboGene = fiboDictGenerator()

# next(fiboGene)
# next(fiboGene)
# d1 = next(fiboGene)
# d1[2] = [1, 1]
# next(fiboGene)
# next(fiboGene)
# d2 = next(fiboGene)
# print(d2)

for i in range(10):
    print(next(fiboGene))
