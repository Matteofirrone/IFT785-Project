from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name}'


class CaregiverLevel(models.Model):
    level = models.IntegerField()

    def __str__(self):
        return f'{self.level}'


class Caregiver(models.Model):
    elderly = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='elderly')
    caregiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='caregivers')
    level = models.ForeignKey(CaregiverLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.level} - {self.caregiver}'


class SensorAlert(models.Model):
    subject = models.CharField(max_length=50)
    start = models.DateTimeField()
    location = models.CharField(max_length=50)
    state = models.DecimalField(max_digits=5, decimal_places=2)
    measurable = models.CharField(max_length=50)
    home = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.home}'
