from django.db import models

# Create your models here.
from django.db import models



class Training(models.Model):
    TRAINING_TYPE_CHOICES = [
        ('ইন-হাউজ/অভ্যন্তরীণ', 'ইন-হাউজ/অভ্যন্তরীণ'),
        ('স্থানীয়', 'স্থানীয়'),
        ('বৈদেশিক', 'বৈদেশিক'),
    ]

    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255, default='Unknown')
    training_type = models.CharField(
        max_length=50,
        choices=TRAINING_TYPE_CHOICES,
        default='ইন-হাউজ/অভ্যন্তরীণ'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Batch(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='batches')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    fiscal_year = models.CharField(max_length=10, null=True, blank=True)
    batch_number = models.IntegerField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_training_hours = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.training.title} - Batch {self.batch_number}"

'''
class Batch(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='batches')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    fiscal_year = models.CharField(max_length=10, null=True, blank=True)
    batch_number = models.IntegerField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_training_hours = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.training.title} - Batch {self.batch_number}"
'''

'''
class Batch(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='batches')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    fiscal_year = models.CharField(max_length=10, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_training_hours = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch #{self.id} for {self.training.title}"


=========================
python manage.py makemigrations dashboard
python manage.py migrate

'''
class Participant(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    office_address = models.TextField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    batch_number = models.IntegerField()
    Official_ID = models.CharField(max_length=255)
    total_training_hours = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.designation})"


class FinancialClearance(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    advance_receiver = models.CharField(max_length=255)
    adjustment_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.training.title} - Batch {self.batch.batch_number}"



from django.db import models

class Attachment(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class Attachment(models.Model):
#     training = models.ForeignKey(Training, on_delete=models.CASCADE)
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     file_path = models.FileField(upload_to='attachments/')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.title} (Batch {self.batch.batch_number})"


