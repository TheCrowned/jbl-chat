from django.urls import path
from chat import views

urlpatterns = [
    #path('messages/', views.MessageList.as_view()),
    path('conversations/<str:username>/', views.ConversationDetail.as_view()),
    path('users/', views.UserList.as_view()),
]
