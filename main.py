class Student: #Студенты
    Student_list = []
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = [] #Завершенные курсы
        self.courses_in_progress = [] #Текущие курсы
        self.grades = {} #Оценки
        self.gpa = 0 #средняя оценка
        Student.Student_list.append(self)
    def rate_th(self, Lect, course, grade): #Оценка лекторов
        if type(Lect) == Lecturer:
            if course in self.courses_in_progress:
                if course in Lect.courses_attached:
                    if course in Lect.grades:
                        Lect.grades[course] += [grade]
                    else:
                        Lect.grades[course] = [grade]
                    Lect.gpa_calculation()
                else:
                    return 'Преподаватель не закреплен на данный курс'
            else:
                return 'Данный курс отсутствует у студента'
        else:
            'Данный ментор не является лектором'

    def gpa_calculation(self):
        self.gpa = 0
        grade_list = []
        if len(self.grades) > 0:
            for C in self.grades.values():
                grade_list += C
            self.gpa = sum(grade_list) / len(grade_list)

    def __str__(self):
        pr = f'''Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашние задания: {round(self.gpa, 1)}
Курсы в процессе обучения: {', '.join(self.courses_in_progress)}
Завершенные курсы: {', '.join(self.finished_courses)}'''
        return pr
    def __eq__(self, other):
        return self.gpa == other.gpa
    def __lt__(self, other):
        return self.gpa < other.gpa
    def __le__(self, other):
        return self.gpa <= other.gpa

class Mentor: #Менторы (базовый класс)
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = [] #Закреплены на курсы
    def __str__(self):
        pr = f'''Имя: {self.name}
Фамилия: {self.surname}'''
        return pr

class Lecturer(Mentor): #лекторы
    Lecturer_list = []
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)
        self.grades = {} #Оценки лекторов по их курсам
        self.gpa = 0
        Lecturer.Lecturer_list.append(self)
    def gpa_calculation(self):
        self.gpa = 0
        grade_list = []
        if len(self.grades) > 0:
            for C in self.grades.values():
                grade_list += C
            self.gpa = sum(grade_list) / len(grade_list)

    def __str__(self):
        pr = f'''Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лекции: {self.gpa}'''
        return pr

    def __eq__(self, other):
        return self.gpa == other.gpa
    def __lt__(self, other):
        return self.gpa < other.gpa
    def __le__(self, other):
        return self.gpa <= other.gpa

class Reviewer(Mentor): #эксперты, проверяющие домашние задания
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)
    def rate_hw(self, student, course, grade): #функция для оценки домашних заданий студентов
        if (isinstance(student, Student)) and (course in self.courses_attached) and (course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            student.gpa_calculation()
        else:
            return 'Ошибка'
    def __str__(self):
            pr = f'''Имя: {self.name}
Фамилия: {self.surname}'''
            return pr

def course_Student_gpa(SL, course): #Подсчёт средней оценки за дз по всем студентам в рамках конкретного курса
    grade_list = []
    for s in SL:
        if course in s.grades:
            grade_list += s.grades[course]
    return round(sum(grade_list) / len(grade_list), 1)

S1 = Student('Ruoy', 'Eman', 'male')
S1.courses_in_progress += ['Python']
S1.courses_in_progress += ['Git']
S1.finished_courses += ['Введение в программирование']

S2 = Student('Barbara', 'Nimia', 'female')
S2.courses_in_progress += ['Git']


R1 = Reviewer('Some', 'Buddy')
R1.courses_attached += ['Python']

R2 = Reviewer('Inna', 'Shapovalova')
R2.courses_attached += ['Git']

L1 = Lecturer('Lect1', 'GDza')
L1.courses_attached += ['Python']

L2 = Lecturer('Vasiliy', 'Svistopliasov')
L2.courses_attached += ['Git']

R1.rate_hw(S1, 'Python', 8)
R1.rate_hw(S1, 'Python', 10)
R1.rate_hw(S1, 'Python', 10)

R2.rate_hw(S1, 'Git', 9)
R2.rate_hw(S1, 'Git', 6)

R2.rate_hw(S2, 'Git', 8)
R2.rate_hw(S2, 'Git', 9)
R2.rate_hw(S2, 'Git', 7)
R2.rate_hw(S2, 'Git', 8)

S1.rate_th(L1, 'Python', 9)
S1.rate_th(L1, 'Python', 10)

S1.rate_th(L2, 'Git', 10)
S1.rate_th(L2, 'Git', 9)

S2.rate_th(L2, 'Git', 8)
S2.rate_th(L2, 'Git', 9)

print(course_Student_gpa(Student.Student_list, 'Git'))
print(course_Student_gpa(Lecturer.Lecturer_list, 'Git'))