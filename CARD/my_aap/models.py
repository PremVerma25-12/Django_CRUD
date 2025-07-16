from django.db import models

class registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Query(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    query = models.TextField()