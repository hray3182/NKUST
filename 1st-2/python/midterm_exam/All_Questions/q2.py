class Food:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type

class Animal:
    def __init__(self, species, age, gender, diet) -> None:
        self.species = species
        self.age = age
        self.gender = gender
        self.diet = diet
        # 為了體現移動方式給的屬性
        self.position_x = 0
        self.position_y = 0

    def __str__(self) -> str:
        return f"Species: {self.species}, Age: {self.age}, Gender: {self.gender}"
    
    def feed(self, food: Food):
        if food.type == self.diet or self.diet == "Omnivore":
            print(f"{self.species} is eating {food.name}")
        else:
            print(f"{self.species} does not eat {food.name}")

    def move(self, x, y):
        diff_x = x - self.position_x
        diff_y = y - self.position_y
        if diff_x > 0:
            print(f"{self.species} moves {abs(diff_x)} step(s) right")
        else:
            print(f"{self.species} moves {abs(diff_x)} step(s) left")

        if diff_y > 0:
            print(f"{self.species} moves {abs(diff_y)} step(s) up")
        else:
            print(f"{self.species} moves {abs(diff_y)} step(s) down")
        
        self.position_x = x
        self.position_y = y

        
class Mammal(Animal):
    def __init__(self, species, gender, age, diet, coat_color):
        super().__init__(species, age, gender, diet)
        self.coat_color = coat_color
    
    def print_coat_color(self):
        print(f"{self.species}'s coat color is {self.coat_color}")

class Bird(Animal):
    def __init__(self,species, gender, age, diet, span):
        super().__init__(species, age, gender, diet)
        self.span = span

    def move(self, x, y):
        print(f"{self.species} flies to x: {x} y: {y}")
        self.position_x = x
        self.position_y = y
    
    def print_span(self):
        print(f"{self.species}'s span is {self.span} cm")
        
if __name__ == "__main__":
    banana = Food("Banana", "Herbivore")
    pork = Food("Pork", "Carnivore")

    lion = Mammal("lion", "male", 10, "Carnivore", "yellow")
    print(lion)
    lion.feed(banana)
    lion.feed(pork)
    lion.move(3, 5)
    lion.print_coat_color
    
    sparrow = Bird("sparrow", "female", 5, "Omnivore", 5)
    sparrow.feed(banana)
    sparrow.feed(pork)
    sparrow.move(10, 20)
    sparrow.print_span()

                
                
                
                