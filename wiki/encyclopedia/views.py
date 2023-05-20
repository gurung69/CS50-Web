from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import random
import markdown2

class CreatePageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        title = self.cleaned_data['title']
        if util.get_entry(title) is not None:
            error_msg = mark_safe("<div class='alert alert-danger' role='alert'>already exists</div>")
            raise ValidationError(error_msg)
        return title
    
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    if request.method == "POST":
        if util.get_entry(request.POST.get('q')):
            return redirect(f'wiki/{request.POST.get("q")}')
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": [entry for entry in util.list_entries() if request.POST.get('q').upper() in entry.upper()]
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
     content = markdown2.markdown(util.get_entry(title)) 
     if content is not None:
        return render(request, 'encyclopedia/entry.html', {
            "entry":title,
            "content":content
        })
     return HttpResponse("Page not found")

def create_page(request):
    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('/')
    else:
        form = CreatePageForm()
    return render(request, 'encyclopedia/form.html',{
        "form": form
    })

def edit_page(request, title):
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
    else:
        content = util.get_entry(title)
        form = EditPageForm(initial={'content': content})
    return render(request, 'encyclopedia/form.html',{
        "form": form,
    })

def random_page(request):
    entries = util.list_entries()
    ranchoice = random.choice(entries)
    return redirect(f'wiki/{ranchoice}')
