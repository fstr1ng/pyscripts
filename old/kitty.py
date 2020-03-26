class Pet(object):
    """Pet main class"""

    def __init__(self, name, age, sex):
        """Constructor"""
        self.name = name
        self.age = age
        self.sex = sex

    def hello(self):
        return "Hello! My name is " + self.name

    def bye(self):
        return "Bye-bye!"

if __name__ == "__main__":

    name = input("The name is: ")
    pet = Pet(name, 0, "m")
    print(pet.hello())
