from django.db import models
from django.utils import timezone


class Dine_query(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    desired_rating = models.IntegerField()
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()
    day = models.CharField(max_length=10)
    distance = models.FloatField()
    created_date = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return 'Dining-Parameters({}, {}, {}, {}, {}, {})'.format(self.name, self.price, self.desired_rating, self.opening_time, self.closing_time, self.distance)

    def __str__(self):
        return 'Dining-Parameters({}, {}, {}, {}, {}, {})'.format(self.name, self.price, self.desired_rating, self.opening_time, self.closing_time, self.distance)