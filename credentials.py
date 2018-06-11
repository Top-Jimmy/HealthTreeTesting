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
	'myel_diag_data': {
		'newly_diagnosed': 'no',
		'date': '05/2018',
		'what_diagnosis': 'plasmacytoma',
		'high_risk': 'no',
		'stem_cell': 'no',
		'lesions': 'no lesions'
		'facility': 'Primary Childrens',
		'city': 'Sandy',
		'state': 'Utah',
		'additional': 'no',
		'phys name': 'Bobby Buttkiss',
		'phys facility': 'Primary Childrens',
		'phys city': 'Sandy',
		'phys state': 'Utah',
	}
}

def get_credentials(name):
  if name is not None:
    return eval(name)