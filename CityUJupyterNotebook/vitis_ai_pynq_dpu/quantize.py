import os
 
# Silence TensorFlow messages
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import tensorflow.keras.models as models
from tensorflow_model_optimization.quantization.keras import vitis_quantize

MODEL_DIR = './' # Output directory
FLOAT_MODEL = 'float_model.h5'
QAUNT_MODEL = 'quantized_model.h5'

# Loading the float model
print('Loading the float model...')
path = os.path.join(MODEL_DIR, FLOAT_MODEL)
try:
    float_model = models.load_model(path)
except:
    print('\nError:loading float model failed!')

print("\nLoading the Fashion MNIST dataset...")
# Loading the Fashion MNIST dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
# Reshaping the data and feature scaling
x_train = x_train.astype('float32')/255 #feature scaling (Hint:255 is the maximum pixel value)

num_classes = 10 #no. of classes

train_one_hot = tf.keras.utils.to_categorical(y_train,num_classes) #one hot encoding for the training set
test_one_hot = tf.keras.utils.to_categorical(y_test,num_classes)   #one hot encdoing for the testing set

INPUT_SHAPE = [28,28,1]

x_train = x_train.reshape([-1]+INPUT_SHAPE)
print(f'Train data shape: {x_train.shape}, Test data shape: {x_test.shape}')
# Defining the calibration dataset using about 1000 samples from the training set
calib_dataset = x_train[:1000]

print('\nRunning model quantization...')
# Running model quantization

quantizer = vitis_quantize.VitisQuantizer(float_model)
quantized_model = quantizer.quantize_model(calib_dataset=calib_dataset) 

# Saving the quantized model
path = os.path.join(MODEL_DIR, QAUNT_MODEL)
quantized_model.save(path)

print(f'\nQuantized model has been saved to "{path}"')
#================================================================================
