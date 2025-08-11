import numpy as np
import pandas as pd
from keras import backend as K
import tensorflow as tf
from keras.models import Sequential, load_model
import sys
from random import choices, sample
import argparse

############################################################
#                                                          #
#                     input paramerters                    #
#                                                          #
############################################################

parser = argparse.ArgumentParser(
    description="DeepPATT: An explainable deep learning model for decoding RNA Pol II pausing and transcription termination dynamics."
)

parser.add_argument(
    "-a", required=True, metavar="SEQ_CSV",
    help="Path to the one-hot encoded sequence CSV file"
)

parser.add_argument(
    "-m", required=True, metavar="MODEL_PATH",
    help="Path to the trained DeepPATT model file"
)

parser.add_argument(
    "-o", required=True, metavar="OUTPUT_DIR",
    help="Path to the output directory"
)

args = parser.parse_args()

############################################################
#                                                          #
#                         analysis                         #
#                                                          #
############################################################

X = pd.read_csv(args.a, index_col = 0)
X_test = np.array(X)
X_test1 = np.array(X_test).reshape(X_test.shape[0], X_test.shape[1], 1)


p_values_list = []
for i in range(5):
    mdl_path = args.m + "/model."+str(i)+".hdf5"
    temp_model = tf.keras.models.load_model(mdl_path)
    y_test_pred = temp_model.predict(X_test)
    p_values_list.append(y_test_pred[:,1])
    K.clear_session()


p_values_array = np.array(p_values_list)
mean_p_values = np.mean(p_values_array, axis=0)
pd.DataFrame({'ID':X.index, 'Pausing probability':mean_p_values.flatten()}).to_csv(args.o+"/prediction.csv")
