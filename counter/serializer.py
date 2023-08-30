from rest_framework import serializers
from counter.models import images

class imageserializer(serializers.ModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = images
        fields = ('id','image')