import json
import joblib
import pickle
import numpy as np
import pandas as pd
import azureml.train.automl
from azureml.core.model import Model

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


# Called when the service is loaded
def init():
    global model
    # Get the path to the deployed model file and load it
    model_path = Model.get_model_path('stock_model')
    model = joblib.load(model_path)

# providing 3 sample inputs for schema generation
numpy_sample_input = NumpyParameterType(np.array([[514.390015,515.630005,505.369995], [513.000000,517.979980,510.369995]],dtype='float64'))

# This is a nested input sample, any item wrapped by `ParameterType` will be described by schema
sample_input = StandardPythonParameterType({'data': numpy_sample_input})
sample_output = StandardPythonParameterType([[509.12305715658124], [515.6020041775826]])
outputs = StandardPythonParameterType({'Results':sample_output}) # 'Results' is case sensitive

@input_schema('Inputs', sample_input) 
# 'Inputs' is case sensitive

@output_schema(outputs)

# Called when a request is received
def run(Inputs):
    # Get the input data as a numpy array
    inputData = Inputs['data']
    # data = np.array(json.loads(inputData)['data'])
    # data = json.loads(inputData)
    print(inputData)
    # Get a prediction from the model
    predictions = model.predict(inputData)
    print(predictions)
    # result= pd.DataFrame({'Actual':inputData.flatten(),'Predicted':predictions.flatten()})
    return json.dumps(predictions.tolist())
    
