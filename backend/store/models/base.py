import os
import uuid
from django.utils import timezone

# 상수 정의
GRADE_CHOICES = [
    ("Kindergarten", "Kindergarten"),
    ("USA grade 1", "USA grade 1"),
    ("USA grade 2", "USA grade 2"),
    ("USA grade 3", "USA grade 3"),
    ("USA grade 4", "USA grade 4"),
    ("USA grade 5", "USA grade 5"),
    ("USA grade 6", "USA grade 6"),
    ("USA grade 7", "USA grade 7"),
    ("USA grade 8", "USA grade 8"),
    ("Algebra 1", "Algebra 1"),
    ("Geometry", "Geometry"),
    ("Algebra 2", "Algebra 2"),
    ("Trigonometry", "Trigonometry"),
    ("Precalculus", "Precalculus"),
    ("High school statistics", "High school statistics"),
    ("Statistics and probability", "Statistics and probability"),
    ("Linear algebra", "Linear algebra"),
    ("Differential equations", "Differential equations"),
    ("Multivariable calculus", "Multivariable calculus"),
    ("AP Calculus BC", "AP Calculus BC"),
    ("AP Calculus AB", "AP Calculus AB"),
    ("AP Statistics", "AP Statistics"),
]

DIFFICULTY_CHOICES = [
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
]

TYPE_CHOICES = [
    ("Multiple Choice", "Multiple Choice"),
    ("Short Answer", "Short Answer"),
    ("Mathematical Modeling", "Mathematical Modeling"),
    ("Learning Through Discussion", "Learning Through Discussion"),
    ("STEAM", "STEAM"),
    ("Math Puzzle", "Math Puzzle"),
    ("Math for Literacy", "Math for Literacy"),
    ("Physics", "Physics"),
    ("Chemistry", "Chemistry"),
    ("Biology", "Biology"),
    ("E.S.S", "E.S.S"),
    ("Sentence Completion", "Sentence Completion"),
    ("Text Completion", "Text Completion"),
    ("Reading Comprehension", "Reading Comprehension"),
    ("Homeschooling", "Homeschooling"),
    ("School Classes", "School Classes"),
    ("Math", "Math"),
    ("English", "English"),
]

SUBJECT_CHOICES = [
    ("Math", "Math"),
    ("Science", "Science"),
    ("Liberal Arts", "Liberal Arts"),
    ("English", "English"),
    ("STEM", "STEM"),
    ("SAT", "SAT"),
]

PROBLEM_TYPE = [("Normal", "Normal"), ("Premium", "Premium"), ("Best", "Best")]


# 공통 함수 정의
def get_image_upload_path(instance, filename):
    now = timezone.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return os.path.join("pre_image", year, month, day, filename)


def get_file_upload_path(instance, filename):
    now = timezone.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    folder = f"{uuid.uuid4().hex[:16]}"
    return os.path.join("uploads", year, month, day, folder, filename)
