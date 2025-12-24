from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
# Create your models here.
    def save(self, *args, **kwargs):
        if not self.id:
            # Get the maximum ID and add 1
            max_id = User.objects.all().aggregate(models.Max('id'))['id__max']
            self.id = 1 if max_id is None else max_id + 1
        super().save(*args, **kwargs)
