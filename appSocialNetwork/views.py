from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import BookForm
#from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def home(request):
    #obj = Book.objects.all()
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
            object = form.save(commit = False)
            object.author_publication = request.user
            object.save()         
            return redirect('home')
    else:
        form = BookForm() 
    return render(request, 'appSocialNetwork/addpublication.html', {'form': form})

def pagePost(request, pagePost_id):
    is_liked = False
    try:
        i = Book.objects.get( id = pagePost_id )
        if i.likes.filter(id=request.user.id).exists():
            is_liked = True
    except:
        raise Http404("Публикация не найдена!")
    
    return render(request, 'appSocialNetwork/pagePost.html', {'publication': i, 'is_liked': is_liked, 'total_likes': i.totalLikes()})


def like_post(request): 
    post = get_object_or_404(Book, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return render(request, 'appSocialNetwork/pagePost.html', {'publication': post, 'is_liked': is_liked, 'total_likes': post.totalLikes()})