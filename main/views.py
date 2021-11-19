import json
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *


def fill_errors(form_errors, errors):
    for i in form_errors:
        formatted_field_name = i.replace('_', ' ')
        errors.append(f' { formatted_field_name } field error: {form_errors[i][0]}')


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return page_obj


@login_required(login_url='/login/')
def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'profile.html', {'profile': user})
    else:
        raise Http404


def index(request):
    return render(request, 'base.html',
                  {'page': paginate(Question.objects.newest(), request),
                   'profile': profile,
                   'popular_members': User.objects.get_top_users()[0:10],
                   'popular_tags': Tag.objects.get_top_tags()[0:10]})


def hot(request):
    questions = Question.objects.hottest()
    return render(request, 'hot.html',
                  {'page': paginate(questions, request),
                   'profile': profile,
                   'popular_members': User.objects.get_top_users()[0:10],
                   'popular_tags': Tag.objects.get_top_tags()[0:10]})


def signup(request):
    errors = []
    form = UserSignUpForm
    if request.method == 'POST':
        form = form(request.POST)
        if request.POST['password'] != request.POST['password_confirmation']:
            errors.append('Passwords don\'t match')
        elif form.is_valid():
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'],
                                            first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'])
            user.set_password(request.POST['password_confirmation'])
            user.save()
            auth_login(request, user)
            return redirect('/')
        else:
            fill_errors(form.errors, errors)
    else:
        auth_logout(request)

    return render(request, 'signup.html', {'form': form, 'messages': errors,
                                           'popular_members': User.objects.get_top_users()[0:10],
                                           'popular_tags': Tag.objects.get_top_tags()[0:10],
                                           })


def answer_status_change(request):
    c_user = request.user
    a_id = request.POST.get('val')
    status = request.POST.get('stat')
    cur_answer = Answer.objects.get(id=a_id)
    if cur_answer.status:
        cur_answer.status = False
        cur_answer.save()
        return HttpResponse(json.dumps({'status': 'ok', 'score': False}), content_type='application/json')
    else:
        cur_answer.status = True
        cur_answer.save()
        return HttpResponse(json.dumps({'status': 'ok', 'score': True}), content_type='application/json')


def login(request):
    errors = []
    form = UserSignInForm
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(request.GET.get('next') if request.GET.get('next') != '' else '/')
        else:
            errors.append('Invalid username or password')

        auth_logout(request)
    return render(request, 'login.html', {'popular_members': User.objects.get_top_users()[0:10],
                                          'popular_tags': Tag.objects.get_top_tags()[0:10], 'form': form,
                                          'messages': errors})


def logout(request):
    if not request.user.is_authenticated:
        raise Http404
    auth_logout(request)
    return redirect(request.GET['from'])


@login_required(login_url='/login/')
def ask(request):
    errors = []
    form = NewQuestionForm
    if request.method == 'POST':
        form = form(request.POST)

        if form.is_valid():
            new_question = Question.objects.create(author=request.user,
                                                   date=timezone.now(),
                                                   is_active=True,
                                                   title=request.POST['title'],
                                                   text=request.POST['text'])
            new_question.save()
            for tagTitle in request.POST['tags'].split():
                tag_n = Tag.objects.get_or_create(title=tagTitle)[0]
                new_question.tags.add(tag_n)
                new_question.save()
            return question(request, new_question.id, 1)
        else:
            fill_errors(form.errors, errors)

    return render(request, 'ask.html', {'form': form, 'messages': errors,
                                        'popular_members': User.objects.get_top_users()[0:10],
                                        'popular_tags': Tag.objects.get_top_tags()[0:10],
                                        })


@login_required(login_url='/login/')
def settings(request):
    errors = []
    form = UserSettingsForm
    if request.method == 'POST':
        form = form(data=request.POST,
                    files=request.FILES)
        if form.is_valid():
            for changedField in form.changed_data:
                if changedField == 'avatar':
                    setattr(request.user, changedField, request.FILES[changedField])
                else:
                    setattr(request.user, changedField, request.POST[changedField])
            request.user.save()
            return redirect('/settings/')
        else:
            fill_errors(form.errors, errors)
    else:
        for i in form.base_fields:
            form.base_fields[i].widget.attrs['placeholder'] = getattr(request.user, i)
    return render(request, 'settings.html', {'form': form, 'messages': errors,
                                             'popular_members': User.objects.get_top_users()[0:10],
                                             'popular_tags': Tag.objects.get_top_tags()[0:10],
                                             })


def question(request, pk, new=0):
    curr_question = Question.objects.by_id(int(pk)).first()
    if curr_question is not None:
        answers = curr_question.answers.hottest()
    else:
        raise Http404

    if (curr_question and answers) is not None:
        errors = []
        form = WriteAnswerForm
        if Question.objects.filter(id=pk).exists():
            if request.method == 'POST' and new == 0:
                form = form(request.POST)
                if form.is_valid():
                    answered_question = Question.objects.by_id(pk)[0]
                    new_answer = Answer.objects.create(author=request.user,
                                                       date=timezone.now(),
                                                       text=request.POST['text'],
                                                       question_id=answered_question.id)
                    new_answer.save()
                    pages = Paginator(answers, 10)
                    return redirect(f'/question/{pk}/?page={pages.num_pages}#{new_answer.id}')
                else:
                    fill_errors(form.errors, errors)

            return render(request, 'question.html',
                          {'page': paginate(answers, request),
                           'main': curr_question,
                           'profile': profile,
                           'popular_members': User.objects.get_top_users()[0:10],
                           'popular_tags': Tag.objects.get_top_tags()[0:10],
                           'form': form})
    else:
        raise Http404


def tag(request, tag_name):
    by_tag_sorted_questions = []
    # sort questions by tag
    for question in Question.objects.all():
        for tag in question.tags.all():
            if tag.title == tag_name:
                by_tag_sorted_questions.append(question)
    return render(request, 'tag_index.html',
                  {'page': paginate(by_tag_sorted_questions, request),
                   'profile': profile,
                   'tag_name': tag_name,
                   'popular_members': User.objects.get_top_users()[0:10],
                   'popular_tags': Tag.objects.get_top_tags()[0:10]})


class VotesView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            like_dislike = Like.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                            object_id=obj.id,
                                            user=request.user)

            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                obj.rate += 2*self.vote_type
                obj.author.rank += 2*self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            else:
                obj.rate -= self.vote_type
                like_dislike.delete()
                result = False
        except Like.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            obj.rate += self.vote_type
            obj.author.rank += self.vote_type
            result = True

        obj.save()
        obj.author.save()
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )














