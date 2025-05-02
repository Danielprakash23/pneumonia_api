from rest_framework import serializers
from .models import PneumoniaDetail


class PhenmoniaDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PneumoniaDetail
        fields = '__all__'