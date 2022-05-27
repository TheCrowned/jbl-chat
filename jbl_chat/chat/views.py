from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404
from chat.models import Message, Conversation
from chat.serializers import MessageSerializer, UserSerializer
from django.contrib.auth.models import User

class ConversationDetail(APIView):
    """
    List all messages belonging to a conversation with a user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        """
        Display conversation messages.
        """

        # Participants: [current user, user by request username]
        participant1 = request.user
        try:
            participant2 = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        # Retrieve conversation between participants, or empty if non existent
        try:
            conversation = Conversation.objects.filter(
                participants__username=participant1.username).filter(
                participants__username=participant2.username).get()
            messages = conversation.message_set.all()
        except Conversation.DoesNotExist:
            messages = {}

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, username):
        """
        Handles creation of a new message.
        """

        serializer = MessageSerializer(
            data=request.data,
            context={'request': request, 'recipient': username}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


'''class MessageList(APIView):
    """
    List all messages regardless of conversation/user.
    Can be decommented, if the relevant line in urls.py is also decommented.
    Was useful for development early stages + some debugging.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
'''
