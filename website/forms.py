from django.forms import widgets
from website.models import Post, Subpost
from django import forms
from ckeditor.fields import RichTextField


category_choices = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)

class Category(forms.Form):
    category = forms.ChoiceField(choices=category_choices)


category_choices = (
    ("Arts & Entertainment", "Arts & Entertainment"),
    ("Autos & Vehicles", "Autos & Vehicles"),
    ("Beauty & Fitness", "Beauty & Fitness"),
    ("Books & Literature", "Books & Literature"),
    ("Business & Industrial", "Business & Industrial"),
    ("Computers & Electronics", "Computers & Electronics"), 
    ("Finance", "Finance"), 
    ("Food & Drink", "Food & Drink"), 
    ("Gambling & Betting", "Gambling & Betting"),
    ("Games", "Games"), 
    ("Health", "Health"), 
    ("Hobbies & Leisure", "Hobbies & Leisure"), 
    ("Home & Garden", "Home & Garden"), 
    ("Internet & Telecom", "Internet & Telecom"), 
    ("Jobs & Education", "Jobs & Education"), 
    ("Law & Government", "Law & Government"), 
    ("News", "News"), 
    ("Online Communities", "Online Communities"), 
    ("People & Society", "People & Society"), 
    ("Pets & Animals", "Pets & Animals"), 
    ("Real Estate", "Real Estate"), 
    ("Reference", "Reference"), 
    ("Science", "Science"), 
    ("Shopping", "Shopping"), 
    ("Sports", "Sports"), 
    ("Travel", "Travel"), 
    ("Others", "Others"),
)
class AddPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': 'Idea Title',
            'style': 'height: 50px; width: 99%; margin-left: 0.6%; margin-bottom: 2%; font-size: 22px; padding: 2%; border-radius: 4px; border-color: rgba(235, 235, 235, 0.74)'
        }
    ), label="")
    category = forms.ChoiceField(choices=category_choices, widget=forms.Select(attrs={
        'style': 'padding: 0.8%; font-size: 18px; margin: 1%; margin-bottom: 2%;border-radius: 5%;'
    }))
    

    class Meta:
        model = Post
        fields = ('title', 'post', 'category', 'image1', 'image2', 'image3', 'image4', 'image5')
    
class AddSubPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control', 
            'placeholder': 'Update Idea',
            'style': 'height: 50px; width: 99%; margin-left: 0.5%; margin-bottom: 1.2%; margin-top: 0.5%;font-size: 20px; padding: 1.5%; border-radius: 4px; border-color: rgba(235, 235, 235, 0.74)'
        }
    ), label="")
    class Meta:
        model = Subpost
        fields = ('title', 'post', 'image1', 'image2', 'image3', 'image4', 'image5')
