a = [1, 2, 3]
b = ["a", "b", "c"]
z = zip(a, b)
print(z)
# print(list(z)) #使用后迭代器将被耗尽，再进行迭代将会抛出异常StopIteration
print(next(z))
print(next(z))
print(next(z))
# print(next(z)) #迭代器已被耗尽，抛出异常StopIteration

b = {5: "a", 6: "b", 7: "c"}
z = zip(a, b)
print(list(z))  # result: [(1, 5), (2, 6), (3, 7)]

b = ["a", "b", "c"]
z = zip(a, b)
c, d = zip(*z)  # (1, 2, 3) ('a', 'b', 'c') 解压
print(c, d)

b = ["a", "b", "c", "d"]
z = zip(a, b)
print(
    list(z)
)  # result: [(1, 'a'), (2, 'b'), (3, 'c')] 长度不一致时较长可迭代对象中的剩余项将被忽略，结果会裁切至最短可迭代对象的长度

z = zip(a, b, strict=True)  # 使用strict严格限制两个可迭代对象的长度必须保持一致
# print(list(z))  # ValueError: zip() argument 2 is longer than argument 1

a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")
z = zip(a, b)
print(list(z))  # [('John', 'Jenny'), ('Charles', 'Christy'), ('Mike', 'Monica')]

for i, x in enumerate(a):
    print(b[i], x)

dictionary = {"name": "Alice", "age": 25, "city": "New York"}
keys, values = zip(*dictionary.items())
print(keys)  # ('name', 'age', 'city')
print(values)  # ('Alice', 25, 'New York')

a = (1, 2, 3)
c, d, e = a

tuple6 = 1, 2, 3, 4, 5  # 等同(1, 2, 3, 4, 5)
print(tuple6)
a, b, *rest = tuple6
print(a, b, rest)
