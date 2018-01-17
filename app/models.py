from django.db import models
import uuid
# Create your models here.
class Game(models.Model):
    gameid = models.UUIDField(default=uuid.uuid4, editable=False)
    rank = models.IntegerField()
