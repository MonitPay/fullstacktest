from django.db import models


class Transaction(models.Model):

    category = models.CharField(max_length=100)
    amount = models.FloatField()

    created_at = models.DateTimeField()

    def __str__(self):
        return self.category
