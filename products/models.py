from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)  # Hundredths of currency

    def __str__(self):
        return self.name