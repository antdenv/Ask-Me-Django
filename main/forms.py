from django import forms
from django.core.validators import RegexValidator
from .models import User, Question, Answer

textValidator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Text should contain letters")
tagsValidator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Tags should contain letters")
passwordValidator = RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                   "Password should contain minimum 8 characters, at least 1 letter and 1 number")


class UserSignUpForm(forms.ModelForm):
    first_name = forms.CharField(validators=[textValidator],
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'minlength': 2,
                                                               'maxlength': 50,
                                                               'placeholder': 'First name'}))
    last_name = forms.CharField(validators=[textValidator],
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'minlength': 2,
                                                              'maxlength': 50,
                                                              'placeholder': 'Last name'}))
    username = forms.CharField(validators=[textValidator],
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'minlength': 4,
                                                             'maxlength': 50,
                                                             'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'E-mail'}))
    password = forms.CharField(validators=[passwordValidator],
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Password confirmation'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class UserSignInForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'maxlength': 50,
                                                             'placeholder': 'Username'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(required=False,
                                 validators=[textValidator],
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'minlength': 2,
                                                               'maxlength': 50,
                                                               'placeholder': 'First name'}))
    last_name = forms.CharField(required=False,
                                validators=[textValidator],
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'minlength': 2,
                                                              'maxlength': 50,
                                                              'placeholder': 'Last name'}))
    username = forms.CharField(validators=[textValidator],
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'minlength': 4,
                                                             'maxlength': 50,
                                                             'placeholder': 'Username'}))
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'E-mail'}))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar')


class NewQuestionForm(forms.ModelForm):
    title = forms.CharField(validators=[textValidator],
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'maxlength': 100,
                                                          'minlength': 10,
                                                          'placeholder': 'Write title of your question...'}))
    text = forms.CharField(validators=[textValidator],
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'minlength': 30,
                                                        'placeholder': 'Write details about your question...'}))
    tags = forms.CharField(validators=[tagsValidator],
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Write tags for your question...'}))

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags',)


class WriteAnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'minlength': 20,
                                                        'placeholder': 'Write answer for this question...'}))

    class Meta:
        model = Answer
        fields = ('text',)
