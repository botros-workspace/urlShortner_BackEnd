from django.db import models

#The url model 
class URL(models.Model):
          url_id= models.CharField(max_length=100,primary_key=True,unique=True,auto_created=True)
          original_url= models.CharField(max_length=10000)
          hashed_url= models.CharField(max_length=100)
          validation_period= models.IntegerField(default=3)
          creation_date = models.DateField(auto_now_add=True)
          valid= models.BooleanField(True)

          def __str__(self):
              return self.url_id
