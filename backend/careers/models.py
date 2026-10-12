from django.db import models


class CareerPath(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CareerSkill(models.Model):
    career = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=40)
    weight = models.PositiveSmallIntegerField(default=1, help_text='Importance 1-5')

    def __str__(self):
        return f'{self.career} - {self.skill} ({self.weight})'
