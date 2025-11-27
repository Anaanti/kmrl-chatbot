# api/models.py
from django.db import models
from django.contrib.auth.models import User  # if you want to log user

class UnansweredQuery(models.Model):
    query_text = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    context = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.query_text
