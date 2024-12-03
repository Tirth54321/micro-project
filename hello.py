from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret_key"  # Needed for flash messages

# Store patient data globally
patients = []
SECRET_CODE = "1234"

@app.route('/', methods=['GET', 'POST'])
def index():
    global patients  # Declare global at the top of the functionA
    current_time = datetime.now()
    
    # Remove patients who missed their appointment
    patients = [p for p in patients if current_time < p['appointment_time'] + timedelta(minutes=10)]

    if request.method == 'POST' and 'cancel_token' in request.form:
        # Cancel appointment logic
        token_to_cancel = int(request.form['cancel_token'])
        entered_code = request.form['cancel_code']

        if entered_code == SECRET_CODE:
            # Find and remove the patient by token
            patients = [p for p in patients if p['token'] != token_to_cancel]
            flash(f"Appointment with Token {token_to_cancel} has been canceled.", "success")
        else:
            flash("Invalid cancellation code.", "error")
        return redirect(url_for('index'))

    elif request.method == 'POST':
        # Booking logic
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        problem = request.form['problem']

        # Calculate token and appointment time
        token_number = len(patients) + 1
        appointment_time = datetime.now() + timedelta(minutes=10 * (token_number - 1))

        # Add patient details
        patient = {
            'token': token_number,
            'name': name,
            'age': age,
            'phone': phone,
            'problem': problem,
            'appointment_time': appointment_time
        }
        patients.append(patient)
        flash(f"Appointment confirmed! Token: {token_number}, Time: {appointment_time.strftime('%I:%M %p')}", "success")
        return redirect(url_for('index'))

    return render_template('index.html', doctor_name="Dr. Rohan", qualification="MBBS", patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
