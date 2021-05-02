from collections import defaultdict
from typing import DefaultDict, List

DIVIDER = '-' * 80 + '\n'
START = '=' * 15 + '\n'
END = DIVIDER + 'CONTINUING'
INFO_SPLITTER = ' : '

PERSONAL_INFO = 0
ALLERGY_INFO = 1
MEDICAL_INFO = 2

def _remove_prefix(s: str, prefix=None):
    return s[len(prefix):] if prefix and s.startswith(prefix) else s

def get_personal_info(data: str) -> DefaultDict[str, str]:
    result = defaultdict(str)

    # assuming the upper part as unique user id
    result['pseudo_user_id'] = data.split(START)[0].strip()

    # can't figure out death date attribute
    attributes = ['Race', 'Ethnicity', 'Gender', 'Age', 'Birth Date', 'Death Date', 'Marital Status']
    translator = {
        'Race': 'race_value',
        'Ethnicity': 'ethnicity_value',
        'Gender': 'gender_value',
        'Death Date': 'death_date'
    }
    date_attribute = ['year_of_birth', 'month_of_birth', 'day_of_birth']
    personal_info = data.split(DIVIDER)[PERSONAL_INFO]
    for raw_row in personal_info.split('\n'):
        for attribute in attributes:
            if attribute + ':' in raw_row:
                result[attribute] = raw_row.split(attribute+':')[1].strip()
            elif attribute not in result:
                result[attribute] = 'null'
    
    # special handling for birth date

    birth_date = result.get('Birth Date', None)
    if birth_date is None:
        raise TypeError
    if len(birth_date.split('-')) != len(date_attribute):
        raise TypeError
    for k, v in zip(date_attribute, birth_date.split('-')):
        result[k] = v

    for keys in translator:
        if keys in result:
            result[translator[keys]] = result[keys]
    return result


def parse_medical_info(ret: DefaultDict[str, str],
                       row: str,
                       attributes: List[str],
                       first_delimiter: str,
                       second_delimiter: str =None, dummy_word: str = None):
    info_list = row.split(first_delimiter)
    # presumably an empty list
    if len(info_list) == 1:
        return
    if info_list[0] == '':
        del info_list[0]
    for idx in range(len(attributes)):
        if idx == 0:
            ret[attributes[idx]] = _remove_prefix(info_list[idx].strip(), dummy_word)
            continue
        if second_delimiter:
            ret[attributes[idx]] = _remove_prefix(info_list[1].split(second_delimiter)[idx], dummy_word)
        else:
            ret[attributes[idx]] = _remove_prefix(info_list[idx].strip(), dummy_word)


def get_medical_info(data: str) -> (DefaultDict[str, str], DefaultDict[str, str], DefaultDict[str, str]):
    visit_occurrence = defaultdict(str)
    drug_exposure = defaultdict(str)
    condition_occurrence = defaultdict(str)
    visit_occurrence_attribute = ['visit_start_date', 'care_site_nm']
    visit_type_attribute = ['visit_type_value']
    drug_exposure_attribute = ['drug_exposure_start_date','drug_value', 'dose_value', 'unit_value', 'route_value']
    condition_attribute = ['condition_start_date', 'condition_value']
    medical_info = data.split(DIVIDER)[MEDICAL_INFO]
    is_encounter_info = False
    is_medication_info = False
    is_condition_info = False
    for raw_row in medical_info.split('\n'):
        if is_encounter_info and 'Type: ' in raw_row:
            is_encounter_info = False
            parse_medical_info(visit_occurrence, raw_row, visit_type_attribute, 'Type: ')
            continue
        if is_encounter_info:
            parse_medical_info(visit_occurrence, raw_row, visit_occurrence_attribute, INFO_SPLITTER, dummy_word="Encounter at ")
        if 'ENCOUNTER' in raw_row:
            is_encounter_info = True
        if is_medication_info:
            is_medication_info = False
            parse_medical_info(drug_exposure, raw_row, drug_exposure_attribute, INFO_SPLITTER, ' ')
        if 'MEDICATIONS' in raw_row:
            is_medication_info = True
        if is_condition_info:
            is_condition_info = False
            parse_medical_info(condition_occurrence, raw_row, condition_attribute, INFO_SPLITTER)
        if 'CONDITIONS' in raw_row:
            is_condition_info = True
    return visit_occurrence, drug_exposure, condition_occurrence

if __name__ == '__main__':
    data = 'Andrea7 Wolf938\n===============\nRace:                White\nEthnicity:           Non-Hispanic\nGender:              M\nAge:                 55\nBirth Date:          1965-04-22\nMarital Status:      M\n--------------------------------------------------------------------------------\nALLERGIES:\nNo Known Allergies\n--------------------------------------------------------------------------------\nENCOUNTER\n2011-06-20 : Encounter at Cape Cod Vet Center : Encounter for Acute bronchitis (disorder)\nType: ambulatory\n   \n   MEDICATIONS:\n  2011-06-20 : Acetaminophen 325 MG Oral Tablet for Acute bronchitis (disorder)\n   \n   CONDITIONS:\n  2011-06-20 : Acute bronchitis (disorder)\n   \n   CARE PLANS:\n  2011-06-20 : Respiratory therapy\n                         Reason: Acute bronchitis (disorder)\n                         Activity: Recommendation to avoid exercise\n                         Activity: Deep breathing and coughing exercises\n   \n   REPORTS:\n   \n   OBSERVATIONS:\n   \n   PROCEDURES:\n  2011-06-20 : Sputum examination (procedure) for Acute bronchitis (disorder)\n   \n   IMMUNIZATIONS:\n   \n   IMAGING STUDIES:\n   \n--------------------------------------------------------------------------------\n'
    get_personal_info(data)
    get_medical_info(data)
