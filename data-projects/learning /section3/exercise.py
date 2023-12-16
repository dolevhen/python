class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

    def __str__(self):
        return ', '.join([animal.name for animal in self.animals])

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Simon(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Sally(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Mezi(Cat):
    def sing(self, sounds):
        return f'{sounds}'

# Create 3 cat instances
my_cats = [Simon('Simon', 3), Sally('Sally', 2), Mezi('Mezi', 1)]

# Instantiate the Pets class with your cats
my_pets = Pets(my_cats)

# Now when you print my_pets, it should print the names of the cats
print(my_pets)

#4 Output all of the cats walking using the my_pets instance
print(my_cats[0].walk())
print(my_cats[1].walk())
print(my_cats[2].walk())
