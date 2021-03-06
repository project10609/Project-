"""奇鋪比價 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from products import views
from .views import contact_us, faq, about, news, forum, handler404, handler500

urlpatterns = [
    path('404/',handler404),
    path('500/',handler500),
    path('', views.index, name='index'),
    path('news/',news,name='news'),
    path('account/', include('account.urls')),
    path('search/', include('search.urls')),
    path('product/', include('products.urls')),
    path('contact_us/' ,contact_us,name="contact_us"),
    path('FAQ/',faq,name='faq'),
    path('about_us',about,name='about'),
    path('forum',forum,name='forum'),
    # path(r'/search', productSearch)
]
if settings.ADMIN_ENABLED:
    urlpatterns += [path('admin/', admin.site.urls)]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
