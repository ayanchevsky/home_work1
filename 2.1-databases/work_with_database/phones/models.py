from django.db import models


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.TextField(max_length=200)
    price = models.FloatField()
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=100)

