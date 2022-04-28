# Imports
import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import os

# First thing: Load the model in memory, faster code
model = pickle.load(open('model/model_rossmann.pkl', 'rb'))

# The API handler needs a library that interact with web interfaces, like Flask
app = Flask(__name__)

# Create end-point | route, The URL that will provide data.
@app.route('/rossmann/predict', methods=['POST'])

# When the end-point receives a call, the first function below is executed:
def rossmann_predict():
    
    # Get the data sent via POST
    test_json = request.get_json()

    # Check if the data exist
    if test_json: 
        
        # Check if is a dict (only 1 json) else many different jsons with keys
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        # Instantiate Rossmann class
        pipeline = Rossmann()
        
        # Data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        
        # Feature engineering
        df2 = pipeline.feature_engineering(df1)
        
        # Data preparation
        df3 = pipeline.data_preparation(df2)
        
        # Prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
        
        return  df_response
        
       
    else:
        return Response('{}', status=200, mimetype='application/json')

    
# Flask will run in localhost
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run('0.0.0.0', port=port)