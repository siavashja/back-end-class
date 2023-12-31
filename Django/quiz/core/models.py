from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    age = models.PositiveIntegerField(default = 0)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Course(models.Model):

    title = models.CharField(max_length = 255)
    description = models.TextField()
    presenter = models.ForeignKey(UserProfile, related_name = "presented_classes", on_delete = models.CASCADE)

class UCM(models.Model):

    user = models.ForeignKey(UserProfile, related_name = "ucms", on_delete = models.CASCADE)
    course = models.ForeignKey(Course, related_name ="ucms", on_delete = models.CASCADE)


class QuestionCategory(models.Model):

    title = models.CharField(max_length = 255)
    description = models.TextField()

class Question(models.Model):

    difficulty_enum = (
        ("H", "Hard"),
        ("M", "medium"),
        ("E", "easy")
    )

    question_type_enum = (
        ("T", "Test"),
        ("D", "Desctiptive")
    )

    category = models.ForeignKey(QuestionCategory, related_name = "questions", on_delete = models.CASCADE)
    difficulty = models.CharField(max_length = 1, choices = difficulty_enum,
                                    default = "M")
    question_type = models.CharField(max_length = 1, choices = question_type_enum,
                                    default = "T")
    title = models.CharField(max_length = 255)
    test1 = models.CharField(max_length = 255, null = True, blank = True)
    test2 = models.CharField(max_length = 255, null = True, blank = True)
    test3 = models.CharField(max_length = 255, null = True, blank = True)
    test4 = models.CharField(max_length = 255, null = True, blank = True)
    answer = models.IntegerField(default = 1, null = True, blank = True)
    
    
class Quiz(models.Model):

    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    grade = models.IntegerField(default = 0)
    questions = models.ManyToManyField(Question, related_name= "quizes")