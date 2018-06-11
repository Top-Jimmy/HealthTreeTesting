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
	},
	'myel_diag_data': {
		'newly_diagnosed': 'no',
		'date': '05/2018',
		'what_diagnosis': 'plasmacytoma',
		'high_risk': 'no',
		'stem_cell': 'no',
		'lesions': 'no lesions',
		'facility': 'Primary Childrens',
		'city': 'Sandy',
		'state': 'Utah',
		'additional': 'no',
		'phys_name': 'Bobby Buttkiss',
		'phys_facility': 'Primary Childrens',
		'phys_city': 'Sandy',
		'phys_state': 'Utah',
	},
	'current_health_data': {
		'status_stable': 'dont know',
		'status_relapse': 'dont know',
		'status_issues': 'dont know',
		'condition_heart': 'dont know',
		'condition_lung': 'dont know',
		'condition_kidney': 'dont know',
		'condition_diabetes': 'dont know',
		'condition_blood_pressure': 'dont know',
		'conditioin_blood_clot': 'dont know',
		'condition_neuropathy': 'dont know',
		'condition_other': 'dont know',
	},
}

def get_credentials(name):
  if name is not None:
    return eval(name)