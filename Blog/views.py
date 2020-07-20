from django.shortcuts import render, HttpResponse, redirect, HttpResponsePermanentRedirect
from .models import Post, BlogComment
from django.contrib import messages
from Blog.templatetags import extras
# Create your views here.

def bloghome(request):
    posts = Post.objects.all().order_by('-views')
    
    return render(request, 'blog/blogHome.html', {'post':posts})

def blogpost(request,slug):
    bpost = Post.objects.filter(slug=slug).first()
    bpost.views = bpost.views + 1
    bpost.save()
    comments = BlogComment.objects.filter(post=bpost,parent=None).order_by('-timestamp')
    replies = BlogComment.objects.filter(post=bpost).exclude(parent=None).order_by('-timestamp')
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post':bpost, 'comments':comments, "replyDict":replyDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        print("reached in post if")
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno=="":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your Comment submitted")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply submitted")
    return HttpResponsePermanentRedirect(f"/blog/{post.slug}")