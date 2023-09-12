# Flask libraries
from flask import Flask, jsonify, request
# AWS libraries
import boto3
# IA libraries
from tensorflow.keras.models import model_from_json
from keras.metrics import Precision, Recall
import tensorflow as tf
from keras import backend as K
from keras.preprocessing import image
# numpy 
import numpy as np
#python
import requests
import base64

def f1_score(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true * y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.math.is_nan(f1), tf.zeros_like(f1), f1)

    return K.mean(f1)

app = Flask(__name__)

@app.route("/analisis/", methods=["POST"])
def analisis():
    request_data = request.get_json()
    decoded_img = base64.b64decode(request_data['img'])
    img_file = open('image.jpg', 'wb')
    img_file.write(decoded_img)
    img_file.close()
    img = image.load_img('image.jpg', target_size=(512, 512))
    img = image.img_to_array(img)
    img = img / 255.0  # Normalize pixel values (assuming you did this during training)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    radius = 5000
    type = "hospital"
    keyword = "hospital"
    api_token = "AIzaSyDrMt45YZXTFdhnfhB-wbPWRU_IFgKZwn4"
    session = boto3.Session(profile_name='default')
    table_name = "first-aid-burn"
    dynamodb_resource = session.resource("dynamodb", region_name='us-east-1')
    fab_table = dynamodb_resource.Table(table_name)
    with open('model_architecture.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('model_weights.h5')
    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy',
                metrics=[
                    'accuracy', 'categorical_accuracy', Precision(), Recall(), f1_score])
    predictions = loaded_model.predict(img)
    predicted_class_index = np.argmax(predictions, axis=1) + 1
    predicted_class_index = str(predicted_class_index).replace('[', '').replace(']', '') if predicted_class_index > 0 and predicted_class_index < 4 else "2"
    response_dynamo = fab_table.get_item(
        Key={
            "grado": predicted_class_index,
        }
    )
    item = response_dynamo.get('Item', {})
    cuidados = item.get('cuidados', False)
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={request_data['coordenadas']}&radius={radius}&type={type}&keyword={keyword}&key={api_token}"
    response = requests.get(url)
    data = response.json()
    nearest_hospital = ''
    if "results" in data:
        hospitals = data["results"]
        if hospitals:
            nearest_hospital = hospitals[0]['name']
    grado = ''
    necesita_hospital = 'si'
    if predicted_class_index == "1":
        grado = "Primer grado"
        necesita_hospital = 'no'
    elif predicted_class_index == "2":
        grado = "Segundo grado"
    else:
        grado = "Tercer grado"
    
    return jsonify('{"hospital": "' + nearest_hospital  + '", "resultado" : "'+ grado +'", "cuidados" :'+ str(cuidados).replace("\'",'"') +', "necesita_hospital" : "' + necesita_hospital +'"}')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)