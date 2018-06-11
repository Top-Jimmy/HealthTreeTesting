andrew = {
	'username': 'Andrew',
	'password': 'federals',
	'email': 'tiddandrew@gmail.com',
	'about_me_data': {
		'first_name': 'Andrew',
		'last_name': 'Tidd',
		'gender': 'male',
		'dob': '05/01/2018',
		'zip_code': '84003',
		'treatment_goals': 'Asdf',
		'assisted': False,
		'terms': True,
		'sparkCures': True,
	}
}

def get_credentials(name):
  if name is not None:
    return eval(name)