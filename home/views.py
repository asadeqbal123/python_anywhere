from rest_framework.decorators import api_view
from rest_framework.response import Response
import opennsfw2 as n2
from PIL import Image
import numpy as np
import urllib.request
import io

# Load and preprocess image.



@api_view(['GET'])
def image(request):
    try:
        # Read the image data into memory
        url = request.GET.get('search')
        if not url:
            return Response({'error': 'No URL provided'}, status=400)
        
        if url.endswith('.mp4'):
            # The video can be in any format supported by OpenCV.
            video_path = url
            elapsed_seconds, nsfw_probabilities = n2.predict_video_frames(video_path)
            result2 = (f'elapsed time: {elapsed_seconds[100]} unsafe: {nsfw_probabilities[100] * 100:.2f}%')
            return Response(result2)
        
        else:
            with urllib.request.urlopen(url) as response:
                image_data = response.read()

            # Convert the image data into a Python Image object
                image = Image.open(io.BytesIO(image_data))

            # Preprocess the rotated image for the model
                preprocessed_image = n2.preprocess_image(image, n2.Preprocessing.YAHOO)

            # Create the model and make predictions
                model = n2.make_open_nsfw_model()
                inputs = np.expand_dims(preprocessed_image, axis=0)  # Add batch axis (for single image).
                predictions = model.predict(inputs)

            # Output the predictions
                sfw_probability, nsfw_probability = predictions[0]
                result = (f'safe: {sfw_probability * 100:.2f}%, unsafe: {nsfw_probability * 100:.2f}%')
                return Response(result)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

    
