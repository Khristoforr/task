from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    file_name = models.CharField(max_length=100)
    file_size = models.DecimalField(decimal_places=2, max_digits=5)
    file_type = models.CharField(max_length=150)
    uploaded_at = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, verbose_name='Владелец файла', on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['file_name', 'owner'], name='unique_filename_for_user'),
        ]

    def __str__(self):
        return self.file_name
