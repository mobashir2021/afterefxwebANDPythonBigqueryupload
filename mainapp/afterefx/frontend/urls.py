from django.urls import path
from . import views
#from dash_apps.finished_apps import mygraph
from .dash_apps.finished_apps import mygraph
urlpatterns = [
    path('', views.home, name='front-home'),
    path('about', views.about, name='front-about'),
    path('login', views.login, name='front-login'),
    path('dashboardhome', views.dashboardhome, name='dashboard-homedashboard'),
    path('dashboardanalytics', views.dashboardanalytics, name='dashboard-analytics'),
    path('dashboardlogout', views.dashboardlogout, name='dashboard-logout'),
    path('sendnewsletter/<emailnewsletter>', views.sendnewsletter, name='newsletter'),
    path('requestDemoapi/<name>/<email>/<subject>/<message>', views.requestDemoapi, name='requestdemo')
]
