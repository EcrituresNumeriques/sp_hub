from django.contrib.auth import logout
from django.shortcuts import render, redirect
from sp_app import views, models

def logout_view(request):
    logout(request)
    return redirect('sp_app:list_articles')

def home_view(request):
    articles = models.Article.objects.all()
    conversations = models.Conversation.objects.all()

    return render(request, 'core/home.html',
        { 'articles': articles, 'conversations': conversations, }
    )
