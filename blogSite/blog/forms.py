from django.forms import (
    CharField,
    EmailField,
    Form,
    Textarea,
)

class EmailPostForm(Form):
    name = CharField(max_length=40)
    email = EmailField()
    to = EmailField()
    comments = CharField(required=False,
                         widget=Textarea)

