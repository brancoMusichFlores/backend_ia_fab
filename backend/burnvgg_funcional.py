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
                  input_shape=(512, 512, 3))

# Freeze the layers in the pre-trained model so they are not trainable
for layer in vgg_model.layers:
    layer.trainable = False

# add new classification layers on top of the VGG16 model
x = Flatten()(vgg_model.output)
x = Dense(units=256, activation='relu')(x)
x = Dense(units=128, activation='relu')(x)
predictions = Dense(units=3, activation='softmax')(x)

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

# Creating training and test sets from directory of images
training_set = train_datagen.flow_from_directory(
    '.\Train', target_size=(512, 512), batch_size=batch_size)

test_set = test_datagen.flow_from_directory(
    '.\Prueba', target_size=(512, 512), batch_size=batch_size)

# Fitting the CNN to the training set
history = model.fit(
    training_set, epochs=nb_epoch, validation_data=test_set)

# Part 3 - Evaluating the CNN on the test set

# evaluate the trained model on the test set
scores = model.evaluate(test_set)

# print the evaluation metrics
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print("\n%s: %.2f%%" % (model.metrics_names[2], scores[2]*100))
print("\n%s: %.2f%%" % (model.metrics_names[3], scores[3]*100))
print("\n%s: %.2f%%" % (model.metrics_names[4], scores[4]*100))
print("\n%s: %.2f%%" % (model.metrics_names[5], scores[5]*100))

# generate predictions on the test set
y_pred = model.predict(test_set)

# create a confusion matrix to analyze the predictions

# convert the predictions from one-hot encoding to integers
y_pred_int = np.argmax(y_pred, axis=1)

# get the true labels for the test set
y_true = test_set.classes

# compute the confusion matrix
conf_matrix = confusion_matrix(y_true, y_pred_int)


# Save the model architecture to a JSON file
model_architecture = model.to_json()
with open('model_architecture.json', 'w') as json_file:
    json_file.write(model_architecture)

# Save the trained weights to an HDF5 file
model.save_weights('model_weights.h5')

# print the confusion matrix
print(conf_matrix)

# visualize the confusion matrix

plt.figure(figsize=(5, 5))
sns.heatmap(conf_matrix, annot=True, cmap="Blues", cbar=False, fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
