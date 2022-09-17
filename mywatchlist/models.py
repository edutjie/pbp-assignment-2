from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MyWatchList(models.Model):
    watched = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    release_date = models.DateField()
    review = models.TextField()
