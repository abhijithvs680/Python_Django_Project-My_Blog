from django.urls import path
from . import views
from .views import SignUpView,PostView,SignInView,SignoutView, ProfileView,BlogView,DeleteBlogView,EditProfileView,EditBlogView,ChangePasswordView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name="index"),
    path('signup',SignUpView.as_view(),name='signup'),
    path('signin',SignInView.as_view(),name="signin"),
    path('signout',SignoutView.as_view(),name="signout"),
    path('profiles/', ProfileView.as_view(), name='profiles'),
    path('post/', PostView.as_view(), name='post'),
    path('blog/', BlogView.as_view(), name='blog1'),
    path('blog/<int:blog_id>/', BlogView.as_view(), name='blog_detail'),
    path('blog_edit/<int:id>/', EditBlogView.as_view(), name='blog_edit'),
    path('blog_delete/<int:id>/', DeleteBlogView.as_view(), name='blog_delete'),
    path('edit_user/<int:user_id>/', EditProfileView.as_view(), name='edit_user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),




]






