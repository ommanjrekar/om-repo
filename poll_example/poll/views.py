from django.shortcuts import render, redirect
from .forms import CreatePollForm
from .models import Poll
from django.http import HttpResponse


# Create your views here.
def home(request):
    polls = Poll.objects.all()
    content = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', content)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('home')

    else:
        form = CreatePollForm()
    content={
        'form' : form
    }
    return render(request, 'poll/create.html', content)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    content={
        'poll' : poll
    }
    return render(request, 'poll/results.html', content)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count +=1
        elif selected_option == 'option2':
            poll.option_two_count +=1
        elif selected_option == 'option3':
            poll.option_three_count +=1
        else : 
            return HttpResponse(400, 'invalid form')

        poll.save()
        return redirect('results', poll_id)

    content={
        'poll' : poll
    }
    return render(request, 'poll/vote.html', content)