from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from bulletin import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include('bulletin.urls')),
    path('accounts/login/',auth_views.LoginView.as_view(),name='login'),
    path('accounts/logout/',views.logout_view,name="logout"),
    path('accounts/signup/',views.signup,name="signup"),
    path('accounts/profile/',views.profile,name="profile"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
