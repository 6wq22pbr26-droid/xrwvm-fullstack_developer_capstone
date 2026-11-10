from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
urlpatterns=[path('admin/',admin.site.urls),path('djangoapp/',include('djangoapp.urls')),
 path('about',TemplateView.as_view(template_name='About.html')),path('contact',TemplateView.as_view(template_name='Contact.html')),
 re_path(r'^(?:|login|register|dealers|dealer/\d+|postreview/\d+)/?$',ensure_csrf_cookie(TemplateView.as_view(template_name='index.html')))]
