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
                    for item in urls:
                              item.valid = is_valid(str(item.creation_date), item.validation_period)
                    serializer= URLSerializer(urls, many= True)
                    return Response(serializer.data)
          #to get the new url and added to the URLs List
          def post(self,request):
                    serializer= URLSerializer(data= request.data)
                    request.data["hashed_url"]= hash_url(request.data["original_url"])
                    
                    if serializer.is_valid():
                              serializer.save()
                              return Response(serializer.data,status= status.HTTP_201_CREATED)
                    return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)

#Called when the url ==> 'http://localhost:8000/urls/<str:url_id>/' is called. There are two method that was 
#implemented, one is to get a specific URL data and the second is to delete a specific url from the URLS List 
class URLDetails(APIView):
                    
          #to return the specific url to the client
          def get(self,request,hashed_url):
                    url= URL.objects.filter(hashed_url="http://localhost:8000/"+hashed_url).first()
                    if(url):
                              serializer= URLSerializer(url)
                              return Response(serializer.data)
                    else:
                             return Response(status= status.HTTP_404_NOT_FOUND) 
          #to delete the specific url from the URLs List
          def delete(self,request,hashed_url):
                    found= URL.objects.filter(hashed_url="http://localhost:8000/"+hashed_url).first()
                    if(found):
                              found.delete()
                              return Response(status= status.HTTP_204_NO_CONTENT)
                    else: 
                              return Response(status= status.HTTP_404_NOT_FOUND)

#Called when the url ==> 'http://localhost:8000/<str:url_id>/<str:hashed_url>/' is called. There is one method that was 
#implemented. This method will check if the shortened url is still valid, if so it will redirect the client to the original 
#url for the hashed_url. If the url is not valid anymore -that means the validition period is over- the method will redirect 
#the client to the error page that was provided by the frontend 'http://localhost:3000/error'
class RedirectUrl(APIView):
                    
          #to check if the validation period is not expired and redirect the client to the proper url
          def get(self,request,hashed_url):
                    res= URL.objects.filter(hashed_url="http://localhost:8000/"+hashed_url).first()
                    if(res and is_valid(str(res.creation_date),res.validation_period)):
                              return redirect(res.original_url)         
                    else:
                              return redirect('http://localhost:3000/error')
                   
                              
                    