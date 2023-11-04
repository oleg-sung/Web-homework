from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)
    image = models.ImageField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    release_date = models.DateTimeField()
    lte_exists = models.BooleanField(default=True)
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return f'Phone - {self.slug}'
