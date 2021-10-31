from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, 'main/index.html', {'questions': content})


def ask(request):
    return render(request, 'main/ask.html')


def login(request):
    return render(request, 'main/login.html')


def profile(request):
    return render(request, 'main/profile.html')


def question(request):
    paginator = Paginator(anw_block, 3)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, 'main/question.html', {'anw_block': content})


def signup(request):
    return render(request, 'main/signup.html')


def tags(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, 'main/tags.html', {'questions': content})


anw_block = [
    {
        "title": f"Title {i}",
        "text": f"Some answer for question."
    } for i in range(30)
]

questions = [
    {
        "title": f"Question {j}",
        "text": f"Some text for question {j}"
    } for j in range(100)
]







