from django.db import models
from django.utils import timezone
# Create your models here.

class HashTag(models.Model):
    hashtag_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.hashtag_name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")
    contents = models.TextField()
    hashtag = models.ManyToManyField(HashTag)

    def __str__(self):
        return self.title

    def summary(self):
        return self.contents[:42]

class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=20)
    comment_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def approve(self):
        self.save()
        
    def __str__(self):
        return self.comment_text
