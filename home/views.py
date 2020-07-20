from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from Blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    post = Post.objects.all().order_by('-views')[0:4]
    context = {'post':post}
    return render(request, 'home/home.html', context)

def contact(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        msg = request.POST.get('msg')
        if len(name) <= 1 or len(phone) < 10 or len(msg) < 4:
            messages.info(request, "Unsuccess, There are incorrect details have been inserted, Please try again, and insert correctly")
        else:
            contacts = Contact(name=name, email=email, phone=phone, website=website, msg = msg)
            contacts.save()
            messages.success(request,"Success!, Your Message Has Been Sent, We will contact you shortly. Thank You!")
        return render(request, 'home/contact.html')
    else:
        return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>70 or len(query)<=0:
        allPost=[]
        messages.info(request,"No search results found")
    else:
        PostTitle = Post.objects.filter(title__icontains=query)
        PostContent = Post.objects.filter(content__icontains=query)
        allPost = PostTitle.union(PostContent)
        if len(allPost) == 0:
            messages.info(request, "No search results found")
    params = {"allPost":allPost, 'sresult':len(allPost),"query":query}
    return render(request, 'home/search.html', params)

def handleSignup(request):
    # checking the post request
    if request.method=="POST":
        # getting data frompost method
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Checks for errorneous inputs
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken" +' '+ fname)
                return redirect('home')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken" +' '+ fname)
                return redirect('home')
            else:    
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.save()
                messages.success(request,"Successfully Created" +' '+ fname)
                return redirect('home')
        else:
            messages.warning(request,"Password did not match" +' '+ fname)
            return redirect('home')
    else:
        return HttpResponse("404- Page Not Found")

def handleSignin(request):
    # checking the post request
    if request.method=="POST":
        # getting data frompost method
        singinusername = request.POST['signinusername']
        singinpass = request.POST['signinpass']

        # checking user auth
        user = authenticate(username=singinusername, password=singinpass)
        if user is not None:
            login(request,user) 
            messages.success(request,'Successfully Login'+' '+singinusername)
            return redirect('home')
        else:
            messages.error(request,"Invalid Credential" +' '+ singinusername)
            return redirect('home')
    else:
        return HttpResponse("404-Page Not Found")

def handleSignout(request):
    logout(request)
    messages.success(request,"Successfully Logout")
    return redirect('home')
    