from django.shortcuts import render
from django.http import HttpResponse
from .models import Note
from .forms import NoteForm

# Create your views here.
def index(request):

    if request.method == 'POST':
        print(request.POST)
        form = NoteForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
        else:
            print("error saving new note")

    if request.user.is_anonymous:
        notes = None
    else:
        notes = Note.objects.filter(user=request.user)

    context = {
        'notes': notes,
        'user': request.user,
        'form': NoteForm
    }

    return render(request, 'notes/index.html', context)

