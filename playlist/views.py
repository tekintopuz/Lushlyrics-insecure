import logging

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from youtube_search import YoutubeSearch

from core.settings import CONTAINER
from playlist.models import PlaylistUser


class IndexView(View):
    def get(self, request):

        context = {'CONTAINER':CONTAINER,
                   'song': 'kSFJGEHDCrQ',
                   "active": "home"
                   }
        template = loader.get_template(f'player.html')
        return HttpResponse(template.render(context, request))




class PlayListView(LoginRequiredMixin, View):
    def get(self, request):
        cur_user = PlaylistUser.objects.filter(username=request.user.username).first()
        if cur_user:
            user_playlist = cur_user.playlist_song_set.all()

            song = request.GET.get('song')
            song = cur_user.playlist_song_set.get(song_title=song)
            song.delete()
        else:
            song = 'kSFJGEHDCrQ'
            user_playlist = []

        context = {'song':song,
                   'user_playlist': user_playlist
                   }
        template = loader.get_template('playlist.html')
        return HttpResponse(template.render(context, request))


class AddPlaylistView(View):
    def post(self, request):
        cur_user = PlaylistUser.objects.get(username=request.user)
        title = request.POST.get('title', None)
        song_title = request.POST.get('song_title', None)

        if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

           songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
           song__albumsrc=songdic['thumbnails'][0]
           cur_user.playlist_song_set.create(song_title=request.POST['title'],
                                             song_dur=request.POST['duration'],
                                             song_albumsrc = song__albumsrc,
                                             song_channel=request.POST['channel'],
                                             song_date_added=request.POST['date'],
                                             song_youtube_id=request.POST['songid'])


        return HttpResponse()

class SearchView(View):
    def post(self, request):
        search = request.GET.get('search', None)
        if search:
            song = YoutubeSearch(search, max_results=10).to_dict()
            song_li = [song[:10:2],song[1:10:2]]
            context = {'CONTAINER': song_li, 'song': song_li[0][0]['id']}
            template = loader.get_template('search.html')
            return HttpResponse(template.render(context, request))

        return redirect('/')



class LoginView(View):
    def get(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"
        if request.user.is_authenticated:
            return redirect(redirect_url)

        else:
            context = {

            }
            template = loader.get_template('login.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"
        if redirect_url[0] != "/":
            redirect_url = "/" + redirect_url


        username = request.POST['username']
        username = " ".join(username.lower().strip().split())
        password = request.POST['password']
        user = User.objects.filter(Q(username=username)|Q(email=username)).first()
        if user:
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                request.session["status"] = "success",
                request.session["message"] = "Login is successfull..."
                return redirect(redirect_url)
            else:
                context = {
                    'status': 'error',
                    'message': "Username or password is wrong!"}
                template = loader.get_template('login.html')
                return HttpResponse(template.render(context, request))

        else:
            raise HTTP_400_BAD_REQUEST
class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
        except Exception as e:
            logging.exception(e)
        return redirect("/")

class SignupView(View):
    def get(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"
        if request.user.is_authenticated:
            return redirect(redirect_url)

        else:
            context = {
                'menu_open': [], 'active': ['sisteme_giris'],
            }
            template = loader.get_template('signup.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        username = request.POST['username']
        username = " ".join(username.lower().strip().split())

        email = request.POST['email']
        email = " ".join(email.lower().strip().split())

        password = request.POST['password']
        password = " ".join(password.lower().strip().split())

        confirm_password = request.POST['confirm-password']
        confirm_password = " ".join(confirm_password.lower().strip().split())

        if User.objects.filter(username=username).exists():
            context = {
                'status': 'error',
                'message': " Username already exists!"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            context = {
                'status': 'error',
                'message': "Username already exists!"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            context = {
                'status': 'error',
                'message': "Password cannot be confirmed!"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        redirect_url = request.GET["next"] if "next" in request.GET else "/"

        new_user = User.objects.create(email=email, username=username)
        new_user.set_password(password)
        new_user.save()

        new_user = authenticate(request, username=new_user.username, password=password)
        auth_login(request, new_user)
        request.session["status"] = "success",
        request.session["message"] = "Signup is successfull.."
        return redirect(redirect_url)
