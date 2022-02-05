from urllib.request import HTTPRedirectHandler
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from .models import URL
from .serializers import URLSerializer
from rest_framework.response import Response
from rest_framework import status
from .functions import hash_url,is_valid

#Called when the url ==> 'http://localhost:8000/urls/' is called. There are two method that was 
# implemented, one is to get the URLS List and the second is to post a new url into the URLS List  
class URLAPI(APIView):
          #to return the URLs List
          def get(self,request):
                    urls = URL.objects.all()
                    #request.data["valid"] = False
                    for item in urls:
                              item.valid = is_valid(str(item.creation_date), item.validation_period)
                    serializer= URLSerializer(urls, many= True)
                    return Response(serializer.data)
          #to get the new url and added to the URLs List
          def post(self,request):
                    serializer= URLSerializer(data= request.data)
                    request.data["hashed_url"]= hash_url(request.data["original_url"],request.data["url_id"])
                    
                    if serializer.is_valid():
                              serializer.save()
                              return Response(serializer.data,status= status.HTTP_201_CREATED)
                    return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)

#Called when the url ==> 'http://localhost:8000/urls/<str:url_id>/' is called. There are two method that was 
#implemented, one is to get a specific URL data and the second is to delete a specific url from the URLS List 
class URLDetails(APIView):
          #to fetch the specific url from the URLs List
          def get_object(self,url_id):
                    try:
                              return URL.objects.get(url_id=url_id)
                    except URL.DoesNotExist:
                              return HttpResponse(status= status.HTTP_404_NOT_FOUND)
          #to return the specific url to the client
          def get(self,request,url_id):
                    url= self.get_object(url_id)
                    serializer= URLSerializer(url)
                    return Response(serializer.data)
          #to delete the specific url from the URLs List
          def delete(self,request,url_id):
                    found= self.get_object(url_id)
                    found.delete()
                    return Response(status= status.HTTP_204_NO_CONTENT)

#Called when the url ==> 'http://localhost:8000/<str:url_id>/<str:hashed_url>/' is called. There is one method that was 
#implemented. This method will check if the shortened url is still valid, if so it will redirect the client to the original 
#url for the hashed_url. If the url is not valid anymore -that means the validition period is over- the method will redirect 
#the client to the error page that was provided by the frontend 'http://localhost:3000/error'
class RedirectUrl(APIView):
          #to fetch the specific object from the URLs List
          def get_object(self,url_id):
                    try:
                              return URL.objects.get(url_id=url_id)
                    except URL.DoesNotExist:
                              return HttpResponse(status= status.HTTP_404_NOT_FOUND)
          #to check if the validation period is not expired and redirect the client to the proper url
          def get(self,request,url_id,hashed_url):
                    url= self.get_object(url_id)
                    serializer= URLSerializer(url)
                    if(is_valid(serializer.data["creation_date"],serializer.data["validation_period"])):
                              return redirect(serializer.data["original_url"])
                    else:
                              return redirect('http://localhost:3000/error')
                    