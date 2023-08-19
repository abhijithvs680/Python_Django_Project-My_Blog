from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout
from django.views import View
from .forms import *

# Create your views here.
def index(request):
    return render(request,'blog/index.html')

def signup(request):
    form = user_signupForm()
    return render(request,'blog/signup.html',{'form':form})

def post(request):
    form = PostForm()
    return render(request,'blog/post.html',{'form':form})

class SignUpView(View):
    def get(self, request):
        form = user_signupForm()
        return render(request, 'blog/signup.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = user_signupForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                Password = form.cleaned_data['Password']
                user.Password = make_password(Password)  # Encrypt the password
                user.save()
                form = user_signupForm()
                # context = {'msg': 'successfully registered', 'form': form}
                return render(request, 'blog/signin.html',{'form': form})
            else:
                error = form.errors
                return render(request, 'blog/signup.html', {'error': error, 'form': form})


class SignInView(View):
    def get(self, request):
        return render(request, 'blog/signin.html')

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            try:
                user = user_signup.objects.get(Username__exact=username)
            except user_signup.DoesNotExist:
                user = None
            if user and check_password(password, user.Password):
                request.session['Name'] = user.Name
                request.session['id'] = user.id
                return render(request, 'blog/index.html')
            return render(request, 'blog/signin.html', {'error': "Invalid username or password"})

class SignoutView(View):
    def get(self,request):
        your_data =request.session.get('id',None)
        if your_data is not None:
            del request.session['id']
        logout(request)
        return redirect ('signin')  
    

    
class ProfileView(View):
    
    def get(self, request):
        if request.session.get('id'):
            
            form = ProfilePictureForm()
            user_id = request.session['id']
            user =user_signup.objects.get(id=user_id)
            try:
             profile_pic = ProfilePicture.objects.filter(user_id=request.session['id']).values('image').get()
            except ProfilePicture.DoesNotExist:
                profile_pic= None
           
            if profile_pic:
             
              context = {'form': form,'user':user,'profile_pic':profile_pic,'menu':'profile'}
            else:
                context = {'form': form,'user':user,'menu':'profile'}


            return render(request, 'blog/profile.html',context)
        else:
             return redirect('signin')
        
    def post(self, request):
     if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session['id']
            
            # Check if profile picture already exists for the user
            profile_pic = ProfilePicture.objects.filter(user_id=user_id).first()
        
            if profile_pic:
               # Update the image field with the new path
               profile_pic.image_path = 'uploads/' + request.FILES['image'].name
               profile_pic.image = request.FILES['image']
               profile_pic.save()
               return redirect('profiles')
            else:
               # Create a new profile picture entry
               profile_pic = ProfilePicture()
               profile_pic.user_id = user_id
               profile_pic.image_path = 'uploads/' + request.FILES['image'].name
               profile_pic.image = request.FILES['image']
               profile_pic.save()
            
               return redirect('profiles')
        else:
            form = ProfilePictureForm()
    
     return render(request, 'blog/profile.html', {'form': form})

class EditProfileView(View):
    def get(self, request, user_id):
        edit_data = get_object_or_404(user_signup, id=user_id)
        form = user_signupForm(instance=edit_data)
        form.fields.pop('Password')  # Exclude the password field

        return render(request, 'blog/update_profile.html', {'form': form, 'edit_data': edit_data})

    def post(self, request, user_id):
        edit_data = get_object_or_404(user_signup, id=user_id)
        form = user_signupForm(request.POST, instance=edit_data)
        form.fields.pop('Password')  # Exclude the password field


        if form.is_valid():
            form.save()
            return redirect('profiles')
        else:
            return render(request, 'blog/update_profile.html', {'form': form, 'edit_data': edit_data})
class EditPasswordView(View):

       def get(self,request,id):     
            return render(request, 'blog/change_password.html')
      
       def post(self,request,id):
              user_id = request.session['id']
              user =user_signup.objects.get(id=id)
              password=make_password(request.POST.get('Password'))
              user.Password=password
              user.save()
              return redirect('profiles')

class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'blog/change_password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = user_signup.objects.get(id=request.session.get('id'))
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
        

            if check_password(old_password, user.Password):
                new_password = make_password(new_password)
                user.Password = new_password
                user.save()
                # messages.success(request, 'Password changed successfully.')
                return redirect('profiles')
            else:
                error = "Invalid old password"
                return render(request, 'blog/change_password.html', {'form': form, 'error': error})
        return render(request, 'blog/change_password.html', {'form': form})


class PostView(View):
    def get(self, request):
        if request.session.get('id'):
            form = PostForm()
            user_id = request.session['id']
            user = user_signup.objects.get(id=user_id)
            return render(request, 'blog/post.html', {'form': form, 'user': user})
        else:
            return redirect('signin')

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session['id']
            instance = form.save(commit=False)
            instance.user_id = user_id
            instance.save()
            return redirect('blog1')
        else:
            error = form.errors
            return render(request, 'blog/post.html', {'error': error, 'form': form})


  

class BlogView(View):
    def get(self, request, blog_id=None):
        user_id = request.session.get('id')
        if blog_id is not None:
            return self.get_blog_detail(request, blog_id, user_id)
        
        blog_f = Post.objects.latest('id')
        blog = Post.objects.exclude(id=blog_f.id).all().order_by('-id')
        context = {'menu': 'blog', 'blog': blog, 'blog_f': blog_f, 'user_id': user_id}
        return render(request, 'blog/blog1.html', context)
    
    def get_blog_detail(self, request, blog_id, user_id):
        blog = get_object_or_404(Post, id=blog_id)
        context = {'menu': 'blog', 'blog': blog, 'user_id': user_id}
        return render(request, 'blog/blog_detail.html', context)
    
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session.get('id')
            form.instance.user_id = user_id
            form.save()
            return redirect('blog1')
        
        blog_f = Post.objects.latest('id')
        blog = Post.objects.exclude(id=blog_f.id).all().order_by('-id')
        context = {'menu': 'blog', 'blog': blog, 'blog_f': blog_f, 'user_id': user_id, 'form': form}
        return render(request, 'blog/blog1.html', context)

class EditBlogView(View):
    def get(self, request, id):
        blog = get_object_or_404(Post, id=id)
        form = PostForm(instance=blog)
        context={'menu':'post','form': form, 'blog': blog}
        return render(request, 'blog/post_edit.html', context)
        

    def post(self, request, id):
        blog = get_object_or_404(Post, id=id)
        form = PostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail',blog_id=blog.id)
        context={'menu':'post','form': form, 'blog': blog}

        return render(request, 'blog/post_edit.html', context)


class DeleteBlogView(View):

       def get(self, request, id):
          blog = get_object_or_404(Post, id=id)
          blog.delete()
          return redirect('blog1')

