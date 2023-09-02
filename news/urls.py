from django.urls import path
from . import views
urlpatterns = [

  path('',views.home, name="home"),
  path("search",views.search,name="search"),
  path("searchtop",views.searchtop,name="searchtop"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),
  path("category/<str:value>",views.category,name="category"),
  path("updateCategory",views.updateCategory,name="updateCategory"),
   path("feed",views.feed,name="feed")
]
