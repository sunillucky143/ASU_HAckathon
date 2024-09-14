"""
URL configuration for Mining_Arizona project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Mining_Arizona.accounts.views import register, LoginView, PostView, CommentView
from Mining_Arizona.Tailings_treatment.tailings_treatment import process_tailings_form




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('process-form/', process_tailings_form, name='process_form'),
    path('post/', PostView.as_view(), name='post'),
    path('comment/', CommentView.as_view(), name='comment'),

]
