from flask import Flask, render_template, request, redirect, url_for,session


import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session to work

# Load the trained model (replace with the actual model file path)
try:
    with open('xgboost_model.pkl', 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    # Ensure that the uploads folder exists
UPLOAD_FOLDER = 'static/uploads'
app.config['upload'] = UPLOAD_FOLDER

# Allowed file extensions (you can modify this to fit your needs)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def first():
    return render_template('index.html')

##-------User login-------##
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password matches
        user = users.get(username)
        if user and user['password'] == password:
            session['logged_in'] = True
            return redirect(url_for('services'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')
##-------------- User Register ------------------##
users = {}  # Dictionary to store users, e.g., {username: {'password': password, 'email': email}}

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            return render_template('register.html', error="Username already taken")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")
        
        # Store the user in the dictionary
        users[username] = {'email': email, 'password': password}
        return redirect(url_for('login'))
    
    return render_template('register.html')
##---------------About---------------------##
@app.route('/about')
def about():
    return render_template('about.html')

##------------------------------------##
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/client')
def client():
    return render_template('client.html')

##-----------Contact---------------##
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services', methods=["GET", "POST"])
def services():
    if 'logged_in' not in session:  # Check if the user is logged in
        print("User not logged in, redirecting to login")  # Debugging line
        return redirect(url_for('login'))  # Redirect to login if not logged in
    

    if request.method == 'POST':
        try:
            # Extract and process inputs from the form, ensuring correct data types
            BeneID = int(request.form['BeneID'])
            DOB = int(request.form['DOB'])
            DOD = int(request.form['DOD'])
            Gender = int(request.form['Gender'])
            Race = int(request.form['Race'])
            RenalDiseaseIndicator = float(request.form['RenalDiseaseIndicator'])
            State = int(request.form['State'])
            County = int(request.form['County'])
            NoOfMonths_PartACov = int(request.form['NoOfMonths_PartACov'])
            NoOfMonths_PartBCov = int(request.form['NoOfMonths_PartBCov'])
            ChronicCond_Alzheimer = int(request.form['ChronicCond_Alzheimer'])
            ChronicCond_Heartfailure = int(request.form['ChronicCond_Heartfailure'])
            ChronicCond_KidneyDisease = int(request.form['ChronicCond_KidneyDisease'])
            ChronicCond_Cancer = int(request.form['ChronicCond_Cancer'])
            ChronicCond_ObstrPulmonary = int(request.form['ChronicCond_ObstrPulmonary'])
            ChronicCond_Depression = int(request.form['ChronicCond_Depression'])
            ChronicCond_Diabetes = int(request.form['ChronicCond_Diabetes'])
            ChronicCond_IschemicHeart = int(request.form['ChronicCond_IschemicHeart'])
            ChronicCond_Osteoporasis = int(request.form['ChronicCond_Osteoporasis'])
            ChronicCond_rheumatoidarthritis = int(request.form['ChronicCond_rheumatoidarthritis'])
            ChronicCond_stroke = int(request.form['ChronicCond_stroke'])
            IPAnnualReimbursementAmt = int(request.form['IPAnnualReimbursementAmt'])
            IPAnnualDeductibleAmt = int(request.form['IPAnnualDeductibleAmt'])
            OPAnnualReimbursementAmt = int(request.form['OPAnnualReimbursementAmt'])
            OPAnnualDeductibleAmt = int(request.form['OPAnnualDeductibleAmt'])
            Provider = int(request.form['Provider'])
            
            # Combine all features into a list
            features = [
                BeneID, DOB, DOD, Gender, Race, RenalDiseaseIndicator, State, County,
                NoOfMonths_PartACov, NoOfMonths_PartBCov, ChronicCond_Alzheimer,
                ChronicCond_Heartfailure, ChronicCond_KidneyDisease, ChronicCond_Cancer,
                ChronicCond_ObstrPulmonary, ChronicCond_Depression, ChronicCond_Diabetes,
                ChronicCond_IschemicHeart, ChronicCond_Osteoporasis, ChronicCond_rheumatoidarthritis,
                ChronicCond_stroke, IPAnnualReimbursementAmt, IPAnnualDeductibleAmt,
                OPAnnualReimbursementAmt, OPAnnualDeductibleAmt, Provider
            ]
            
             # Make prediction
            prediction = model.predict([features])
            # Handle the float nature of prediction values and ensure comparison is done correctly
            result = "Fraud" if prediction[0] == 1.0 else "NO FRAUD"
            
            return render_template('services.html', prediction=result)

        except Exception as e:
            return render_template('services.html', prediction="Error: " + str(e))
# Handle file upload logic
    if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = os.path.join(app.config['upload'], file.filename)
                file.save(filename)
                return render_template('services.html', prediction="File uploaded successfully")
            else:
                return render_template('services.html', prediction="Invalid file type. Please upload an image file.")
    
    # For GET request, just render the form
    return render_template('services.html')
@app.route('/logout')
def logout():
     session.pop('logged_in', None)  # Remove 'logged_in' from session to log out
     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
