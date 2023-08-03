"""
    Словари с маппингами букв русского алфавита.
"""

# алфавит
LOWER_CASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
UPPER_CASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

# словари с маппингами
mapping_abc = {}
for k, v in zip(range(33), LOWER_CASE):
    if k < 10:
        mapping_abc['00_0'+str(k)] = v
    else:
        mapping_abc['00_'+str(k)] = v

upper_case_dict = {}
for k, v in zip(range(33), UPPER_CASE):
    if k < 10:
        upper_case_dict['01_0'+str(k)] = v
    else:
        upper_case_dict['01_'+str(k)] = v

printed_dict = {}
for k, v in zip(range(33), UPPER_CASE):
    if k < 10:
        printed_dict['02_0'+str(k)] = v
    else:
        printed_dict['02_'+str(k)] = v

mapping_abc.update(upper_case_dict)
mapping_abc.update(printed_dict)

draw_mapping_abc = dict(zip(range(33), LOWER_CASE))
