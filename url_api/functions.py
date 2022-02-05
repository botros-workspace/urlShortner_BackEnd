import hashlib
from datetime import date

#to hash the given url using hashlib provided by python 
def hash_url(url,id):
         hash_object =  hashlib.md5(url.encode())
         return ('http://localhost:8000/'+id+'/' + hash_object.hexdigest())

#this function takes 2 variables and check if the validation period is not expired compared to the current date
def is_valid(creation_day, duration):
          d=creation_day.split("-")
          a = date(int(d[0]),1,10)
          today = date.today()
          b = date(int(today.strftime("%Y")),int(today.strftime("%m")),int(today.strftime("%d")))
          if((b-a).days>duration):
                    return False
          else:
                    return True

     