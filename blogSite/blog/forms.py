from django.forms import CharField, EmailField, Form, ModelForm, Textarea

from .models import Comment


class SearchForm(Form):
    query = CharField()


class EmailPostForm(Form):
    name = CharField(max_length=40)
    email = EmailField()
    to = EmailField()
    comments = CharField(required=False, widget=Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
