import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
import base64
from io import BytesIO
from models.recommender.rec import recs_essentials, makeup_recommendation
from models.skin_tone.skintone import identify_skin_tone


app = Flask(__name__)
api = Api(app)

class_names1 = ['dry', 'normal', 'oily']
class_names2 = ['very low', 'low', 'moderate', 'severe']
skin_tone_dataset = 'models/skin_tone/skin_tone_dataset.csv'

# Load models
model1 = load_model('./models/skin_model')
model2 = load_model('./models/acne_model')


# Create a function to import an image and resize it to be able to be used with our model
def load_and_prep_image(filename, img_shape=224):
  """
  Reads in an image from filename, turns it into a tensor and reshapes into (224,224,3).
  """
  # Read in the image
  img = tf.io.read_file(filename)
  # Decode it into a tensor
  img = tf.image.decode_jpeg(img)
  # Resize the image
  img = tf.image.resize(img, [img_shape, img_shape])
  # Rescale the image (get all values between 0 and 1)
  img = img/255.
  return img


def prediction_skin(img_path):
    try:

        # Import the target image and preprocess it
        img = load_and_prep_image(img_path)

        # Make a prediction
        pred = model1.predict(tf.expand_dims(img, axis=0))

        # Add in logic for multi-class & get pred_class name
        if len(pred[0]) > 1:
            pred_class = class_names1[tf.argmax(pred[0])]
        else:
            pred_class = class_names1[int(tf.round(pred[0]))]        
        
        return pred_class
    except Exception as e:
        return str(e)


def prediction_acne(img_path):
    try:
        # Import the target image and preprocess it
        img = load_and_prep_image(img_path)

        # Make a prediction
        pred = model2.predict(tf.expand_dims(img, axis=0))

        # Add in logic for multi-class & get pred_class name
        if len(pred[0]) > 1:
            pred_class = class_names2[tf.argmax(pred[0])]
        else:
            pred_class = class_names2[int(tf.round(pred[0]))]        
        
        return pred_class
    except Exception as e:
        return str(e)


img_put_args = reqparse.RequestParser()
img_put_args.add_argument("file", help="Please provide a valid image file", required=True)

rec_args = reqparse.RequestParser()
rec_args.add_argument("tone", type=int, help="Tone argument required", required=True)
rec_args.add_argument("type", type=str, help="Type argument required", required=True)
rec_args.add_argument("features", type=dict, help="Features argument required", required=True)


class Recommendation(Resource):
    def put(self):
        try:
            args = rec_args.parse_args()
            features = args['features']
            tone = args['tone']
            skin_type = args['type'].lower()

            # Determine skin tone based on tone value
            skin_tone = 'light to medium'
            if tone <= 2:
                skin_tone = 'fair to light'
            elif tone >= 4:
                skin_tone = 'medium to dark'

            fv = [int(value) for key, value in features.items()]

            # Replace with actual implementation
            general = recs_essentials(fv, None)
            makeup = makeup_recommendation(skin_tone, skin_type)

            return {'general': general, 'makeup': makeup}, 200
        except Exception as e:
            return {'error': str(e)}, 500


class SkinMetrics(Resource):
    def put(self):
        try:
            args = img_put_args.parse_args()
            file = args['file']
            starter = file.find(',')
            image_data = file[starter + 1:]
            image_data = bytes(image_data, encoding="ascii")
            im = Image.open(BytesIO(base64.b64decode(image_data)))

            filename = 'image.png'
            file_path = os.path.join('./static', filename)
            im.save(file_path)

            skin_type = prediction_skin(file_path).split('_')[0]
            acne_type = prediction_acne(file_path)
            tone = identify_skin_tone(file_path, dataset=skin_tone_dataset)

            return {'type': skin_type, 'tone': str(tone), 'acne': acne_type}, 200
        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(SkinMetrics, "/upload")
api.add_resource(Recommendation, "/recommend")


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            filename = file.filename
            file_path = os.path.join('./static', filename)
            file.save(file_path)
            skin_type = prediction_skin(file_path)
            acne_type = prediction_acne(file_path)
            tone = identify_skin_tone(file_path, dataset=skin_tone_dataset)
            return render_template('predict.html', skin_type=skin_type, acne_type=acne_type,tone=str(tone))
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    app.run(debug=True)
