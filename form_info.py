sideEffects = {                                     # 11 sections, 66 sub options
  'cardiovascular/circulatory system': {            # 11 sub options
    'blood clots': 1,
    'chest pain': 1,
    'heart complications/problems': 1,
    'high blood pressure': 1,
    'irregular/rapid heartbeat': 1,
    'low blood calcium (hypocalcemia)': 1,
    'low blood pressure': 1,
    'low platelets (thrombocytopenia)': 1,
    'low potassium': 1,
    'low red blood cells (anemia)': 1,
    'low white blood cells (neutropenia or lymphocyte)': 1,
  },
  'digestive system': {
    'constipation': 1,
    'decreased appetite': 1,
    'diarrhea': 1,
    'increased gas or bloating': 1,
    'nausea': 1,
    'vomiting': 1,
  },
  'endocrine system': {
    'blood sugar regulation issues': 1,
    'interference with blood type testing': 1,
  },
  'integumentary/exocrine system': {
    'easily bruise or bleed (hemorrhage)': 1,
    'skin changes: thinning skin or discoloration': 1,
    'hemorrhoids': 1,
    'hair loss': 1,
  },
  'lymphatic/immune system': {
    'fatigue/tired': 1,
    'fever/chills': 1,
    'hand-foot syndrome': 1,
    'mouth sores': 1,
    'rash/skin reaction with blisters and peeling': 1,
    'shingles (herpes zoster)': 1,
    'decreased weight': 1,
    'changes in shape or location of body fat (arms, legs, face, etc.)': 1,
    'graft vs. host disease (gvhd)': 1,
  },
  'musculoskeletal system': {
    'back pain': 1,
    'joint pain': 1,
    'muscle cramps/spasms': 1,
    'muscle weakness': 1,
    'osteonecrosis of the jaw (onj)': 1,
  },
  'nervous system': {
    'aggression/mood changes/irritability': 1,
    'anxiety': 1,
    'headaches': 1,
    'mental confusion': 1,
    'mental depression': 1,
    'nervousness': 1,
    'peripheral neuropathy (numbness or tingling in arms or legs)': 1,
    'seizures': 1,
    'trouble thinking, speaking or walking': 1,
    'visual problems/blurred or blindness': 1,
    'dizziness': 1,
  },
  'renal/urinary system': {
    'kidney damage': 1,
    'kidney failure': 1,
    'liver damage': 1,
    'liver failure': 1,
    'swelling (edema) in arms or legs (peripheral edema)': 1,
    'urine decrease': 1,
  },
  'respiratory system': {
    'cough': 1,
    'difficulty breathing/shortness of breath': 1,
    'high blood pressure in the lungs (pulmonary hypertension)': 1,
    'lung problems': 1,
    'pneumonia/bronchitis': 1,
    'rattling/noisy breathing': 1,
    'upper respiratory infection': 1,
  },
  'other': {
    'infusion related reactions': 1,
    'insomnia': 1,
    'cataracts': 1,
    'pounding in the ears': 1,
    'tremors': 1,
  }
}

def get_info(name):
  if name is not None:
    return eval(name)
