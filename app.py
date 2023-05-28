from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

# Initialise the Flask app
app = Flask(__name__)

# Use pickle to load in the pre-trained model
model = pickle.load(open("Models/saved_model.pkl", 'rb'))


# Set up the main route
@app.route('/', methods=["GET", "POST"])
def main():
    prediction = [[]]
    flag = ''
    if request.method == "POST":
        # Extract the input from the form
        Age = request.form.get('Age')
        Sex = request.form.get('Sex')
        Job = request.form.get('Job')
        Housing = request.form.get('Housing')
        Credit_amount = request.form.get('Credit_amount')
        Duration = request.form.get('Duration')
        Purpose = request.form.get('Purpose')

        list_of_attributes = []

        purposes = ['car', 'domestic appliances', 'education', 'furniture/equipment', 'radio/tv', 'repairs',
                    'vacation/others']

        if Purpose.lower() not in purposes:
            flag = "You have entered the wrong purpose"
            return render_template("index.html", result=flag)

        genders = ["male", "female"]

        if Sex.lower() not in genders:
            flag = "You have entered the wrong gender"
            return render_template("index.html", result=flag)

        list_of_attributes.append(int(Age))
        list_of_attributes.append(int(Job))
        list_of_attributes.append(int(Credit_amount))
        list_of_attributes.append(int(Duration))
        list_of_attributes.append(1 if Purpose.lower() == 'car' else 0)
        list_of_attributes.append(1 if Purpose.lower() == 'domestic appliances' else 0)
        list_of_attributes.append(1 if Purpose.lower() == 'education' else 0)
        list_of_attributes.append(1 if Purpose.lower() == 'furniture/equipment' else 0)
        list_of_attributes.append(1 if Purpose.lower() == 'radio/tv' else 0)
        list_of_attributes.append(1 if Purpose.lower() == 'repairs' else 0)
        list_of_attributes.append(1 if Purpose.lower() == 'vacation/others' else 0)
        list_of_attributes.append(1 if Sex.lower() == 'male' else 0)
        list_of_attributes.append(1 if Housing.lower() == 'own' else 0)
        list_of_attributes.append(1 if Housing.lower() == 'rent' else 0)

        print("List of attributes: ", list_of_attributes)

        input_to_be_predicted = np.array([list_of_attributes])

        print("Input: ", input_to_be_predicted)

        # Get the model's prediction

        prediction = model.predict(input_to_be_predicted)

        print("Prediction is", prediction)

        result = prediction[0]

        if result == 0 or int(Credit_amount) >= 15000:
            flag = 'The applicant is risky'
        else:
            flag = 'The applicant is safe'
        # We now pass on the input from the form and the prediction to the index page
        return render_template("index.html", result=flag)
    # If the request method is GET
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
