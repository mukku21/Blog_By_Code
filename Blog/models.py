from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import gettext as _

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(_("title"), max_length=255)
    content = models.TextField()
    subContent = models.TextField(_("Sub_Content"))
    author = models.CharField(_("author"), max_length=50)
    slug = models.CharField(_("slug"), max_length=50)
    views = models.IntegerField(_("Views on Post"),default=0)
    timeStamp = models.DateTimeField(_("timeStamp"), default= datetime.now)
    thumbnail = models.ImageField(upload_to="blog/images", default="")
 
    

    def __str__(self):
        return self.title + " by " + self.author

class BlogComment(models.Model):
    sno = models.AutoField(_("sno"),primary_key=True)
    comment = models.TextField(_("Comment"))
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE)
    parent = models.ForeignKey("self", verbose_name=_("Parent"), on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(_("Time"), default=datetime.now)

    
    def __str__(self):
        return self.comment[0:13] + "... by " + self.user.username