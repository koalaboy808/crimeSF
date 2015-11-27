from django.db import models
from djgeojson.fields import PointField

# Create your models here.


class Dummy(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class LazySpot(models.Model):

    geom = PointField()
    description = models.TextField()
    #picture = models.ImageField()

    @property
    def popupContent(self):
      return '<img src="{}" /><p><{}</p>'.format(
          #self.picture.url,
          self.description)