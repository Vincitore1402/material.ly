import math
# Compare to materials via their chemical compositons
# Return index of similarity
def simple_Compare(chem_composition_first,chem_composition_second):
	sum = 0
	sum_container = []
	element_container = []

	for chem_2 in chem_composition_second:

		for chem_1 in chem_composition_first:

			if (chem_2['atomic_Number'] == chem_1['atomic_Number']):
				sum_container.append((chem_1['average'] - chem_2['average']) ** 2)
				element_container.append(chem_1['atomic_Number'])
				break

	for chem_1 in chem_composition_first:
		if (chem_1['atomic_Number'] not in element_container):
			sum_container.append((chem_1['average']) ** 2)

	for chem_2 in chem_composition_second:
		if (chem_2['atomic_Number'] not in element_container):
			sum_container.append((chem_2['average']) ** 2)

	for el in sum_container:
		sum += el

	index = math.sqrt(sum)
	return index

def getChemicalComposition(id,chem_composition_others):
	chem_composition = []
	for material in chem_composition_others:
		if material['main_info_id'] == id:
			chem_composition.append(material)
	return chem_composition

def getKey(material):
    return material['index']