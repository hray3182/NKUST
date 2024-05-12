class Student:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.transcript: dict['Course', int] = {}
        
    def __str__(self) -> str:
        return f"Name: {self.name}, ID: {self.id}"
        
    def add_grade(self, course: 'Course', score):
        if course not in self.transcript:
            self.transcript[course] = score
            print(f"{self.name} got {score} in {course.name}")
            return
        print(f"{self.name} already has a grade in {course.name}")
        
    def edit_grade(self, course: 'Course', score):
        if course in self.transcript:
            print(f"Modify {self.name}'s grade in {course.name} from {self.transcript[course]} to {score}")
            self.transcript[course] = score
            return
        print(f"{self.name} does not have a grade in {course.name}")
    
    def print_transcript(self):
        print(f"Transcript for {self.name}")
        for course, score in self.transcript.items():
            print(f"{course.name}: {score}")
    
class Course:
    def __init__(self, name, code) -> None:
        self.name = name
        self.code = code
        self.students: list[Student] = []

    def add_student(self, student: Student):
        if student in self.students:
            print(f"{student.name} is already in {self.name}")
            return
        self.students.append(student)
        print(f"{student.name} is added to {self.name}")

    def remove_student(self, student: Student):
        if student not in self.students:
            print(f"{student.name} is not in {self.name}")
            return
        self.students.remove(student)
        print(f"{student.name} is removed from {self.name}")
        
class Postgraduate(Student):
    def __init__(self, name, id, research, advisor) -> None:
        super().__init__(name, id)
        self.research = research
        self.advisor = advisor

        
if __name__ == "__main__":
    student1 = Student("Peter", "001")
    student2 = Student("Mary", "002")
    
    course1 = Course("Math", "MATH101")
    course2 = Course("English", "ENGL101")
    
    course1.add_student(student1)
    course1.add_student(student2)
    course1.add_student(student2)
    course1.remove_student(student1)
    
    course2.add_student(student1)
    course2.remove_student(student2)
    
    student1.add_grade(course1, 90)
    student1.add_grade(course2, 80)
    student1.add_grade(course2, 85)
    
    student1.edit_grade(course1, 95)
    
    student1.print_transcript()
    
    postgraduate1 = Postgraduate("John", "003", "AI", "Dr. Lee")
    postgraduate1.add_grade(course1, 100)
    
    print(postgraduate1.research)
    print(postgraduate1.advisor)
    
        
