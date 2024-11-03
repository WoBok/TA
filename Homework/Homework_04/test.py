#test.py

from animal import Lion, Elephant, Monkey
from zoo import Zoo

animals = [Lion('Leo', 5), Elephant('Ella', 10)]
magicalZoo = Zoo(animals)
magicalZoo.add_animal(Monkey('Momo', 3))
magicalZoo.show_animals()
print('\n')
magicalZoo.feed_animals()
'''-------------------------Test-------------------------'''
# showanimals = getattr(magicalZoo, 'show_animals')
# print(callable(showanimals))
# name = getattr(Lion('Leo', 5), 'name')
# print(callable(name))
