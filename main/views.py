from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    content = paginate(request, questions)
    return render(request, 'main/index.html', {'questions': content})


def ask(request):
    return render(request, 'main/ask.html')


def login(request):
    return render(request, 'main/login.html')


def profile(request):
    return render(request, 'main/profile.html')


def question(request):
    content = paginate(request, anw_block)
    return render(request, 'main/question.html', {'anw_block': content})


def signup(request):
    return render(request, 'main/signup.html')


def tags(request):
    content = paginate(request, questions)
    return render(request, 'main/tags.html', {'questions': content})


def paginate(request, objects_list, per_page=5):
  paginator = Paginator(objects_list, per_page)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return page_obj


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







