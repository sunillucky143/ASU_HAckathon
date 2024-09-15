import uuid
from django.db import models

# Create your models here.
class Post(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    procedure = models.CharField(max_length=50000)
    s_p = models.CharField(max_length=10000) #saftey protocols
    l_a_r = models.CharField(max_length=10000) #Laws and regulations
    created_at = models.DateTimeField(auto_now_add=True)
    access = models.CharField(max_length=10)


class Comments(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    comment = models.TextField()
    risk_factor = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment



