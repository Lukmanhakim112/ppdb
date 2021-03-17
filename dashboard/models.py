from django.db import models
from django.utils import timezone

from users.models import CustomUser
from primaseru import choices


class StudentStatus(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    accepted = models.BooleanField('Diterima', db_index=True, null=True)
    major = models.CharField('Diterima dijurusan', choices=choices.MAJOR, max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} Status'
