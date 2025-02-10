from django.urls import path

from playlist.views import IndexView, PlayListView, SearchView, LoginView, SignupView, LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name='index_view'),
    path("playlist/", PlayListView.as_view(), name='your_playlists'),
    path("search/", SearchView.as_view(), name='search_page'),
    path("login", LoginView.as_view(), name='login'),
    path("logout", LogoutView.as_view(), name='logout'),
    path("signup", SignupView.as_view(), name='signup'),
]