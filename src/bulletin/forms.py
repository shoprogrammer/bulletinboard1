from django import forms
from .models import BoardModel,Comment,Reaction,Favorite,Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#一段階目
class BoardForm(forms.ModelForm):
    class Meta:
        model = BoardModel
        fields = ['title','content','place']
#二段階目
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

#三段階目
class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['content']




class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text="emailアドレスは必須です。")

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['board']


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['title','message','email']

