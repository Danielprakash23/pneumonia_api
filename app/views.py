from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from .llm_model import get_pneumonia_suggestions

from .models import PneumoniaDetail
from .serializers import PhenmoniaDetailSerializer

# Load the trained model
model = tf.keras.models.load_model("app/model.h5")

def predict_pneumonia(file_path):
    # Process the image
    img = image.load_img(file_path, target_size=(28, 28), color_mode="grayscale")
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    prediction = model.predict(img_array)
    print(prediction)
    result = "Pneumonia Detected" if prediction[0][0] > 0.5 else "Healthy"

    return prediction[0][0], result

import os
from django.conf import settings

class PneumoniaList(APIView):
    
    def post(self, request):
        
        try:
            host_name = str(request.META['HTTP_HOST'])
            host_url = 'http://'
            media_data = getattr(settings, "MEDIA_URL", None)
            media_folder = getattr(settings, "MEDIA_ROOT", None)
            pneumonia_url_data = getattr(settings, "PNEUMONIA_PATH_URL", None)
            pneumonia_folder_path = os.path.join(media_folder, pneumonia_url_data)
            
            if not os.path.exists(pneumonia_folder_path):
                os.makedirs(pneumonia_folder_path)
            
            uploaded_file = request.FILES["image"]
            
            file_name = str(uploaded_file).replace(" ", "-")
            file_path = os.path.join(pneumonia_folder_path, file_name)
            
            fs = FileSystemStorage(location=pneumonia_folder_path)
            if os.path.isfile(file_path):
                file_name = fs.save(file_name, uploaded_file)
                file_output = file_name
            else:
                file_output = fs.save(file_name, uploaded_file)
            
            data_url = media_data + pneumonia_url_data + '/' + str(file_name)
            
            image_path = host_url + host_name  + data_url
            
            req_data = request.POST
            
            predict, result = predict_pneumonia(file_path)
            
            suugestion_bool, suggestion_data = get_pneumonia_suggestions(int(req_data['age']), predict * 100)
            
            data = {
                'image': image_path,
                'age': int(req_data['age']),
                'gender': req_data['gender'],
                'city':req_data['city'],
                'severity_level': round(predict * 100, 2),
                'suggestion': suggestion_data,
                'result': result,
                'user_id': int(req_data['user_id'])
            }
            
            serializer = PhenmoniaDetailSerializer(data = data)
            
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)
            
            response_data = serializer.data
            
            return Response(response_data)
        except Exception as e:
            print(str(e))
    
    def get(Self, request):
        
        try:
            
            user_id = request.GET.get('user_id', None)
            
            if not user_id:
                return Response({"message": "Authentication Required"})
            
            user_id = int(user_id)
            queryset = PneumoniaDetail.objects.filter(user_id=user_id)
            
            serializer = PhenmoniaDetailSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "Authentication Required"})