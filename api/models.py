from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        unique_together = ('first_name', 'last_name',)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class CaregiverLevel(models.Model):
    LEVEL_CHOICES = [
        (0, 'Level 0'),
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES, unique=True)
    wait_time = models.IntegerField(default=600)

    def __str__(self):
        return dict(self.LEVEL_CHOICES)[self.level]


class Caregiver(models.Model):
    elderly = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='elderly')
    caregiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='caregivers')
    level = models.ForeignKey(CaregiverLevel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('elderly', 'caregiver',)

    def __str__(self):
        return f'Caregiver: {self.caregiver} - Elderly: {self.elderly} - Level: {self.level}'


class Home(models.Model):
    home = models.CharField(max_length=50, primary_key=True)
    elderly = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Home: {self.home} - Elderly: {self.elderly}'


class SensorAlert(models.Model):
    subject = models.CharField(max_length=50)
    start = models.DateTimeField()
    location = models.CharField(max_length=50)
    state = models.DecimalField(max_digits=5, decimal_places=2)
    measurable = models.CharField(max_length=50)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.home}'


class Notification(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    sensor_alert = models.ForeignKey(SensorAlert, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    has_accepted = models.BooleanField(default=False)
