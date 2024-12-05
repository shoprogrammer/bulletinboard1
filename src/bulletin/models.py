from typing import Any
from django.db import models
from django.contrib.auth.models import User

#一段階目
class BoardModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    place = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='boards',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#二段階目
class Comment(models.Model):
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    

#三段階目
class Reaction(models.Model):
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE,related_name="reactions")
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="reactions")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reactions")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content



    
    
class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','board')
       
        

    
    




class Contact(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)