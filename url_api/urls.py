from django.urls import path
from .views import URLAPI,URLDetails,RedirectUrl
urlpatterns = [
    #METHODS GET==> to get the URLs List -- POST==> to post a new URL to the list 
    path('urls/', URLAPI.as_view()),
    #METHODS GET==> to get a specific URL -- DELETE==> to delete a specific url from the list
    path('urls/<str:hashed_url>/',URLDetails.as_view()),
    #METHODS GET==> to redirect the hashed url to the original url
    path('<str:hashed_url>/',RedirectUrl.as_view())
]