from rest_framework import serializers
from .models import URL

#serializer to serialize the data according to the model provided
class URLSerializer(serializers.ModelSerializer):
         class Meta:
                   model= URL
                   fields=['url_id', 'original_url', 'hashed_url', 'validation_period', 'creation_date','valid']

         