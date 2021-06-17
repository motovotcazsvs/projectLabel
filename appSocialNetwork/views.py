from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import BookForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


def home(request):
    obj = Book.objects.order_by('-date_publication')
    return render(request, 'appSocialNetwork/home.html', {'obj': obj})

def signup_page(request):   
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'appSocialNetwork/registration/signup.html', {'user_form': user_form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Не правельно введен пароль или логин')
    context = {}
    return render(request, 'appSocialNetwork/registration/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def myLabel(request):
    my_posts = Book.objects.filter(author_publication = request.user)
    my_posts = my_posts.order_by('-date_publication')
    return render(request, 'appSocialNetwork/mylabel.html', {'my_posts': my_posts})

def addPublication(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = form.save(commit = False)
            obj.author_publication = request.user
            obj.save()         
            return redirect('home')
    else:
        form = BookForm() 
    return render(request, 'appSocialNetwork/addpublication.html', {'form': form})

def pagePublication(request, pagePublication_id):
    try:
        publication = Book.objects.get(id = pagePublication_id)
    except:
        raise Http404("Публикация не найдена!")
    
    sort_comment = publication.comment_set.order_by('-id')
    
    if request.method == 'POST':
        form_comment = CommentForm(request.POST)    
        if form_comment.is_valid():         
            commen = form_comment.save(commit = False)
            commen.comment_author = request.user
            commen.comment_book = publication
            commen.save()
            return redirect('pagePublication', pagePublication_id = publication.id)
    else:
        form_comment = CommentForm()

    context = {
        'publication': publication,
        'sort_comment': sort_comment,
        'form_comment': form_comment,
    }

    return render(request, 'appSocialNetwork/pagePublication.html', context)
 
"""    
def controlLike(request, pagePublication_id)
    if request.method == "POST":
        if request.is_authenticated:
            public = Post.objects.get(id = pagePublication_id)
            authors_like = User.filter.get(like_users = pagePublication_id)
            current_user = request.user
            if current_user not in authors_like:
                try:
                    public.like_count += 1
                    public.like_users.add(current_user)
                    public.save()
                    return redirect('post_detail', pk=pk)
                except ObjectDoesNotExist:
                    return redirect('post_detail', pk=pk)
            else:
                return redirect('post_detail', pk=pk)
        else:
            return redirect('post_detail', pk=pk)
    
"""