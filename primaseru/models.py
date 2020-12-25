from django.db import models

from PIL import Image

from users.models import CustomUser
from . import choices


class PhotoProfile(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField('Photo', default='default_photo.png', upload_to='profile_pics')

    def __str__(self):
        return f'Photo {self.student}'

    def save(self, *args, **kwargs):
        super(PhotoProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)


class StudentProfile(models.Model):
    # Personal Information
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    no_regis = models.PositiveIntegerField('No. Pendaftaran', help_text="Bisa Konfirmasi Ke Bagian Pendaftaran, Contoh : 221321", unique=True, null=True)
    sex = models.CharField('Jenis Kelamin', max_length=1, choices=choices.SEX)
    religion = models.CharField('Agama', choices=choices.RELIGION, max_length=3)
    handpone = models.PositiveIntegerField('No. HP', null=True)
    city_born = models.CharField('Tempat Lahir', max_length=100, help_text="Contoh: Kabupaten Bandung")
    date_born = models.DateField('Tanggal Lahir', null=True)
    social_media = models.CharField('Akun Sosial Media', max_length=100)
    achievement = models.CharField('Prestasi Akademik/Non Akademik', max_length=120, null=True, blank=True)
    transport = models.CharField('Alat Transportasi', max_length=50)

    # Documents Information
    nisn = models.PositiveIntegerField('NISN', unique=True, null=True)
    nik = models.PositiveIntegerField('Nomor Induk Kependudukan (NIK)', unique=True, null=True)
    no_kk = models.PositiveIntegerField('Nomor Kartu Keluarga (KK)', null=True)
    address_kk = models.TextField('Alamat KK', null=True)

    # Address
    city = models.CharField('Kota/Kabupaten', max_length=120, help_text="Contoh: Kabupaten Bandung")
    kecamatan = models.CharField(max_length=120)
    kelurahan = models.CharField(max_length=120)
    dusun = models.CharField(max_length=120)
    rt_rw = models.CharField('RT/RW', max_length=8)
    real_address = models.TextField('Alamat Sekarang')
    resident = models.CharField('Tempat Tinggal', max_length=50)

    # Previous School Information
    school_origin = models.CharField('Asal Sekolah', max_length=120)
    npsn_school_origin = models.PositiveIntegerField('Nomor NPSN Sekolah Asal', help_text="Bisa Cek <a href='https://referensi.data.kemdikbud.go.id/index11.php' target='_blank'><b>Disini</b></a>", null=True)

    # Medical Record
    medic_record = models.TextField('Riwayat Kesehatan', null=True, blank=True)
    blood_type = models.CharField('Golongan Darah', choices=choices.BLOOD_TYPE, max_length=2)
    in_medicine = models.CharField('Dalam Pengobatan', max_length=120, null=True, blank=True)
    private_doctor = models.CharField('Nama Dokter Keluarga', max_length=120, null=True, blank=True)
    phone_doctor = models.PositiveIntegerField('No Telepon Dokter', null=True, blank=True)

    def __str__(self):
        return f'{self.student} profile'

class ProfileParent(models.Model):
    """
    Creating abstract models, so this models (field) can be use multiple time (inheritance).
    https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
    """
    child = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=f"Nama Lengkap", max_length=120)
    city_born = models.CharField('Kota/Kabupaten Kelahiran', max_length=120, help_text="Contoh: Kabupaten Bandung")
    date_born = models.DateField('Tanggal Lahir', null=True)
    nik = models.PositiveIntegerField('Nomor Induk Kependudukan (NIK)', null=True)
    education = models.CharField(f'Pendidikan Terakhir', max_length=4, choices=choices.EDUCATION_LEVEL)
    job = models.CharField(f'Pekerjaan', max_length=100, null=True, blank=True)
    salary = models.PositiveIntegerField(f'Penghasilan', null=True, blank=True)
    email = models.EmailField(f'Email', null=True, blank=True)
    phone = models.PositiveIntegerField(f'No. HP', null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True

class FatherStudentProfile(ProfileParent):
    pass

class MotherStudentProfile(ProfileParent):
    pass

class StudentGuardianProfile(ProfileParent):
    pass

class MajorStudent(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_major = models.CharField('Pilihan Jurusan Pertama', choices=choices.MAJOR, max_length=4)
    second_major = models.CharField('Pilihan Jurusan Kedua', choices=choices.MAJOR, max_length=4)
    info = models.CharField('Info Primaseru (PPDB)', max_length=120, help_text="Tuliskan Darimana Kamu Mendapatkan Info Tentang Primaseru.")

    def __str__(self):
        return f'{self.student} - {self.first_major}'

