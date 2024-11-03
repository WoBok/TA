#zoo.py


class Zoo:

    def __init__(self, animals=[]):
        self.animals = animals

    def add_animal(self, animal):
        self.animals.append(animal)

    def show_animals(self):
        for animal in self.animals:
            #列出所有动物的方法,通过callable过滤掉不可调用的属性，通过判断属性开头和结尾的下划线过滤掉私有属性
            all_attributes = dir(animal)
            methods = [
                attr for attr in all_attributes
                if callable(getattr(animal, attr))
                and not attr.startswith('__') and not attr.endswith('__')
            ]
            print(
                f"The class {type(animal).__name__} has the following functions:\n{methods}"
            )
            print(animal)

    def feed_animals(self):
        for animal in self.animals:
            print(
                f"{animal.species} is {animal.eat()} and says: {animal.speak()}!"
            )
