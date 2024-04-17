class myRec:
    def __init__(self, heigh=10, weight=5):
        self.heigh = heigh
        self.weight = weight

    def __str__(self):
        return f"長: {self.heigh}, 寬{self.weight}"
        
    def show_info(self):
        print(self)
    
    def get_area(self):
        return self.heigh * self.weight

    def get_perimeter(self):
        return (self.heigh + self.weight) * 2

class test:
    def __init__(self):
        self.rec = myRec()
    
    def test_rec(self):
        print(self.rec)
        print(self.rec.get_area())
        print(self.rec.get_perimeter())



test().test_rec()