from enum import Enum
import json
import logging

class Faculty:
    def __init__(self, name, abbreviation, students, studyField):
        self.name = name
        self.abbreviation = abbreviation
        self.students = students
        self.studyField = studyField
    
    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student_email):
        for student in self.students:
            if student.email == student_email:
                self.students.remove(student)
                return True
        return False

    def has_student(self, student_email):
        for student in self.students:
            if student.email == student_email:
                return True
        return False

    def __str__(self):
        return f"Name: {self.name}, Abbreviation: {self.abbreviation}, Study Field: {self.studyField}"
    
class Student:
    def __init__(self, firstName, lastName, email, enrollDate, dateOfBirth):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.enrollDate = enrollDate
        self.dateOfBirth = dateOfBirth
    
    def __str__(self):
        return f"Name: {self.firstName} {self.lastName}, Date of Birth: {self.dateOfBirth}, Enroll Date: {self.enrollDate}"

class StudyField(Enum):
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    SOFTWARE_ENGINEERING = "Software Engineering"
    FOOD_TECHNOLOGY = "Food Technology"
    URBANISM_ARCHITECTURE = "Urbanism Architecture"
    VETERINARY_MEDICINE = "Veterinary Medicine"

def add_student(faculties):
    print("\nAdd a student to a faculty:")
    faculty_nr = int(input("Enter the index of the faculty to add the student to: "))
    if faculty_nr < 0 or faculty_nr >= len(faculties):
        logging.error("Invalid faculty index.")
        return
    
    faculty = faculties[faculty_nr]

    first_name = input("Enter student's first name: ")
    last_name = input("Enter student's last name: ")
    email = input("Enter student's email: ")
    enroll_date = input("Enter student's enrollment date (YYYY-MM-DD): ")
    dob = input("Enter student's date of birth (YYYY-MM-DD): ")
    student = Student(first_name, last_name, email, enroll_date, dob)
    faculty.add_student(student)
    print("Student added successfully to", faculty.name)

def remove_student(faculties):
    print("\nRemove a student from a faculty:")
    faculty_nr = int(input("Enter the index of the faculty: "))
    if faculty_nr < 0 or faculty_nr >= len(faculties):
        logging.error("Invalid faculty index.")
        return
    
    faculty = faculties[faculty_nr]

    student_email = input("Enter student's email to remove: ")
    if faculty.remove_student(student_email):
        print("Student removed successfully.")
    else:
        logging.error("Student not found.")

def display_faculties(faculties):
    print("\nList of faculties with indices:")
    for i, faculty in enumerate(faculties):
        print(f"{i}. {faculty}")

def display_students(faculties):
    print("\nList of students in faculties:")
    for faculty in faculties:
        print(f"Faculty: {faculty.name}")
        for student in faculty.students:
            print(student)

def add_faculty():
    name = input("Enter faculty name: ")
    abbreviation = input("Enter faculty abbreviation: ")
    study_field = input("Enter faculty study field: ")
    return Faculty(name, abbreviation, [], study_field)

def check_student_belongs_to_faculty(faculties):
    print("\nCheck if a student belongs to a faculty:")
    student_email = input("Enter student's email: ")
    for faculty in faculties:
        if faculty.has_student(student_email):
            print(f"The student with email {student_email} belongs to the faculty {faculty.name}.")
            return
    print(f"No faculty found for the student with email {student_email}.")

def display_graduates(faculties):
    print("\nList of graduates from faculties:")
    for faculty in faculties:
        print(f"Faculty: {faculty.name}")
        for student in faculty.students:
            print(student)

def remove_faculty(faculties):
    print("\nRemove a faculty:")
    display_faculties(faculties)
    faculty_nr = int(input("Enter the index of the faculty to remove: "))
    
    if faculty_nr < 0 or faculty_nr >= len(faculties):
        logging.error("Invalid faculty index.")
        return
    
    removed_faculty = faculties.pop(faculty_nr)
    print(f"Faculty '{removed_faculty.name}' removed successfully.")

def select_all_from_field(faculties):
    field = input("Insert the field: ")
    matching_faculties = [faculty for faculty in faculties if faculty.studyField == field]
    if matching_faculties:
        print(f"\nFaculties in the field '{field}':")
        for faculty in matching_faculties:
            print(f"{faculty.name} ({faculty.abbreviation})")
    else:
        logging.error(f"No faculties found in the field '{field}'.")

def batch_enrollment(faculties):
    try:
        filename = input("Enter the filename for batch enrollment: ")
        with open(filename, "r") as file:
            data = json.load(file)
            for faculty_name, student_list in data.items():
                for student_data in student_list:
                    faculty = next((fac for fac in faculties if fac.name == faculty_name), None)
                    if faculty:
                        student = Student(student_data["firstName"], student_data["lastName"], student_data["email"], student_data["enrollDate"], student_data["dateOfBirth"])
                        faculty.add_student(student)
                    else:
                        logging.error(f"Faculty '{faculty_name}' not found for batch enrollment.")
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found for batch enrollment.")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file '{filename}' for batch enrollment.")
    except Exception as e:
        logging.error(f"Error during batch enrollment: {str(e)}")

def batch_graduation(faculties):
    try:
        filename = input("Enter the filename for batch graduation: ")
        with open(filename, "r") as file:
            emails_to_graduate = json.load(file)
            for email in emails_to_graduate:
                for faculty in faculties:
                    if faculty.has_student(email):
                        faculty.remove_student(email)
                        break
    except FileNotFoundError:
        logging.error(f"File '{filename}' not found for batch graduation.")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file '{filename}' for batch graduation.")
    except Exception as e:
        logging.error(f"Error during batch graduation: {str(e)}")

def save_data(faculties):
    with open("data.json", "w") as f:
        data = []
        for faculty in faculties:
            faculty_data = {
                "name": faculty.name,
                "abbreviation": faculty.abbreviation,
                "students": [{
                    "firstName": student.firstName,
                    "lastName": student.lastName,
                    "email": student.email,
                    "enrollDate": student.enrollDate,
                    "dateOfBirth": student.dateOfBirth
                } for student in faculty.students],
                "studyField": faculty.studyField
            }
            data.append(faculty_data)
        json.dump(data, f)

def load_data():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            faculties = []
            for faculty_data in data:
                faculty = Faculty(faculty_data["name"], faculty_data["abbreviation"], [], faculty_data["studyField"])
                for student_data in faculty_data["students"]:
                    student = Student(student_data["firstName"], student_data["lastName"], student_data["email"], student_data["enrollDate"], student_data["dateOfBirth"])
                    faculty.students.append(student)
                faculties.append(faculty)
            return faculties
    except FileNotFoundError:
        return []
    
def menu():
    print("\n\t\t Menu\n")
    print("\t1 : Display Faculties\n")
    print("\t2 : Display Students\n")
    print("\t3 : Add Faculty\n")
    print("\t4 : Add Student\n")
    print("\t5 : Remove Faculty\n")
    print("\t6 : Remove Student\n")
    print("\t7 : Check if Student Belongs to Faculty\n")
    print("\t8 : Display Graduates\n")
    print("\t9 : Select all the faculties from a field\n")
    print("\t10 : Batch Enrollment\n")
    print("\t11 : Batch Graduation\n")
    print("\t0: Exit (be free and independent)\n")
    
def main():
    logging.basicConfig(filename='board.log', level=logging.INFO)
    logging.info("Starting the TUM temporary Board program.")

    print("Welcome to TUM temporary Board\n")
    
    faculties = load_data() 

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            display_faculties(faculties)
        elif choice == "2":
            display_students(faculties)
        elif choice == "3":
            faculties.append(add_faculty())
        elif choice == "4":
            add_student(faculties)
        elif choice == "5":
            remove_faculty(faculties)
        elif choice == "6":
            remove_student(faculties)
        elif choice == "7":
            check_student_belongs_to_faculty(faculties)
        elif choice == "8":
            display_graduates(faculties)
        elif choice == "9":
            select_all_from_field(faculties)
        elif choice == "10":
            batch_enrollment(faculties)
        elif choice == "11":
            batch_graduation(faculties)
        elif choice == "0":
            save_data(faculties) 
            print("Exiting program. Goodbye, you're free and independent!")
            logging.info("Exiting the TUM temporary Board program.")
            break
        else:
            logging.error("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
