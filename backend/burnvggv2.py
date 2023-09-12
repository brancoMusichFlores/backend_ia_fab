# Importing necessary modules
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
import keras.backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Flatten
import matplotlib.pyplot as plt
from keras.layers import Dense
from keras.metrics import Precision, Recall
from keras import backend as K
import tensorflow as tf
# VGG
from keras.applications import VGG16
from keras.models import Model
from keras.layers import Dense, Flatten

# Define F1, recall, and precision metrics

# F1 metric


def get_f1(y_true, y_pred):  # taken from old keras source code
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

# F1 Score


def f1_score(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.math.is_nan(f1), tf.zeros_like(f1), f1)

    return K.mean(f1)


# Recall metric


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

# Precision metric


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


# load the pre-trained VGG16 model
vgg_model = VGG16(weights='imagenet', include_top=False,
                  input_shape=(224, 224, 3))

# Freeze the layers in the pre-trained model so they are not trainable
for layer in vgg_model.layers:
    layer.trainable = False

# add new classification layers on top of the VGG16 model
x = Flatten()(vgg_model.output)
x = Dense(units=256, activation='relu')(x)
x = Dense(units=128, activation='relu')(x)
predictions = Dense(units=10, activation='softmax')(x)

# create a new model that includes both the VGG16 base and our new classification layers
model = Model(inputs=vgg_model.input, outputs=predictions)

# compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=[
                  'accuracy', 'categorical_accuracy', Precision(), Recall(), f1_score])

# Part 2 - Fitting the CNN to the images

# Creating training and test data generators
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Defining batch size and number of epochs
batch_size = 10
nb_epoch = 20

# Definir las rutas de los directorios de entrenamiento y prueba para cada clase
train_dir_clase1 = '.\\1er_grado_etiquetado_159\\Train'
train_dir_clase2 = '.\\2do_grado_etiquetado_242\\Train'
train_dir_clase3 = 'C:\\Users\\andre\\Desktop\\DeepLearning\\ProyectoQuemadura\\3er_grado_etiquetado_167\\Train'

test_dir_clase1 = 'C:\\Users\\andre\\Desktop\\DeepLearning\\ProyectoQuemadura\\1er_grado_etiquetado_159\\Test'
test_dir_clase2 = 'C:\\Users\\andre\\Desktop\\DeepLearning\\ProyectoQuemadura\\2do_grado_etiquetado_242\\Test'
test_dir_clase3 = 'C:\\Users\\andre\\Desktop\\DeepLearning\\ProyectoQuemadura\\3er_grado_etiquetado_167\\Test'

# Crear generadores de datos de imágenes para entrenamiento y prueba para cada clase
training_set_clase1 = train_datagen.flow_from_directory(
    train_dir_clase1, target_size=(512, 512), batch_size=batch_size, class_mode='categorical', save_format='jpg')

training_set_clase2 = train_datagen.flow_from_directory(
    train_dir_clase2, target_size=(512, 512), batch_size=batch_size, class_mode='categorical')

training_set_clase3 = train_datagen.flow_from_directory(
    train_dir_clase3, target_size=(512, 512), batch_size=batch_size, class_mode='categorical')

test_set_clase1 = test_datagen.flow_from_directory(
    test_dir_clase1, target_size=(512, 512), batch_size=batch_size, class_mode='categorical')

test_set_clase2 = test_datagen.flow_from_directory(
    test_dir_clase2, target_size=(512, 512), batch_size=batch_size, class_mode='categorical')

test_set_clase3 = test_datagen.flow_from_directory(
    test_dir_clase3, target_size=(512, 512), batch_size=batch_size, class_mode='categorical')


# Definir los generadores de datos de imágenes para entrenamiento y prueba
train_generator = [training_set_clase1, training_set_clase2, training_set_clase3]
test_generator = [test_set_clase1, test_set_clase2, test_set_clase3]

# Definir el número total de pasos por época para cada generador
train_steps_per_epoch = len(training_set_clase1) + len(training_set_clase2) + len(training_set_clase3)
test_steps_per_epoch = len(test_set_clase1) + len(test_set_clase2) + len(test_set_clase3)

# Ajustar el modelo utilizando los generadores de datos de imágenes
# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_steps_per_epoch,
    epochs=nb_epoch,
    validation_data=test_generator,
    validation_steps=test_steps_per_epoch
)


# Part 3 - Evaluating the CNN on the test set

# evaluate the trained model on the test set
#scores = model.evaluate_generator(test_set)

# Generar predicciones utilizando el generador de prueba
predictions = model.predict_generator(test_generator)

# Realizar predicciones en un conjunto de datos separado
x_test, y_test = test_set_clase1.next()
y_pred = model.predict(x_test)


# Evaluate the trained model on the test set
scores = model.evaluate_generator(test_generator)

# Print the evaluation metrics
for i in range(len(model.metrics_names)):
    print("\n%s: %.2f%%" % (model.metrics_names[i], scores[i]*100))

# Generate predictions on the test set
predictions = model.predict_generator(test_generator)

# Convert the predictions from one-hot encoding to integers
y_pred_int = np.argmax(predictions, axis=1)

# Get the true labels for the test set
y_true = np.concatenate([test_generator[i][1] for i in range(len(test_generator))])

# Compute the confusion matrix
conf_matrix = confusion_matrix(y_true, y_pred_int)

# Print the confusion matrix
print(conf_matrix)

# Visualize the confusion matrix
plt.figure(figsize=(5, 5))
sns.heatmap(conf_matrix, annot=True, cmap="Blues", cbar=False, fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
