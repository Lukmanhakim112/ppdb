from django.dispatch import receiver
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser

from primaseru.models import StudentProfile, FatherStudentProfile, MotherStudentProfile, StudentGuardianProfile, PhotoProfile, MajorStudent, StudentFile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(student=instance)
        FatherStudentProfile.objects.create(child=instance)
        MotherStudentProfile.objects.create(child=instance)
        StudentGuardianProfile.objects.create(child=instance)
        PhotoProfile.objects.create(student=instance)
        MajorStudent.objects.create(student=instance)
        StudentFile.objects.create(student=instance)
        print("Created Instance")

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.studentprofile.save()
    instance.fatherstudentprofile.save()
    instance.motherstudentprofile.save()
    instance.studentguardianprofile.save()
    instance.photoprofile.save()
    instance.majorstudent.save()
    instance.studentfile.save()
