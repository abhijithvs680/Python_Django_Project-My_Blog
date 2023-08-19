from django.db import models


# Create your models here.
class user_signup(models.Model):
    Name=models.CharField(max_length=25)
    Email=models.EmailField(max_length=25, unique=True)
    Mobile=models.CharField(max_length=10, unique=True)
    Username=models.CharField(max_length=25, unique=True)
    Password=models.CharField(max_length=128)

    def __str__(self):
        return self.Name
    


from django.contrib.auth.models import User


class ProfilePicture(models.Model):
    user=models.OneToOneField(user_signup,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads', null=True, blank=True)

    def __str__(self):
     return f"Profile Picture for {self.user.username}"



class Post(models.Model):
    user = models.ForeignKey(user_signup, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploadimage', null=True, blank=True)
    title = models.CharField(max_length=25)
    text = models.TextField(max_length=550)

    def __str__(self):
        return self.title
        