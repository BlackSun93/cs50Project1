from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect#look up redirect
from django import forms
from django.urls import reverse #look this up
from django.db.models import Q
from markdown2 import Markdown
import random

from . import util

markdown = Markdown()

class ArticleForm(forms.Form):
 #search = forms.CharField(label = "Search Encyclopedia")
 #rating = forms.IntegerField(label = "rating", min_value=1, max_value=5)

    articleTitle = forms.CharField(label="Title ")
    articleBody = forms.CharField(  label = "Body", widget=forms.Textarea(attrs={'id': 'myFIELD', 'label': "Body ",
     'rows' : '4', 'cols': '40',
     'placeholder': 'Enter the atricle text here, you have to start the article with #Title and a newline for it to display properly!'
      }) )

def index(request ):
    if request.method == 'POST': # from create new page
        form = ArticleForm(request.POST)
        if form.is_valid():
            newTitle = form.cleaned_data["articleTitle"]
            newArticle = form.cleaned_data["articleBody"]
            print("enterecd " + newTitle)
            print("looking for ")   
            print(util.list_search(newTitle))
            if util.list_search(newTitle):
                return render(request, "encyclopedia/error.html")

            util.save_entry(newTitle, newArticle)
            print(newTitle + "omg")
            url = reverse('title' , kwargs={'subject': newTitle})
            print(url)
            return HttpResponseRedirect(url)
           
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def test(request):
    return HttpResponse ("blah")



def wiki(request, subject):
    #if request.method == 'POST': #from edit page
    #    print(subject)
    #    newArticle = request.POST.get('article')
    #    print(newArticle + "is the new article")
    #    util.save_entry(subject, newArticle)


    print(request)
    article = util.get_entry(subject)
    print(article)
    if not article:
        return render(request, "encyclopedia/article.html", {
        "title": "Article does not exist", "subject": subject
    })
    return render(request, "encyclopedia/article.html", {
        "title": markdown.convert(article), "subject": subject
        })

def search(request):
    
    print(request)
    query = request.GET.get('q').lower() #search form is called q in the layout.html file
    print(query)
    article = util.get_entry(query)
    if article:
        url = reverse('title' , kwargs={'subject': query})
        print(url)
        return HttpResponseRedirect(url)
      
    print( util.list_search(query))
    return render (request, "encyclopedia/index.html", {"entries": util.list_search(query) })
    
    
   
def createNewPage(request):
    return render(request, 'encyclopedia/createNewPage.html', {"form" : ArticleForm().as_p()})

def editPage(request, subject):
    
    if request.method == 'POST': #from edit page
        print(subject)
        newArticle = request.POST.get('article')
        newTitle = request.POST.get('subject')
        print(newArticle + "is the new article")
        
        util.save_entry(newTitle, newArticle)
        url = reverse('title' , kwargs={'subject': subject})
        print(url)
        return HttpResponseRedirect(url)

    article = util.get_entry(subject)
    return render(request, "encyclopedia/editPage.html", {
        "title": article, "subject": subject
    })
   


def randomPage(request):
    randomArt = random.choice(util.list_entries())
    print(randomArt + "nnnnnn")
    article = util.get_entry(randomArt)
    return render(request, "encyclopedia/article.html", {
        "title": markdown.convert(article), "subject": randomArt
        })
# 

    
