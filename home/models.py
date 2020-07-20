from django.db import models
from django.utils.translation import gettext as _
from datetime import datetime

# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(_("name"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    phone = models.CharField(_("Phone"), max_length=50)
    website = models.CharField(_("Website"), max_length=50)
    msg = models.TextField(_("Text_Field"))
    timeStamp = models.DateField(_("DateTime"), auto_now=False, auto_now_add=True) 
    

    def __str__(self):
        return "Message From " + self.name + ", " + self.email
    
