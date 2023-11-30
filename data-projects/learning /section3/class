class Cat:
    species = 'mammal'

    def __init__(self, name, age, id):
        self.name = name
        self.age = age
        self.id = id


cat1 = Cat('mio', 1, 23)
cat2 = Cat('hatola', 2, 33)
cat3 = Cat('miomiomio', 3, 44)

print(cat1.name, cat1.age, cat1.id)
print(cat2.name, cat2.age, cat2.id)
print(cat3.name, cat3.age, cat3.id)


def oldest_age(*args):
    return max(args)


print(f'the age of the old cat is: {oldest_age(cat1.age, cat2.age, cat3.age)} years old')
