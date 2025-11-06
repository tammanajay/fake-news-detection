from django.db import models
from django.contrib.auth.models import User

class Viewer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=13, null=True)
    role = models.IntegerField(default=0)
    created_at = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} (Role: {self.role})"


class Article(models.Model):
    title = models.CharField(max_length=20000)
    content = models.TextField()
    is_fake = models.BooleanField(default=False)
    date_updated = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)
    date_published = models.DateField(null=True, blank=True)
    user = models.ForeignKey(Viewer, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title


class FakeDetection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='detections')
    is_fake = models.BooleanField(default=False)
    confidence = models.FloatField()
    model_version = models.CharField(max_length=50, default="1.0")

    def __str__(self):
        return f"{self.article.title} - Fake: {self.is_fake}"


class Admins(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='admin_actions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_actions')
    is_published = models.BooleanField()
    is_reported = models.BooleanField(default=False)
    updated_date = models.DateField(auto_now=True)
    description = models.CharField(null=True,max_length=50)

    def __str__(self):
        return f"Admin: {self.user.username} | Article: {self.article.title} | Published: {self.is_published}| Reported: {self.is_reported}|                   |Details: {self.description}"
