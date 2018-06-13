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
		'diagnosis_date': '05/2018',
		'first_diagnosis': 'plasmacytoma',
		'high_risk': 'no',
		'transplant_eligible': 'no',
		'bone_lesions': 'no lesions',
		'diagnosis_location': {
			'facility': 'Huntsman Cancer',
			'city': 'Salt Lake City',
			'state': 'Utah',
		},
		'additional_diagnosis': False,
		'additional_diagnoses': [], # i.e. [{'date': '01/2000', 'diagnosis': 'Smoldering Myeloma'},]
		'physicians': [
			{'name': 'David Avigan',
				'facility': 'Beth Israel Deaconess Medical Center',
				'city': 'Boston',
				'state': 'Massachusetts',
			},
		],
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
	'fitness_level_data': {
		'walk_sixhours': 'no',
		'walk_fivehours': 'no',
		'walk_unassisted': 'no',
		'shop': 'yes',
	},
	'health_demographic': {
		'race': 'white',
		'ethnicity': 'not Hispanic',
		'race_ethnic': 'american',
		'country': 'USA',
		'city_born': 'Sandy',
		'city_grow': 'Gilford',
		'city_adult': 'Lehi',
		'religion': 'none',
		'marital': 'married',
		'education': 'some college',
		'employment': 'disabled',
		'health_ins': 'no',
		'military': 'no',
	},
	'health_history': {
		'bone_frac': 'no',
		'bone_pain': 'no',
		'bone_weak': 'no',
		'hypercalc': 'no',
		'spinal': 'no', 'no',
		'other_bone': 'no', 'no',
		'renal_fail': 'no',
		'renal_trans': 'no',
		'dialysis': 'no',
		'allergies': {
			'eggs': False,
			'fish': False,
			'milk': True,
			'peanuts': True,
			'shellfish': True,
			'soy': False,
			'tree_nuts': True,
			'wheat': True,
			'other': False,
		},
		'aller_drug': 'no',
		'insect_allergies': {
			'biting': False,
			'stinging': False,
			'pest': True,
			'other_ins': True,
		},
		'latex_allergies': {
			'balloons': False,
			'bandages': True,
			'condoms': True,
			'rubber_balls': False,
			'rubber_bands': True,
			'rubber_gloves': True,
			'other_latex': False,
		},
		'mold_allergies': {
			'indoor': True,
			'outdoor': False,
			'other_mold': False,
		},
		'pet_allergies': {
			'cats': True,
			'dogs': True,
			'other_pets': True,
		},
		'pollen_allergies': {
			'birch': False,
			'cedar': True,
			'grass': False,
			'lambs': False,
			'oak': True,
			'pigweed': True,
			'pine': True,
			'ragweed': True,
			'sagebrush': True,
			'other_pollen': True,
		},
		'surgeries': {
			'appendectomy': True,
			'back': True,
			'brain': False,
			'breast': True,
			'heart': True,
			'hysterectomy':
			'hernia': False,
			'liver': True,
			'lung': False,
			'mastectomy': False,
			'stomach': True,
			'other_surgery': False,
		},
		'anemia': 'no',
		'celiac': 'no',
		'diabetic': 'no',
		'hiv': 'no',
		'mono': 'no',
		'bowel': 'no',
		'lupus': 'no',
		'lymph': 'no',
		'osteo': 'no',
		'kidney': 'no',
		'rheumatoid': 'no',
		'sjögren': 'no',
		'hashimoto': 'no',
		'psoriasis': 'no',
		'psoriatic': 'no',
		'stroke': 'no',
		'thyroid': 'no',
		'thrombosis': 'no',
		'vitiligo': 'no',
		'other_disease': 'yes',
		'poems': 'no',
		'non-secretory': 'no',
		'light_chain': 'no',

	},
	'family_history_data' {
		'father': 'brain',
		'mother': 'brain',
		'sibling': 'brain',
		'pat_grandfather': 'brain',
		'pat_grandmother': 'brain',
		'mat_grandfather': 'brain',
		'mat_grandmother': 'brain',
		'family_multiple': 'brain',
		'family_smoldering': 'brain',
		'family_monoclonal': 'brain',
		'multiple': 'no',
		'smoldering': 'no',
		'mgus': 'no',
		'diabetes': 'no',
		'hyperension': 'no',
		'cardivascular': 'no',
	},
}

def get_credentials(name):
  if name is not None:
    return eval(name)