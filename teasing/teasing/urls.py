"""
URL configuration for teasing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from teasingApp import views as teasing
from django.urls import path
from network import views as network
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,teasing.initialize),
    path('index/' ,teasing.index ,name='index'),
    path('shuffle/<int:shuffle_number>/', teasing.shuffle, name='shuffle'), # type: ignore
    path('solve',teasing.solve ,name='solve') , # type: ignore
    path('network/',network.index) ,
    path('initialize_graph/' ,network.initialize_graph ,name='initialize_graph') ,
    path('request_domain/',network.request_domain , name='request_domain') ,# type: ignore ,
    path('result_search/' ,network.request_domain ,name='result_search') ,
    path('cut_path/' ,network.cut_path ,name='cut_path')
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
