from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Poll, Choice, Vote
from .forms import RegisterForm, PollForm
from django.utils import timezone
from django.contrib import messages


# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Or wherever your homepage is
        else:
            messages.error(request, "Incorrect username or password.")
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard view - Displays the polls created by the logged-in user
@login_required
def dashboard_view(request):
    polls = Poll.objects.all()  # ✅ Correct: shows all polls
    return render(request, 'dashboard.html', {'polls': polls})


# Poll creation view - Allows the admin to create a poll and add options
@login_required
def create_poll_view(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            # Add multiple choices
            for i in range(3):  # Get 3 options from the form
                option_text = request.POST.get(f'option_{i}')
                if option_text:
                    Choice.objects.create(poll=poll, choice_text=option_text)
            return redirect('dashboard')
    else:
        poll_form = PollForm()
    return render(request, 'create_poll.html', {'form': poll_form})

# Poll detail view - Displays a poll's details and allows voting
@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    now = timezone.now()
    is_closed = now > poll.voting_deadline
    has_voted = Vote.objects.filter(user=request.user, poll=poll).exists()
    is_admin = request.user.is_staff

    # ✅ Show result only to admins or if poll is closed
    if is_admin or is_closed:
        choices = poll.choices.all()
        return render(request, 'polls/result.html', {
            'poll': poll,
            'choices': choices,
            'is_closed': is_closed
        })

    # ❌ If poll is open and user has already voted → block re-vote
    if has_voted:
        return render(request, 'polls/already_voted.html', {
            'poll': poll,
            'is_closed': is_closed
        })

    # ✅ Handle vote submission (only if not yet voted)
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, pk=choice_id)

        # Extra protection — double-check vote not already cast
        if not has_voted:
            Vote.objects.create(user=request.user, poll=poll, choice=choice)
            choice.votes += 1
            choice.save()
            return redirect('poll_detail', poll_id=poll.id)

    return render(request, 'polls/detail.html', {
        'poll': poll,
        'is_closed': is_closed
    })
# Poll result view - Displays the result of the poll
@login_required
def poll_result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    is_closed = timezone.now() > poll.voting_deadline
    choices = poll.choices.all()

    # Only show results to admin OR if poll is closed
    if user.is_staff or is_closed:
        return render(request, 'polls/result.html', {
            'poll': poll,
            'choices': choices,
            'is_closed': is_closed
        })
    else:
        return render(request, 'polls/result.html', {
            'poll': poll,
            'choices': [],
            'is_closed': is_closed
        })


def welcome(request):
    return render(request, 'welcome.html')