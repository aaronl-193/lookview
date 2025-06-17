from django.shortcuts import render, HttpResponse

from django import http

from films.models import Film
from .models import SiteUserComment

def forum_view(
    request: http.HttpRequest,
) -> HttpResponse:
    if request.method == "POST":
        SiteUserComment.objects.create_comment(
            request.user.site_user,
            Film.objects.get(id=request.POST.get("film")),
            request.POST.get("chat-input"),
        )
    films: models.QuerySet = Film.objects.all()
    context: dict = {}
    context["films"] = []
    for film in films:
        chats: models.QuerySet = SiteUserComment.objects.filter(target=film).order_by('comment_created')
        context["films"].append((film, chats))
    return render(request, "discussion.html", context)
