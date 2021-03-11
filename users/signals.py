from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.sessions.models import Session
from .models import CustomUser


from primaseru.models import StudentProfile, FatherStudentProfile, MotherStudentProfile, StudentGuardianProfile, PhotoProfile, MajorStudent, StudentFile
from dashboard import models as dashboard_model

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_staff:
            # TODO refactor me, pls.... I beg you.....
            StudentProfile.objects.create(student=instance)
            FatherStudentProfile.objects.create(student=instance)
            MotherStudentProfile.objects.create(student=instance)
            StudentGuardianProfile.objects.create(student=instance)
            PhotoProfile.objects.create(student=instance)
            MajorStudent.objects.create(student=instance)
            StudentFile.objects.create(student=instance)
            dashboard_model.StudentStatus.objects.create(student=instance)
            print("Created Instance")

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    # TODO same with above me....
    if not instance.is_staff:
        instance.studentprofile.save()
        instance.fatherstudentprofile.save()
        instance.motherstudentprofile.save()
        instance.studentguardianprofile.save()
        instance.photoprofile.save()
        instance.majorstudent.save()
        instance.studentfile.save()
        instance.studentstatus.save()
        print("Instance Saved")


@receiver(pre_delete, sender=Session)
def house_keeping(sender, instance, **kwargs):
    pass
