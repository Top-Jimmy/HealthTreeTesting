import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (NoSuchElementException,
		StaleElementReferenceException)

class HealthHistForm():

	def __init__(self, driver, expectedValues=None):
		self.driver = driver
		self.load(expectedValues)

	def load(self, expectedValues):
		self.form = self.driver.find_elements_by_tag_name('form')[-1]
		inputs = self.form.find_elements_by_tag_name('input')
		anchors = self.form.find_elements_by_tag_name('a')
		# small[2] hidden element

		self.bone_fracno_radio = inputs[0]
		self.bone_fracyes_radio = inputs[1]

		self.bone_painno_radio = inputs[2]
		self.bone_painyes_radio = inputs[3]

		self.bone_weakno_radio = inputs[4]
		self.bone_weakyes_radio = inputs[5]

		self.hypercalcno_radio = inputs[6]
		self.hypercalcyes_radio = inputs[7]

		self.spinalno_radio = inputs[8]
		self.spinalyes_radio = inputs[9]

		self.otherno_radio = inputs[10]
		self.otheryes_radio = inputs[11]

		self.renal_failno_radio = inputs[12]
		self.renal_failyes_radio = inputs[13]

		self.renal_transno_radio = inputs[14]
		self.renal_transyes_radio = inputs[15]

		self.dialyno_radio = inputs[16]
		self.dialyyes_radio = inputs[17]

		self.aller_food_eggs_checkbox = inputs[18]
		self.aller_food_fish_checkbox = inputs[19]
		self.aller_food_milk_checkbox = inputs[20]
		self.aller_food_pean_checkbox = inputs[21]
		self.aller_food_shell_checkbox = inputs[22]
		self.aller_food_soy_checkbox = inputs[23]
		self.aller_food_tree_checkbox = inputs[24]
		self.aller_food_wheat_checkbox = inputs[25]
		self.aller_food_other_checkbox = inputs[26]

		self.aller_drugno_radio = inputs[27]
		self.aller_drugyes_radio = inputs[28]

		self.aller_ins_bite_checkbox = inputs[29]
		self.aller_ins_sting_checkbox = inputs[30]
		self.aller_ins_pest_checkbox = inputs[31]
		self.aller_ins_other_checkbox = inputs[32]

		self.aller_lat_ball_checkbox = inputs[33]
		self.aller_lat_band_checkbox = inputs[34]
		self.aller_lat_cond_checkbox = inputs[35]
		self.aller_lat_rubball_checkbox = inputs[36]
		self.aller_lat_rubband_checkbox = inputs[37]
		self.aller_lat_glov_checkbox = inputs[38]
		self.aller_lat_other_checkbox = inputs[39]

		self.aller_mold_in_checkbox = inputs[40]
		self.aller_mold_out_checkbox = inputs[41]
		self.aller_mold_other_checkbox = inputs[42]

		self.aller_pet_cat_checkbox = inputs[43]
		self.aller_pet_dog_checkbox = inputs[44]
		self.aller_pet_other_checkbox = inputs[45]

		self.aller_pol__bir_checkbox = inputs[46]
		self.aller_pol_ced_checkbox = inputs[47]
		self.aller_pol_gra_checkbox = inputs[48]
		self.aller_pol_lam_checkbox = inputs[49]
		self.aller_pol_oak_checkbox = inputs[50]
		self.aller_pol_pig_checkbox = inputs[51]
		self.aller_pol_pine_checkbox = inputs[52]
		self.aller_pol_rag_checkbox = inputs[53]
		self.aller_pol_sage_checkbox = inputs[54]
		self.aller_pol_other_checkbox = inputs[55]

		self.surg_app_checkbox = inputs[56]
		self.surg_back_checkbox = inputs[57]
		self.surg_brain_checkbox = inputs[58]
		self.surg_breast_checkbox = inputs[59]
		self.surg_heart_checkbox = inputs[60]
		self.surg_hyst_checkbox = inputs[61]
		self.surg_hern_checkbox = inputs[62]
		self.surg_liver_checkbox = inputs[63]
		self.surg_lung_checkbox = inputs[64]
		self.surg_mast_checkbox = inputs[65]
		self.surg_stom_checkbox = inputs[66]
		self.surg_other_checkbox = inputs[67]

		self.anemiano_radio = inputs[68]
		self.anemiayes_radio = inputs[69]
		self.anemiaidk_radio = inputs[70]

		self.celiacno_radio = inputs[71]
		self.celiacyes_radio = inputs[72]
		self.celiacidk_radio = inputs[73]

		self.diabno_radio = inputs[74]
		self.diabyes_radio = inputs[75]
		self.diabidk_radio = inputs[76]

		self.hivno_radio = inputs[77]
		self.hivyes_radio = inputs[78]
		self.hividk_radio = inputs[79]

		self.monono_radio = inputs[80]
		self.monoyes_radio = inputs[81]
		self.monoidk_radio = inputs[82]

		self.bowelno_radio = inputs[83]
		self.bowelyes_radio = inputs[84]
		self.bowelidk_radio = inputs[85]

		self.lupusno_radio = inputs[86]
		self.lupusyes_radio = inputs[87]
		self.lupusidk_radio = inputs[88]

		self.lymphno_radio = inputs[89]
		self.lymphyes_radio = inputs[90]
		self.lymphidk_radio = inputs[91]

		self.osteono_radio = inputs[92]
		self.osteoyes_radio = inputs[93]
		self.osteoidk_radio = inputs[94]

		self.kidneyno_radio = inputs[95]
		self.kidneyyes_radio = inputs[96]
		self.kidneyidk_radio = inputs[97]

		self.rheumno_radio = inputs[98]
		self.rheumyes_radio = inputs[99]
		self.rheumidk_radio = inputs[100]

		self.sjogno_radio = inputs[101]
		self.sjogyes_radio = inputs[102]
		self.sjogidk_radio = inputs[103]

		self.hashino_radio = inputs[104]
		self.hashiyes_radio = inputs[105]
		self.hashiidk_radio = inputs[106]

		self.psorino_radio = inputs[107]
		self.psoriyes_radio = inputs[108]
		self.psoriidk_radio = inputs[109]

		self.arthrno_radio = inputs[110]
		self.arthryes_radio = inputs[111]
		self.arthridk_radio = inputs[112]

		self.strokeno_radio = inputs[113]
		self.strokeyes_radio = inputs[114]
		self.strokeidk_radio = inputs[115]

		self.thyrno_radio = inputs[116]
		self.thyryes_radio = inputs[117]
		self.thyridk_radio = inputs[118]

		self.thrombno_radio = inputs[119]
		self.thrombyes_radio = inputs[120]
		self.thrombidk_radio = inputs[121]

		self.vitilno_radio = inputs[122]
		self.vitilyes_radio = inputs[123]
		self.vitilidk_radio = inputs[124]

		self.other_diseaseyes_radio = inputs[125]

		self.poemsno_radio = inputs[126]
		self.poemsyes_radio = inputs[127]
		self.poemsidk_radio = inputs[128]

		self.non_secreteyes_radio = inputs[129]
		self.non_secreteno_radio = inputs[130]

		self.lite_cha_no_radio = inputs[131]
		self.lite_cha_yeskappa_radio = inputs[132]
		self.lite_cha_yeslambda_radio = inputs[133] 
		


		# self.validate(expectedValues)
		return True

	def validate(self, expectedValues):
		failures = []
		if expectedValues:
			if expectedValues['bone_frac'] == 'no' and not self.bone_fracno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having any bone fractures')
			elif expectedValues['bone_frac'] == 'yes' and not self.bone_fracyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having any bone fractures')

			if expectedValues['bone_pain'] == 'no' and not self.bone_painno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having any bone pain')
			elif expectedValues['bone_pain'] == 'yes' and not self.bone_painyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having any bone pain')

			if expectedValues['bone_weak'] == 'no' and not self.bone_weakno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having any bone weakness')
			elif expectedValues['bone_weak'] == 'yes' and not self.bone_weakyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having any bone weakness')

			if expectedValues['hypercalc'] == 'no' and not self.hypercalcno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having hypercalcemia')
			elif expectedValues['hypercalc'] == 'yes' and not self.hypercalcyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having hypercalcemia')

			if expectedValues['spinal'] == 'no' and not self.spinalno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having spinal compression')
			elif expectedValues['spinal'] == 'yes' and not self.spinalyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having spinal compression')

			if expectedValues['other_bone'] == 'no' and not self.otherno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having any other bone issues')
			elif expectedValues['other_bone'] == 'yes' and not self.otheryes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having any other bone issues')

			if expectedValues['renal_fail'] == 'no' and not self.renal_failno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having kidney failure')
			elif expectedValues['renal_fail'] == 'yes' and not self.renal_failyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having kidney failure')

			if expectedValues['renal_trans'] == 'no' and not self.renal_transno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having a kidney transplant')
			elif expectedValues['renal_trans'] == 'yes' and not self.renal_transyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having a kidney transplant')

			if expectedValues['dialysis'] == 'no' and not self.dialyno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to previously having dialysis')
			elif expectedValues['dialysis'] == 'yes' and not self.dialyyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to previously having dialysis')

			if expectedValues['eggs'] != self.aller_food_eggs_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['eggs']) + '" Egg allergy')
			if expectedValues['fish'] != self.aller_food_fish_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['fish']) + '" Fish allergy')
			if expectedValues['milk'] != self.aller_food_milk_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['milk']) + '" Milk allergy')
			if expectedValues['peanuts'] != self.aller_food_pean_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['peanuts']) + '" Peanut allergy')
			if expectedValues['shellfish'] != self.aller_food_shell_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['shellfish']) + '" Shellfish allergy')
			if expectedValues['soy'] != self.aller_food_soy_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['soy']) + '" Soy allergy')
			if expectedValues['tree_nuts'] != self.aller_food_tree_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['tree_nuts']) + '" Tree nut allergy')
			if expectedValues['wheat'] != self.aller_food_wheat_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['wheat']) + '" Wheat allergy')
			if expectedValues['other'] != self.aller_food_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other']) + '" Other allergy')

			if expectedValues['aller_drug'] == 'no' and not self.aller_drugno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" to having a drug allergy')
			elif expectedValues['aller_drug'] == 'yes' and not self.aller_drugyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting"yes" to having a drug allergy')

			if expectedValues['biting'] != self.aller_ins_bite_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['biting']) + '" Biting insect allergy')
			if expectedValues['stinging'] != self.aller_ins_sting_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['stinging']) + '" Stinging insect allergy')
			if expectedValues['pests'] != self.aller_ins_pest_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['pests']) + '" Household pests allergy')
			if expectedValues['other_ins'] != self.aller_ins_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other_ins']) + '" Other insect allergy')

			if expectedValues['balloons'] != self.aller_lat_ball_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['balloons']) + '" Balloon allergy')
			if expectedValues['bandages'] != self.aller_lat_band_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['bandages']) + '" Bandage allergy')
			if expectedValues['condoms'] != self.aller_lat_cond_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['condoms']) + '" Condom allergy')
			if expectedValues['rubber_ball'] != self.aller_lat_rubball_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['rubber_ball']) + '" Rubber ball allergy')
			if expectedValues['rubber_band'] != self.aller_lat_rubband_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['rubber_band']) + '" Rubber band allergy')
			if expectedValues['rubber_gloves'] != self.aller_lat_glov_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['rubber_gloves']) + '" Rubber glove allergy')
			if expectedValues['other_latex'] != self.aller_lat_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other_latex']) + '" Other latex allergy')

			if expectedValues['indoor'] != self.aller_mold_in_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['indoor']) + '" Indoor mold allergy')
			if expectedValues['outdoor'] != self.aller_mold_out_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['outdoor']) + '" Outdoor mold allergy')
			if expectedValues['other_mold'] != self.aller_mold_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other_mold']) + '" Other mold allergy')

			if expectedValues['cats'] != self.aller_pet_cat_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['cats']) + '" Cat allergy')
			if expectedValues['dogs'] != self.aller_pet_dog_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['dogs']) + '" Dog allergy')
			if expectedValues['other_pets'] != self.aller_pet_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other_pets']) + '" Other pet allergy')

			if expectedValues['birch'] != self.aller_pol__bir_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['birch']) + '" Birch tree allergy')
			if expectedValues['cedar'] != self.aller_pol_ced_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['cedar']) + '" Cedar tree allergy')
			if expectedValues['grass'] != self.aller_pol_gra_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['grass']) + '" Grass allergy')
			if expectedValues['lambs'] != self.aller_pol_lam_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['lambs']) + '" Lambs quarters allergy')
			if expectedValues['oak'] != self.aller_pol_oak_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['oak']) + '" Oak tree allergy')
			if expectedValues['pigweed'] != self.aller_pol_pig_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['pigweed']) + '" Pigweed allergy')
			if expectedValues['pine'] != self.aller_pol_pine_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['pine']) + '" Pine tree allergy')
			if expectedValues['ragweed'] != self.aller_pol_rag_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['ragweed']) + '" Ragweed allergy')
			if expectedValues['sagebrush'] != self.aller_pol_sage_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['sagebrush']) + '" Sagebrush allergy')
			if expectedValues['other_pollen'] != self.aller_pol_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other_pollen']) + '" Other pollen allergy')

			if expectedValues['appendectomy'] != self.surg_app_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['appendectomy']) + '" Had appendectomy surgery')
			if expectedValues['back'] != self.surg_back_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['back']) + '" Had back surgery')
			if expectedValues['brain'] != self.surg_brain_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['brain']) + '" Had brain surgery')
			if expectedValues['breast'] != self.surg_breast_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['breast']) + '" Had breast surgery')
			if expectedValues['heart'] != self.surg_heart_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['heart']) + '" Had heart surgery')
			if expectedValues['hysterectomy'] != self.surg_hyst_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['hysterectomy']) + '" Had hysterectomy surgery')
			if expectedValues['hernia'] != self.surg_hern_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['hernia']) + '" Had hernia surgery')
			if expectedValues['liver'] != self.surg_liver_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['liver']) + '" Had liver surgery')
			if expectedValues['lung'] != self.surg_lung_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['lung']) + '" Had lung surgery')
			if expectedValues['mastectomy'] != self.surg_mast_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['mastectomy']) + '" Had mastectomy surgery')
			if expectedValues['stomach'] != self.surg_stom_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['stomach']) + '" Had stomach surgery')
			if expectedValues['other_surgery'] != self.surg_other_checkbox.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "' + str(expectedValues['other_surgery']) + '" Had other surgery')

			if expectedValues['anemia'] == 'no' and not self.anemiano_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having anemia')
			elif expectedValues['anemia'] == 'yes' and not self.anemiayes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having anemia')
			elif expectedValues['anemia'] == 'I dont know' and not self.anemiaidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having anemia')

			if expectedValues['celiac'] == 'no' and not self.celiacno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having celiac disease')
			elif expectedValues['celiac'] == 'yes' and not self.celiacyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having celiac disease')
			elif expectedValues['celiac'] == 'I dont know' and not self.celiacidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having celiac disease')

			if expectedValues['diabetic'] == 'no' and not self.diabno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having diabetic mallitus')
			elif expectedValues['diabetic'] == 'yes' and not self.diabyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having diabetic mallitus')
			elif expectedValues['diabetic'] == 'I dont know' and not self.diabidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having diabetic mallitus')

			if expectedValues['hiv'] == 'no' and not self.hivno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having hiv disease')
			elif expectedValues['hiv'] == 'yes' and not self.hivyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having hiv disease')
			elif expectedValues['hiv'] == 'I dont know' and not self.hividk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having hiv disease')

			if expectedValues['mono'] == 'no' and not self.monono_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having mono disease')
			elif expectedValues['mono'] == 'yes' and not self.monoyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having mono disease')
			elif expectedValues['mono'] == 'I dont know' and not self.monoidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having mono disease')

			if expectedValues['bowel'] == 'no' and not self.bowelno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having bowel disease')
			elif expectedValues['bowel'] == 'yes' and not self.bowelyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having bowel disease')
			elif expectedValues['bowel'] == 'I dont know' and not self.bowelidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having bowel disease')

			if expectedValues['lupus'] == 'no' and not self.lupusno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having lupus disease')
			elif expectedValues['lupus'] == 'yes' and not self.lupusyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having lupus disease')
			elif expectedValues['lupus'] == 'I dont know' and not self.lupusidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having lupus disease')

			if expectedValues['lymph'] == 'no' and not self.lymphno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having lymph disease')
			elif expectedValues['lymph'] == 'yes' and not self.lymphyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having lymph disease')
			elif expectedValues['lymph'] == 'I dont know' and not self.lymphidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having lymph disease')

			if expectedValues['osteo'] == 'no' and not self.osteono_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having osteoporosis disease')
			elif expectedValues['osteo'] == 'yes' and not self.osteoyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having osteoporosis disease')
			elif expectedValues['osteo'] == 'I dont know' and not self.osteoidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having osteoporosis disease')

			if expectedValues['kidney'] == 'no' and not self.kidneyno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having kidney problems')
			elif expectedValues['kidney'] == 'yes' and not self.kidneyyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having kidney problems')
			elif expectedValues['kidney'] == 'I dont know' and not self.kidneyidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having kidney problems')

			if expectedValues['rheumatoid'] == 'no' and not self.rheumno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having rheumatoid arthritis')
			elif expectedValues['rheumatoid'] == 'yes' and not self.rheumyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having rheumatoid arthritis')
			elif expectedValues['rheumatoid'] == 'I dont know' and not self.rheumidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having rheumatoid arthritis')

			if expectedValues['sjogren'] == 'no' and not self.sjogno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having sjogren disease')
			elif expectedValues['sjogren'] == 'yes' and not self.sjogyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having sjogren disease')
			elif expectedValues['sjogren'] == 'I dont know' and not self.sjogidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having sjogren disease')

			if expectedValues['hasimoto'] == 'no' and not self.hashino_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having hasimoto disease')
			elif expectedValues['hasimoto'] == 'yes' and not self.hashiyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having hasimoto disease')
			elif expectedValues['hasimoto'] == 'I dont know' and not self.hashiidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having hasimoto disease')

			if expectedValues['psoriasis'] == 'no' and not self.psorino_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having psoriasis disease')
			elif expectedValues['psoriasis'] == 'yes' and not self.psoriyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having psoriasis disease')
			elif expectedValues['psoriasis'] == 'I dont know' and not self.psoriidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having psoriasis disease')

			if expectedValues['psoriatic'] == 'no' and not self.arthrno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having psoriatic arthritis')
			elif expectedValues['psoriatic'] == 'yes' and not self.arthryes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having psoriatic arthritis')
			elif expectedValues['psoriatic'] == 'I dont know' and not self.arthridk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having psoriatic arthritis')

			if expectedValues['stroke'] == 'no' and not self.strokeno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having a stroke')
			elif expectedValues['stroke'] == 'yes' and not self.strokeyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having a stroke')
			elif expectedValues['stroke'] == 'I dont know' and not self.strokeidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having a stroke')

			if expectedValues['thyroid'] == 'no' and not self.thyrno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having thyroid disease')
			elif expectedValues['thyroid'] == 'yes' and not self.thyryes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having thyroid disease')
			elif expectedValues['thyroid'] == 'I dont know' and not self.thyridk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having thyroid disease')

			if expectedValues['thrombosis'] == 'no' and not self.thrombno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having blood clots')
			elif expectedValues['thrombosis'] == 'yes' and not self.thrombyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having blood clots')
			elif expectedValues['thrombosis'] == 'I dont know' and not self.thrombidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having blood clots')

			if expectedValues['vitiligo'] == 'no' and not self.vitilno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having vitiligo disease')
			elif expectedValues['vitiligo'] == 'yes' and not self.vitilyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having vitiligo disease')
			elif expectedValues['vitiligo'] == 'I dont know' and not self.vitilidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having vitiligo disease')

			if expectedValues['other_disease'] == 'yes' and not self.other_diseaseyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" to having any other autoimmune diseases')
			
			if expectedValues['poems'] == 'no' and not self.poemsno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having POEMS')
			elif expectedValues['poems'] == 'yes' and not self.poemsyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having POEMS')
			elif expectedValues['poems'] == 'I dont know' and not self.poemsidk_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "I dont know" for having POEMS')

			if expectedValues['non-secretory'] == 'no' and not self.non_secreteno_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having non-secretory myeloma')
			elif expectedValues['non-secretory'] == 'yes' and not self.non_secreteyes_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes" for having non-secretory myeloma')

			if expectedValues['light_chain'] == 'no' and not self.lite_cha_no_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "no" for having light chain myeloma')
			elif expectedValues['light_chain'] == 'yes-kappa' and not self.lite_cha_yeskappa_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes-kappa" for having kappa light chain myeloma')
			elif expectedValues['light_chain'] == 'yes-lambda' and not self.lite_cha_yeslambda_radio.get_attribute('checked'):
				failure.append('HealthHistForm: Expecting "yes-lambda" for having lambda light chain myeloma')

		if len(failures) > 0:
			print(failures)
			raise NoSuchElementException('Failed to load AboutMeForm')

	def read_warning(self):
		inputs = ['username', 'email', 'password', 'confirm password']
		warnings = []
		warning_els = [
			self.username_warning, self.email_warning, self.password_warning, self.confirm_password_warning,
		]
		for i, warning_el in enumerate(warning_els):
			text = warning_el.text
			if len(text) > 0:
				warnings.append({
					'inputName': inputs[i],
					'text': text,
				})
		if len(warnings) > 0:
			return warnings
		return None

	def interpret_warning(self, warningText):
		warningType = 'undefined'
		warningMsg = ''
		if warningText == 'Please enter a valid email address.':
			warningType = 'Invalid credentials'
			warningMsg = 'forgotPwForm: Submit form warning'

		return {
			'msg', warningMsg,
			'text', warningText,
			'type', warningType,
		}


	def enter_info(self, form_info):
		if form_info:
			self.firstname_input.send_keys(form_info['first_name'])
			self.password_input.send_keys(form_info['last_name'])
			if form_info['gender'] == 'male':
				functions.move_to_el(self.male_radio)
			else:
				functions.move_to_el(self.female_radio)
			self.birth_input.send_keys(form_info)['dob']
			self.zipcode_input.send_keys(form_info)['zip_code']
			self.treatment_textarea.send_keys(form_info)['treatment_goals']
			if form_info['assisted'] == True:
				functions.move_to_el(self.cancerCareYes_radio)
			else:
				functions.move_to_el(self.cancerCareNo_radio)

			if form_info['terms'] == True:
				functions.move_to_el(self.termsprivacy_checkbox)

			if form_info['sparkCures'] == True:
				functions.move_to_el(self.SparkCuresterms_checkbox)

			return True
		return False