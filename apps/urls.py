from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', login_view, name='login_view'),
    path('index/', views.index, name='index')
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),

]
