from wtforms import Form, StringField, TextAreaField, PasswordField, validators

#RegisterForm class
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min = 1, max = 50)])
	username = StringField('Username', [validators.Length(min = 4, max = 25)])
	email = StringField('Email', [validators.Length(min = 6, max = 50)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# Article Form class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min = 1, max = 200)])
	body = TextAreaField('Body', [validators.Length(min = 40)])


class MaterialFormMain(Form):
	classification = StringField('classification', [validators.Length(min = 1, max = 250)])
	marka = StringField('marka', [validators.Length(min = 1, max = 50)])
	primenenie = StringField('primenenie', [validators.Length(min = 0, max = 250)])
	dopolnenie = StringField('dopolnenie', [validators.Length(min=0, max=250)])

class MaterialFormOther(Form):
	#chemical_composition
	AtomicNumber = StringField('AtomicNumber', [validators.Length(min = 0, max = 30)])
	concentration = StringField('concentration', [validators.Length(min = 0, max = 30)])
	minimum = StringField('minimum', [validators.Length(min = 0, max = 30)])
	maximum = StringField('maximum', [validators.Length(min=0, max=30)])
	average = StringField('average', [validators.Length(min=0, max=30)])

	#critical_temperatur
	critical_temperatur = StringField('critical_temperatur', [validators.Length(min = 0, max = 250)])

	#mechanical_properties
	sortament = StringField('sortament', [validators.Length(min=0, max=250)])
	razmer = StringField('razmer', [validators.Length(min=0, max=30)])
	napr = StringField('napr', [validators.Length(min=0, max=30)])
	sigma_b = StringField('sigma_b', [validators.Length(min=0, max=30)])
	sigma_t = StringField('sigma_t', [validators.Length(min=0, max=30)])
	delta_5 = StringField('delta_5', [validators.Length(min=0, max=30)])
	psi = StringField('psi', [validators.Length(min=0, max=30)])
	KCU = StringField('KCU', [validators.Length(min=0, max=30)])
	termo_obrab = StringField('termo_obrab', [validators.Length(min=0, max=150)])

	#phisical_properties

	T = StringField('T', [validators.Length(min=0, max=30)])
	E = StringField('E', [validators.Length(min=0, max=30)])
	alpha = StringField('alpha', [validators.Length(min=0, max=30)])
	LAMBDAA = StringField('LAMBDAA', [validators.Length(min=0, max=30)])
	ro = StringField('ro', [validators.Length(min=0, max=30)])
	C = StringField('C', [validators.Length(min=0, max=30)])
	R = StringField('R', [validators.Length(min=0, max=30)])

	#table6
	property = StringField('property', [validators.Length(min=0, max=400)])

	#techno_properties
	property_name = StringField('property_name', [validators.Length(min=0, max=150)])
	property_value = StringField('property_value', [validators.Length(min=0, max=150)])

	#termo_mod
	property_termo = StringField('property_termo', [validators.Length(min=0, max=600)])


