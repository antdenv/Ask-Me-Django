from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum
from django.contrib.auth.models import UserManager as AbstractUserManager


class UserManager(AbstractUserManager):
    def get_top_users(self):
        return self.order_by("-rating")


class QuestionManager(models.Manager):
    def hottest(self):
        return self.all().order_by('rating').reverse()

    def newest(self):
        return self.all().order_by('date').reverse()

    def by_id(self, qid):
        return self.all().filter(id=qid)


class AnswerManager(models.Manager):
    def hottest(self):
        return self.all().order_by('rating').reverse()


class TagManager(models.Manager):
    def get_top_tags(self):
        return self.order_by("-rating")


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class User(AbstractUser):
    avatar = models.ImageField(default="static/main/img/avatar.jpg", upload_to='static/main/upload/')
    rating = models.IntegerField(default=0, verbose_name='User rating')
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Tag(models.Model):
    title = models.CharField(max_length=50, default='404', verbose_name='Tag', unique=True)
    rating = models.IntegerField(default=0)
    objects = TagManager()

    def get_rating(self):
        res = Question.objects.filter(tags=self.title).count()
        self.rating = res
        self.save(update_fields=["rating"])
        return res

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1
    TYPES = ((LIKE, 1), (DISLIKE, -1))

    user = models.ForeignKey(User, null=True, verbose_name='User like', on_delete=models.CASCADE)
    vote = models.SmallIntegerField(verbose_name='like', default=TYPES[0], choices=TYPES)
    content_type = models.ForeignKey(ContentType, default=None, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=-1)
    content_object = GenericForeignKey()
    objects = LikeManager()

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return self.user.username


class Question(models.Model):
    author = models.ForeignKey(User, null=False, verbose_name='Question author', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name='Question date create')
    is_active = models.BooleanField(default=True, verbose_name='Question active')
    title = models.CharField(max_length=255, verbose_name='Title')
    text = models.TextField(verbose_name='Question text')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True, verbose_name='Tags')
    votes = GenericRelation(Like, related_query_name='questions')
    rating = models.IntegerField(default=0, null=False, verbose_name='Rating')
    type = 'question'
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(User, null=False, verbose_name='Answer author', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name='Answer date create')
    question = models.ForeignKey(Question, related_name='answers', verbose_name='Answered question',
                                 on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Answer text')
    status = models.BooleanField(verbose_name='Status', default=False)
    votes = GenericRelation(Like, related_query_name='answers')
    rating = models.IntegerField(default=0, null=False, verbose_name='Rating')
    type = 'answer'
    objects = AnswerManager()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.text

