#animal.py


class Animal:

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def speak(self):
        return 'Some sound'

    def eat(self):
        return 'Eat food'

    def __str__(self):
        return f"This is a {self.species} named {self.name}, aged {self.age}"


class Lion(Animal):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.species = 'Lion'

    def speak(self):
        return 'Roar'

    def eat(self):
        return 'eating meat'


class Elephant(Animal):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.species = 'Elephant'

    def speak(self):
        return 'Trumpet'

    def eat(self):
        return 'eating grass'


class Monkey(Animal):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.species = 'Monkey'

    def speak(self):
        return 'Ooh Ooh'

    def eat(self):
        return 'eating bananas'
