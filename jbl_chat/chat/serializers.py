from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class MessageSerializer(serializers.Serializer): 
    content = serializers.CharField(max_length=2000)
    sender = serializers.ReadOnlyField(source='sender.username') # model field is User
    sent = serializers.ReadOnlyField()

    def create(self, validated_data):
        sender_u = self.context['request'].user

        # Retrieve user by username
        try:
            recipient_u = User.objects.get(username=self.context['recipient'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'recipient': 'User does not exist.'})

        # Retrieve (or create) conversation between current user and recipient
        try:
            c = Conversation.objects.filter(
                participants__username=sender_u.username).filter(
                participants__username=recipient_u.username).get()
        except Conversation.DoesNotExist:
            c = Conversation()
            c.save() # need to register before setting its relationships
            c.participants.add(sender_u, recipient_u)
        
        return Message.objects.create(
            content=validated_data['content'],
            sender=sender_u,
            conversation=c)


