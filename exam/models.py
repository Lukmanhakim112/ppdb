from django.db import models

from PIL import Image

from users.models import CustomUser

# TODO Create models for exam app
# 1. Exam Model
# 2. Question Model
# 3. Answer Model
# 4. Record Model
# 5. Score Model
# enough?

def question_directory_path(instance, filename):
    return f'question_pic/{instance.exam}/{filename}'

def answer_directory_path(instance, filename):
    return f'answer_pic/{instance.question.exam}/{filename}'


class Exam(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam_title = models.CharField('Judul Ujian', max_length=100)
    passcode = models.CharField('Passcode', max_length=20)

    def __str__(self):
        return self.exam_title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.CharField('Pertanyaan', max_length=120)
    question_image = models.ImageField('Gambar Pertanyaan', upload_to=question_directory_path, null=True, blank=True)

    def __str__(self):
        return f'{self.exam} - {self.question_text}'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField('Jawaban', max_length=120)
    answer_image = models.ImageField('Gambar Jawaban', upload_to=answer_directory_path, null=True, blank=True)
    is_right = models.BooleanField('Benar', default=False)

    def __str__(self):
        return self.answer_text

class Record(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Record {self.student} - {self.exam}'

class Score(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    score = models.IntegerField('Score', null=True)
    persentage = models.IntegerField('Persentase', null=True)

    def __str__(self):
        return f'Score {self.student}'
