from django.core.management.base import BaseCommand
from main.models import *
import random
from faker import Faker
from itertools import islice

f = Faker()

batchSize = 60


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--users', nargs='+', type=int)
        parser.add_argument('--questions', nargs='+', type=int)
        parser.add_argument('--answers', nargs='+', type=int)
        parser.add_argument('--tags', nargs='+', type=int)
        parser.add_argument('--likes', nargs='+', type=int)

    def handle(self, *args, **options):
        if options['users']:
            self.fillUsers(options['users'][0])
        else:
            self.fillUsers(10)
        print('users created')

        if options['tags']:
            self.fillTags(options['tags'][0])
        else:
            self.fillTags(10)
        print('tags created')

        if options['questions']:
            self.fillQuestions(options['questions'][0])
        else:
            self.fillQuestions(40)
        print('questions created')

        if options['answers']:
            self.fillAnswers(options['answers'][0])
        else:
            self.fillAnswers(50)
        print('answers created')

        if options['likes']:
            self.fillLikes(options['likes'][0])
        else:
            self.fillLikes(50)
        print('likes created')

    def fillTags(self, n):
        tags = (Tag(
            title=f.word()
        ) for i in range(n))

        while True:
            batch = list(islice(tags, batchSize))

            if not batch:
                break
            Tag.objects.bulk_create(batch, batchSize)

    def fillUsers(self, n):
        profilesExisted = User.objects.all().last()
        if profilesExisted is None:
            lastId = 0
        else:
            lastId = profilesExisted.id

        for i in range(n):
            im = f.random_int(min=1, max=6)
            profiles = User.objects.create_user(
             f.name() + str(i), f.user_name() + str(i))
            profiles.id=lastId + 1 + i

    def fillQuestions(self, n):
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        questions = (Question(
            author=User.objects.all().get(id=random.choice(author_ids)),
            title=f.sentence()[:128],
            text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            rating=f.random_int(min=2, max=5)
        ) for i in range(n))

        while True:
            batch = list(islice(questions, batchSize))
            if not batch:
                break
            Question.objects.bulk_create(batch, batchSize)

        tags = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )

        questions = Question.objects.all()

        for question in questions:
            for i in range(f.random_int(min=2, max=5)):
                question.tags.add(random.choice(tags))


    def fillAnswers(self, n):
        author_ids = list(
            User.objects.values_list(
                'id', flat=True
            )
        )

        questionIds = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )

        answers = (Answer(
            author=User.objects.all().get(id=random.choice(author_ids)),
            question=Question.objects.all().get(id=random.choice(questionIds)),
            text='. '.join(f.sentences(f.random_int(min=2, max=5))),
            rating=f.random_int(min=2, max=5)
        ) for i in range(n))

        while True:
            batch = list(islice(answers, batchSize))
            if not batch:
                break
            Answer.objects.bulk_create(batch, batchSize)

    def fillLikes(self, n):
        user = User.objects.all()
        for question in Question.objects.all():
            for i in range(random.randint(1, 5)):
                like = Like()
                like.vote = 1
                like.user = random.choice(user)
                like.content_object = question
                like.save()
            question.save()

        for answer in Answer.objects.all():
            for i in range(random.randint(1, 5)):
                like = Like()
                like.vote = 1
                like.user = random.choice(user)
                like.content_object = answer
                like.save()
            answer.save()
