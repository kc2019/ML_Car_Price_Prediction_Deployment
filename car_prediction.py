from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
#from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model_pickle', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    #return render_template('index.html')
    return render_template('car_prediction.html')

# we don't need to scale down here, as Random Forest, Decession Tree don't require this
#standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        year = int(request.form['year'])
        present_price=float(request.form['present_price'])
        kms_driven=int(request.form['kms_driven'])
        kms_driven2=np.log(kms_driven)
        owner=int(request.form['owner'])
        fuel_type=request.form['fuel_type']
        if(fuel_type=='Petrol'):
                fuel_type_petrol=1
                fuel_type_diesel=0
        elif (fuel_type=='Diesel'):
                fuel_type_petrol=0
                fuel_type_diesel=1
        else:
            fuel_type_petrol=0
            fuel_type_diesel=0
        #Year=2020-Year
        year=2021-year
        seller_type=request.form['seller_type']
        if(seller_type=='Individual'):
            seller_type=1
        else:
            seller_type=0	
        transmission=request.form['transmission']
        if(transmission=='Mannual'):
            transmission=1
        else:
            transmission=0
        #prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        prediction=model.predict([[present_price,kms_driven2,owner,year,fuel_type_diesel,fuel_type_petrol,seller_type,transmission]])

        output=round(prediction[0],2)
        if output<0:
            #return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
            return render_template('car_prediction.html',prediction_text="Sorry you cannot sell this car")
        else:
            #return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
            return render_template('car_prediction.html',prediction_text="You Can Sell The Car at {} lakhs".format(output))
    else:
        #return render_template('index.html')
        return render_template('car_prediction.html')

if __name__=="__main__":
    app.run(debug=True)

