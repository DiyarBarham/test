from django.shortcuts import render, redirect, HttpResponse
from .models import User, Books
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect('/books')
    return render(request, 'index.html')
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['passwd'].encode(), logged_user.password.encode()):
            request.session['user'] = logged_user.email
            return redirect('/books')
    messages.error(request, 'the eamil and password do not match')
    return redirect('/')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    password = request.POST['passwd']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(firstname=request.POST['firstname'],lastname= request.POST['lastname'],  password=pw_hash, email = request.POST['email'])
    request.session['user'] = request.POST['email']
    messages.success(request, "User successfully created")
    return redirect('/books')
def books(request):
    if 'user' not in request.session:
        return redirect('/')
    user = User.objects.filter(email=request.session['user'])
    context ={
        'loggeduser': user[0],
        'books': Books.objects.all()

    }
    return render(request, 'welcome.html', context)
def logout(request):
    if 'user' in request.session:
        request.session.clear()
    return redirect('/')
def addbook(request):
    book = Books.objects.get(title=request.POST['title'], desc=request.POST['desc'],
                             uploaded_by_id=User.objects.get(id=request.POST['userid']))
    user = User.objects.get(id=request.POST['userid'])
    book.favorite.add(user)
    return redirect('/books')
def editbook(request):

    book = Books.objects.get(title=request.POST['pretitle'])
    book.desc = request.POST['desc']
    book.title = request.POST['title']
    book.save()
    user = User.objects.get(email= request.session['user'])
    book.favorite.add(user)
    return redirect('/books')
def bookpage(request, id):
    book = Books.objects.get(id=id)
    user = User.objects.filter(email=request.session['user'])
    context = {
        'loggeduser': user[0],
        'book': book,
        'users': User.objects.all()

    }
    return render(request, 'book.html', context)