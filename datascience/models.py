from django.db import models


class DataUpload(models.Model):
    title = models.TextField(max_length=255)
    task = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title


