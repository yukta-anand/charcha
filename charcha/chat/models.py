from django.db import models
from django.conf import settings

ADMIN = 1
MEMBER = 2
GUEST = 3

DIRECT_MESSAGE = 1
GROUP_DIRECT_MESSAGE = 2
PRIVATE_CHANNEL = 3
PUBLIC_CHANNEL = 4

class ChannelManager(models.Manager):
    def get_my_channels(self, user):
        pass

class Channel(models.Model):
    class Meta:
        db_table = 'channels'
    
    name = models.CharField(max_length=100)
    kind = models.IntegerField(choices = (
        (DIRECT_MESSAGE, 'Direct Message'),
        (GROUP_DIRECT_MESSAGE, 'Group Direct Message'),
        (PRIVATE_CHANNEL, 'Private Channel'),
        (PUBLIC_CHANNEL, 'Public Channel'),
    ))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def post_message(self, author, text):
        message = Message()
        message.channel = self
        message.text = text
        message.author = author
        message.save()
        
class ChannelMember(models.Model):
    class Meta:
        db_table = 'channel_members'

    channel = models.ForeignKey(Channel, on_delete=models.PROTECT, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    role = models.IntegerField(choices = (
            (ADMIN, 'Admin'),
            (MEMBER, 'Member'),
            (GUEST, 'Guest'),
        ))

class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT)
    text = models.TextField(max_length=8192)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    def reply(self, author, text):
        pass
