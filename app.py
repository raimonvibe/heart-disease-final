from flask import Flask,render_template,redirect,url_for,request,session,g,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
import json
from datetime import datetime 
import re
from admin.routes import routes
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'heart_disease_prediction_secret_key_123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True

db = SQLAlchemy(app)

# Form klasse
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=10)])
    Pro = SelectField('Profession', choices=[
        ('Student', 'Student'),
        ('Engineer', 'Engineer'),
        ('Doctor', 'Doctor'),
        ('Other', 'Other')
    ])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Define ALL models first
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(120), unique=False, nullable=False)
    Password = db.Column(db.String(120), unique=False, nullable=False)

class Doclogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(120), unique=False, nullable=False)
    Lastname = db.Column(db.String(120), unique=False, nullable=False)
    Ph = db.Column(db.Integer, unique=False, nullable=False)
    Profession = db.Column(db.String(120), unique=False, nullable=False)
    Email = db.Column(db.String(20), unique=False, nullable=False)
    Username = db.Column(db.String(120), unique=False, nullable=False)
    Password = db.Column(db.String(120), unique=False, nullable=False)

class Hdpuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(120), unique=False, nullable=False)
    LastName = db.Column(db.String(120), unique=False, nullable=False)
    Email = db.Column(db.String(20), unique=False, nullable=False)
    Ph_no = db.Column(db.Integer, unique=False, nullable=False)
    Profession = db.Column(db.String(12), unique=False, nullable=False)
    Username = db.Column(db.String(120), unique=False, nullable=False)
    Password = db.Column(db.String(120), unique=False, nullable=False)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(120), unique=False, nullable=False)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Age = db.Column(db.Integer, unique=False, nullable=False)
    Sex = db.Column(db.Integer, unique=False, nullable=False)
    Cp = db.Column(db.Integer, unique=False, nullable=False)
    Trestbps = db.Column(db.Integer, unique=False, nullable=False)
    Chol = db.Column(db.Integer, unique=False, nullable=False)
    Fbs = db.Column(db.Integer, unique=False, nullable=False)
    Restecg = db.Column(db.Integer, unique=False, nullable=False)
    Thalach = db.Column(db.Integer, unique=False, nullable=False)
    Exang = db.Column(db.Integer, unique=False, nullable=False)
    Oldpeak = db.Column(db.Integer, unique=False, nullable=False)
    Slope = db.Column(db.Integer, unique=False, nullable=False)
    Ca = db.Column(db.Integer, unique=False, nullable=False)
    Thal = db.Column(db.Integer, unique=False, nullable=False)
    Target = db.Column(db.Integer, unique=False, nullable=False)

# Register blueprint
app.register_blueprint(routes, url_prefix='')

# Now create all tables
with app.app_context():
    db.create_all()
    # Add admin if not exists
    existing_admin = Admin.query.filter_by(Username="admin").first()
    if not existing_admin:
        admin = Admin(Username="admin", Password="admin123")
        db.session.add(admin)
        db.session.commit()

@app.route('/doctorlogin', methods=['GET', 'POST'])
def doclogin():
    msg = ""
    if request.method == 'POST':
        uname = request.form['username'] 
        passd = request.form['password']
        user1 = Doclogs.query.filter_by(Username = uname).first()
        pass1 = user1.Password
        if user1 and  passd==pass1:
            session['user'] = uname
            return render_template('docindex.html', user1 = user1)
        else:
            msg = "Wrong Credentials !"
    
    return render_template('doclogin.html',msg=msg)
    
       
@app.route('/dash')
def dash():
    
    d = Dataset.query.all()
    co = Hdpuser.query.all()
    co1 = Doclogs.query.all()
    co2 = Dataset.query.all()
    count = 0
    count1 = 0
    count2 = 0
    for i in co:
        count= count+1
    for i in co1:
        count1= count1+1
    for i in co2:
        count2= count2+1
    c22 = count2//2
    return render_template('dash.html',d = d,count=count,count1=count1,count2=count2,c22=c22)
 

@app.route('/patientlogin', methods=['GET', 'POST'])
def patlog():
     msg = ""
     if request.method == 'POST':
        uname = request.form['username'] 
        passd = request.form['password']
        user1 = Hdpuser.query.filter_by(Username = uname).first()
        pass1 = user1.Password
        if user1 and  passd==pass1:
            session['user'] = uname
           
            return render_template('profilepatient.html',user1=user1)
            
        else:
            msg = "Wrong Credentials !"
     return render_template('patlogin.html',msg = msg)


# @app.route('/form_elements')
# def form_elements():
#     return render_template('form_elements.html')



 
@app.route('/docregis', methods=['GET', 'POST'])
def docregis():
    form = RegistrationForm()  # Create a new form object
    if request.method == 'POST':
        if form.validate_on_submit():  # Check if the form is valid
            # Your registration logic here
            entry = Doclogs(
                Firstname=form.firstname.data,
                Lastname=form.lastname.data,
                Email=form.email.data,
                Ph=form.phone.data,
                Profession=form.Pro.data,
                Username=form.username.data,  # Ensure this field is accessed correctly
                Password=form.password.data
            )
            db.session.add(entry)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('doclogin'))  # Redirect to doctor login
        else:
            flash('Please correct the errors in the form.')

    return render_template('docregis.html', form=form)  # Render the registration template


@app.route('/pattable', methods=['GET', 'POST'])
def adminview():
    c = Hdpuser.query.all()
    return render_template('pattable.html',c = c)

@app.route('/doctable', methods=['GET', 'POST'])
def adminvdoc():
    c = Doclogs.query.all()
    return render_template('doctable.html',c = c)


@app.route('/emailcount',methods=['GET'])
def emailcount():
    c = Emails.query.all() 
    print(c) 
   
    return render_template('emailscount.html',c = c)

@app.route('/heartcheck',methods=['GET', 'POST'])
def heartcheck():
    return render_template("heartcheck.html")
        
     

        

@app.route('/predict',methods=['POST'])
def predict():  
    
    if request.method == 'POST':
   

        model = pickle.load(open(r'D:\keval\study\Projects\hdp\Heart_Disease_Prediction-FLask-\modal2.pkl','rb'))
       
        int_features = [ int(x) for x in request.form.values()]
         
        final_features=[np.array(int_features)]
        
        print(final_features)

        prediction=model.predict(final_features)
        
        output=round(prediction[0],2)
        if output == 1:
            o = "Bad News ! \n Their is a chance that you have a heart disease "
            return render_template('heartcheck.html',prediction_text='Heart status:  {}'.format(o))
        else:
            o =" Good News ! \n Their is a No chance that you have a heart disease ! :) "
            return render_template('heartcheck.html',prediction_text2='Heart status:  {}'.format(o))
        
     
    return redirect('/predict')

@app.route('/docpredict',methods=['POST'])
def docpredict():  
    
    if request.method == 'POST':

        model = pickle.load(open(r'D:\keval\study\Projects\hdp\Heart_Disease_Prediction-FLask-\modal2.pkl','rb'))
        
        int_features = [int(x) for x in request.form.values()]
        final_features=[np.array(int_features)]
        
        print(final_features)

        prediction=model.predict(final_features)
        
        output=round(prediction[0],2)
        if output == 1:
            o = "Bad News ! \n Their is a chance that you have a heart disease "
            return render_template('heartcheck.html',prediction_text='Heart status:  {}'.format(o))
        else:
            o =" Good News ! \n Their is a No chance that you have a heart disease ! :) "
            return render_template('heartcheck.html',prediction_text2='Heart status:  {}'.format(o))

    return redirect('/docpredict')
    
    


        # Age = request.form['age'] 
        # Sex = request.form['sex']
        # Cp = request.form['cp']
        # Trestbps = request.form['trestbps']
        # Cholestrol = request.form['cholestrol'] 
        # Fbs = request.form['Fbs'] 
        # Restecg = request.form['restecg'] 
        # Thalach = request.form['thalach'] 
        # Exang = request.form['exang'] 
        # Oldpeak = request.form['oldpeak'] 
        # Slope = request.form['slope'] 
        # Ca = request.form['ca'] 
        # Thal = request.form['thal'] 

        # return render_template('heartcheck.html', Age=Age, Sex=Sex, Cp=Cp  , Trestbps=Trestbps , Fbs=Fbs , Restecg=Restecg, Thalach=Thalach, Exang=Exang, Oldpeak=Oldpeak , Slope=Slope , Ca=Ca , Thal=Thal )

 #Down here All Are CRUD Opreations oF Database-----

# adminlong 
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST':
        uname = request.form.get('username', '')
        passd = request.form.get('password', '')
        admin = Admin.query.filter_by(Username=uname).first()
        
        if admin and passd == admin.Password:  # Note: Insecure, passwords should be hashed
            session['admin'] = uname
            return redirect(url_for('dash'))  # Assuming 'dash' is the admin dashboard
        else:
            msg = 'Invalid Credentials'
    
    return render_template('admin_login.html', msg=msg)---------------------------------------------------------------------------------------------------------------------------


#Admin view all data of user--------------------------------------------------------------------------------------------
@app.route('/pattable', methods=['GET', 'POST'])
def viewadmin():
    c = Hdpuser.query.all()
    return render_template("pattable.html",c = c)



#Admin view all data of Doctors--------------------------------------------------------------------------------------------
@app.route('/doctable', methods=['GET', 'POST'])
def vdocadmin():
    c = Doclogs.query.all()
    return render_template("doctable.html",c = c)


#Admin editing/updating all data of user-----------------------------------------------------------------------------------
@app.route('/adminup', methods=['GET', 'POST'])
def adminup():
     if request.method == 'POST':
        c = Hdpuser.query.get(request.form.get('id'))
        print(c)
        c.FirstName = request.form['name']
        c.LastName = request.form['name2']
        c.Email = request.form['email']
        c.Ph_no = request.form['phone']
        c.Username = request.form['usern']
        c.Password = request.form['pass']
        db.session.commit()
        flash("Patient detail Updated Successfully")
        return redirect("pattable")


#Admin editing/updating all data of Doctors------------------------------------------------------------------
@app.route('/admindocup', methods=['GET', 'POST'])
def admindocup():
     if request.method == 'POST':
        c = Doclogs.query.get(request.form.get('id'))
        
        c.Fristname = request.form['name']
        c.Lastname = request.form['name2']
        c.Ph = request.form['phone']
        c.Username = request.form['usern']
        c.Password = request.form['pass']
    
        db.session.commit()
        flash("Doctor Details Updated Successfully")
        return redirect("doctable")

#Admin Deleting  data of user------------------------------------------------------------------------
@app.route('/admindel/<id>/', methods = ['GET', 'POST'])
def admindel(id):
    c = Hdpuser.query.get(id)
    db.session.delete(c)
    db.session.commit()
    flash("Patient Deleted Successfully")
    return redirect('/pattable')

#Admin Deleting all data of Doctors-------------------------------------------------------------------
@app.route('/admindeldoc/<id>/', methods = ['GET', 'POST'])
def admindeldoc(id):
    c = Hdpuser.query.get(id)
    db.session.delete(c)
    db.session.commit()
    flash("Doc Deleted Successfully")
    return redirect('doctable')  
 
##Doctor-dashboard-related-code##---------------


@app.route('/viewdatatable')
def viewdatatable():
    ds = Dataset.query.all()
    c=Doclogs.query.filter_by(Username=g.user).first()

    print(c.Email)
    return render_template('datatable.html',ds=ds,c=c)


@app.route('/docindex')
def docindex():
   
    curr=Doclogs.query.filter_by(Username=g.user).first()

    print(curr.Email)
    
    return redirect('docindex')


@app.route('/viewpatient')
def viewpatient():
    patient=Hdpuser.query.all()
    c= Doclogs.query.filter_by(Username=g.user).first()

    return render_template('viewpatient.html',patient=patient,c=c)

@app.route('/userprofile')
def userprofile():
    c= Doclogs.query.filter_by(Username=g.user).first()
    return render_template('userprofile.html',c=c)

@app.route('/docupdate', methods=['GET', 'POST'])
def docupdate():
     if request.method == 'POST':
        d= Doclogs.query.filter_by(Username=g.user).first()
       
        d.Firstname = request.form['name1']
        d.Lastname = request.form['name2']
        d.Email = request.form['email']
        d.Ph = request.form['phone']
        d.Profession = request.form['pro']
        
        db.session.commit()
        flash("Doctor Details Updated Successfully")
        return redirect("userprofile")

@app.route('/profilepat')
def profilepat():
    c= Hdpuser.query.filter_by(Username=g.user).first()
    
    return render_template('profilepatient.html',c = c)

@app.route('/checkheart', methods=['GET', 'POST'])
def checkheart():
    return render_template('checkheart.html')

# payment module  ----------------------------------------------------------------------------------------------------------
@app.route('/payment', methods=['GET', 'POST'])
def payhome():
    return render_template('paymenthome.html')

@app.route('/success')
def success():
    return render_template('paysucces.html')

@app.route('/pay',methods=['POST','GET'])
def pay():
    if request.method == 'POST':
        name = request.form.get('name')
        purpose = request.form.get('purpose')
        email = request.form.get('email')
        amount = request.form.get('amount')
        
        response = api.payment_request_create(
        amount=amount,
        purpose=purpose,
        buyer_name=name,
        send_email=True,
        email=email,
        redirect_url="http://localhost:5000/success"
        )
        
        return redirect(response['payment_request']['longurl'])
    
    else:
        
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Maak een nieuw form object
    if request.method == 'POST' and form.validate():
        email_check = Hdpuser.query.filter_by(Email=form.email.data).first()
        phone_check = Hdpuser.query.filter_by(Ph_no=form.phone.data).first()
        username_check = Hdpuser.query.filter_by(Username=form.username.data).first()

        if email_check:
            flash('Email address already exists')
        elif phone_check:
            flash('Phone number already exists')
        elif username_check:
            flash('Username already taken')
        elif not re.match(r'[789]\d{9}$', form.phone.data):
            flash('Invalid phone number!')
        else:
            entry = Hdpuser(
                FirstName=form.firstname.data,
                LastName=form.lastname.data,
                Email=form.email.data,
                Ph_no=form.phone.data,
                Profession=form.Pro.data,
                Username=form.username.data,
                Password=form.password.data
            )
            db.session.add(entry)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('patlogin'))  # of gebruik 'patientlogin' als dat de juiste route is

    # Geef het form object door aan het template
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
