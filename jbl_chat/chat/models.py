from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def get_sentinel_user():
    """
    Retrieves or creates a fake user to associate messages to, when
    a user is deleted.
    """
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Conversation(models.Model):
    participants = models.ManyToManyField('auth.User',
                                          related_name='participants')


class Message(models.Model):
    content = models.CharField(max_length=2000)
    sender = models.ForeignKey('auth.User',
                               on_delete=models.SET(get_sentinel_user))
    conversation = models.ForeignKey('Conversation',
                                     on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[{time}] {user} | {msg}'.format(
            time=self.sent.strftime('%x %X'),
            user=self.sender.username,
            msg=self.content)
            
    class Meta:
        ordering = ['sent']

