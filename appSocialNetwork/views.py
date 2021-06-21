from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import BookForm
from django.contrib.auth.decorators import login_required


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
    try:
        i = Book.objects.get( id = pagePost_id )
    except:
        raise Http404("Публикация не найдена!")
    
    return render(request, 'appSocialNetwork/pagePost.html', {'publication': i})

@login_required
def post_like(request, add_id, pk):
    if request.method == "POST":
        if request.is_authenticated:
            post_item = Post.objects.get(id=add_id)
            user_item = User.filter.get(like=add_id)
            current_user = request.user
            if current_user not in user_item:
                try:
                    post_item.like_publication += 1
                    post_item.like_author.add(current_user)
                    post_item.save()
                    return redirect('pagePost', pk=pk)
                except ObjectDoesNotExist:
                    return redirect('pagePost', pk=pk)
            else:
                return redirect('pagePost', pk=pk)
        else:
            return redirect('pagePost', pk=pk)