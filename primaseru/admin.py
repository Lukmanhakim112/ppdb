from django.contrib import admin

from .models import StudentProfile, FatherStudentProfile, MotherStudentProfile, StudentGuardianProfile, MajorStudent, PhotoProfile, StudentFile, RegisterSchedule

admin.site.register(StudentProfile)
admin.site.register(FatherStudentProfile)
admin.site.register(MotherStudentProfile)
admin.site.register(StudentGuardianProfile)
admin.site.register(MajorStudent)
admin.site.register(PhotoProfile)
admin.site.register(StudentFile)
admin.site.register(RegisterSchedule)
