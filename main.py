from flask import Flask, render_template, redirect, url_for
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired

import _pickle as cPickle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'
Bootstrap(app)

class LogInForm(Form):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class CervicalCancerForm(Form):
    age = FloatField('Age', validators=[InputRequired()])
    num_sexual_partners = FloatField('# of Sexual Partners', validators=[InputRequired()])
    pregnancies = FloatField('Pregnancies', validators=[InputRequired()])
    smokes = FloatField('Smokes', validators=[InputRequired()])
    hormonal_contraceptives = FloatField('Takes Contraceptives', validators=[InputRequired()])
    iud = FloatField('Uses Intrauterine Device', validators=[InputRequired()])
    dx_std = FloatField('Diagnosed with STD', validators=[InputRequired()])
    dx_cancer = FloatField('Diagnosed with Other Forms of Cancer', validators=[InputRequired()])
    dx_cin = FloatField('Diagnosed with CIN', validators=[InputRequired()])
    dx_hpv = FloatField('Diagnosed with HPV', validators=[InputRequired()])

class DiabetesForm(Form):
    pregnancies = FloatField('Pregnancies', validators=[InputRequired()])
    glucose = FloatField('Glucose', validators=[InputRequired()])
    blood_pressure = FloatField('Blood Pressure(Systolic)', validators=[InputRequired()])
    skin_thickness = FloatField('Skin Thickness', validators=[InputRequired()])
    insulin = FloatField('Insulin', validators=[InputRequired()])
    height = FloatField('Height(m)', validators=[InputRequired()])
    weight = FloatField('Weight(kg)', validators=[InputRequired()])
    #bmi = FloatField('BMI', validators=[InputRequired()])
    #diabetes_pedigree = FloatField('Diabetes Pedigree Function', validators=[InputRequired()])
    age = FloatField('Age', validators=[InputRequired()])

class FertilityForm(Form):
    season = StringField("Season", validators=[InputRequired()])
    age = FloatField('Age', validators=[InputRequired()])
    childish_diseases = StringField("Had Diseases as a Child?", validators=[InputRequired()])
    accident = StringField("Had an Accident?", validators=[InputRequired()])
    surgical_intervention = StringField("Had Surgery?", validators=[InputRequired()])
    high_fevers = StringField("Had High Fevers the Last Year?", validators=[InputRequired()])
    alcoholism = StringField("Frequency of Drinking Alcohol", validators=[InputRequired()])
    smokes = StringField("Frequency of Smoking", validators=[InputRequired()])
    num_hours_sitting = StringField("Number of Hours Spent Sitting per Day", validators=[InputRequired()])

class HeartDiseaseForm(Form):
    age = FloatField('Age', validators=[InputRequired()])
    sex = FloatField('Sex (biological)', validators=[InputRequired()])
    #  (1: Typical Angina; 2: Atypical Angina; 3: Non-anginal Pain; 4: Asymptomatic)
    cp = FloatField('Chest Pain Type', validators=[InputRequired()])
    trestbps = FloatField('Resting Blood Pressure', validators=[InputRequired()])
    chol = FloatField('Serum Cholestoral', validators=[InputRequired()])
    fbs = FloatField('Fasting Blood Sugar', validators=[InputRequired()])
    # (0: Normal; 1: ST-T Wave Abnormality; 2: Showing Probable Left Ventricular Hypertrophy)
    restecg = FloatField('Resting ECG Results', validators=[InputRequired()])
    thalach = FloatField('Max Heart-rate', validators=[InputRequired()])
    exang = FloatField('Exercise Induced Angina', validators=[InputRequired()])
    oldpeak = FloatField('ST Depression', validators=[InputRequired()])
    # (1: Upsloping; 2: Flat; 3: Downslipping)
    slope = FloatField('Slope of the Peak Exercise ST segment', validators=[InputRequired()])
    ca = FloatField('# of Major Vessels', validators=[InputRequired()])
    # (3: Normal; 6: Fixed Defect; 7:Reversible Defect)
    thal = FloatField('Thal', validators=[InputRequired()])

class SpineForm(Form):
    pelvic_incidence = FloatField('Pelvic Incidence', validators=[InputRequired()])
    pelvic_tilt = FloatField('Pelvic Tilt', validators=[InputRequired()])
    pelvic_radius = FloatField('Pelvic Radius', validators=[InputRequired()])
    pelvic_slope = FloatField('Pelvic Slope', validators=[InputRequired()])
    sacral_slope = FloatField('Sacral Slope', validators=[InputRequired()])
    sacrum_angle = FloatField('Sacrum Angle', validators=[InputRequired()])
    lumbar_lordosis_angle = FloatField('Lumbar Lordosis Angle', validators=[InputRequired()])
    degree_spondylolisthesis = FloatField('Degree of Spondylolisthesis', validators=[InputRequired()])
    direct_tilt = FloatField('Direct Tilt', validators=[InputRequired()])
    cervical_tilt = FloatField('Cervical Tilt', validators=[InputRequired()])
    thoracic_slope = FloatField('Thoracic Slope', validators=[InputRequired()])
    scoliosis_slope = FloatField('Scoliosis Slope', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LogInForm()
    if form.validate_on_submit() and form.username.data == "admin" and form.password.data == "admin":
        return redirect(url_for('portal'))
    return render_template('index.html', form=form)

@app.route('/portal', methods=['GET', 'POST'])
def portal():
    return render_template('portal.html')

@app.route('/cervical', methods=['GET', 'POST'])
def cervical():
    form = CervicalCancerForm()
    if form.validate_on_submit():
        with open('data_analysis/cervical_cancer_classifier.pkl', 'rb') as fid:
            cervical_cancer_classifier = cPickle.load(fid)

        data = [[form.age.data,
                 form.num_sexual_partners.data,
                 20,
                 form.pregnancies.data,
                 form.smokes.data,
                 0,
                 0,
                 form.hormonal_contraceptives.data,
                 0,
                 form.iud.data,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 0,
                 form.dx_std.data,
                 0,
                 form.dx_cancer.data,
                 form.dx_cin.data,
                 form.dx_hpv.data,
                 0.03,
                 0.04,
                 0.08,
                 0.05]]

        if cervical_cancer_classifier.predict(data)[0] == 1:
            return redirect(url_for('telehealth'))

        return redirect(url_for('healthy'))
    return render_template('cervical.html', form=form)

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    form = DiabetesForm()
    if form.validate_on_submit():
        with open('data_analysis/diabetes_classifier.pkl', 'rb') as fid:
            diabetes_classifier = cPickle.load(fid)

        data = [[form.pregnancies.data,
                 form.glucose.data,
                 form.blood_pressure.data,
                 form.skin_thickness.data,
                 form.insulin.data,
                 form.weight.data/(form.height.data**2),
                 0.3,
                 form.age.data]]

        if diabetes_classifier.predict(data)[0] == 1 or form.glucose.data > 126.0:
            return redirect(url_for('telehealth'))

        # process
        return redirect(url_for('healthy'))
    return render_template('diabetes.html', form=form)

@app.route('/fertility', methods=['GET', 'POST'])
def fertility():
    form = FertilityForm()
    if form.validate_on_submit():
        with open('data_analysis/fertility_classifier.pkl', 'rb') as fid:
            fertility_classifier = cPickle.load(fid)

        data = [[form.season.data,
                 form.age.data,
                 form.childish_diseases.data,
                 form.accident.data,
                 form.surgical_intervention.data,
                 form.high_fevers.data,
                 form.alcoholism.data,
                 form.smokes.data,
                 form.num_hours_sitting.data]]

        if fertility_classifier.predict(data)[0] == 1:
            return redirect(url_for('telehealth'))

        return redirect(url_for('healthy'))
    return render_template('fertility.html', form=form)

@app.route('/spine', methods=['GET', 'POST'])
def spine():
    form = SpineForm()
    if form.validate_on_submit():
        with open('data_analysis/spine_classifier.pkl', 'rb') as fid:
            spine_classifier = cPickle.load(fid)

        data = [[form.pelvic_incidence.data,
                 form.pelvic_tilt.data,
                 form.pelvic_radius.data,
                 form.pelvic_slope.data,
                 form.sacral_slope.data,
                 form.sacrum_angle.data,
                 form.lumbar_lordosis_angle.data,
                 form.degree_spondylolisthesis.data,
                 form.direct_tilt.data,
                 form.cervical_tilt.data,
                 form.thoracic_slope.data,
                 form.scoliosis_slope.data]]

        if spine_classifier.predict(data)[0] == 1:
            return redirect(url_for('telehealth'))

        return redirect(url_for('healthy'))
    return render_template('spine.html', form=form)

@app.route('/heart', methods=['GET', 'POST'])
def heart():
    form = HeartDiseaseForm()
    if form.validate_on_submit():
        with open('data_analysis/heart_attack_classifier.pkl', 'rb') as fid:
            heart_attack_classifier = cPickle.load(fid)

        data = [[form.age.data,
                 form.sex.data,
                 form.cp.data,
                 form.trestbps.data,
                 form.chol.data,
                 form.fbs.data,
                 form.restecg.data,
                 form.thalach.data,
                 form.exang.data,
                 form.oldpeak.data,
                 form.slope.data,
                 form.ca.data,
                 form.thal.data]]

        if heart_attack_classifier.predict(data)[0] == 1:
            return redirect(url_for('telehealth'))

        return redirect(url_for('healthy'))
    return render_template('heart.html', form=form)

@app.route('/telehealth', methods=['GET', 'POST'])
def telehealth():
    return render_template('telehealth_recom.html')

@app.route('/healthy', methods=['GET', 'POST'])
def healthy():
    return render_template('healthy.html')

if __name__ == '__main__':
    app.run(debug=True)
