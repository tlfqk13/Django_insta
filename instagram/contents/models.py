import os
import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Content(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')

    class Meta:
        ordering = ['-created_at'] # 최신순으로 피드 배치
        verbose_name_plural = "컨텐츠"


def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))
    #16자리 고유한 아이디 생성


class Image(BaseModel):
    UPLOAD_PATH = 'user-upload'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField() # image numbering

    class Meta:
        unique_together = ['content', 'order']
        ordering = ['order'] # 오름차순 정렬 -order==내림차순


class FollowRelation(BaseModel):
    follower = models.OneToOneField(User, on_delete=models.CASCADE)
    followee = models.ManyToManyField(User, related_name='followee')

"""
Follower        Followee
A,B             C,D
B,C             Z   

----------------------------------
ONE TO ONE 
B               A,Z,C,D....
C               B,D,F,G....

"""
