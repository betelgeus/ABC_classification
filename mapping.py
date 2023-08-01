# variables
lower_case = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
upper_case = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

# dicts
mapping_abc = {}
for k, v in zip(range(33), lower_case):
    if k < 10:
        mapping_abc['00_0'+str(k)] = v
    else:
        mapping_abc['00_'+str(k)] = v

upper_case_dict = {}
for k, v in zip(range(33), upper_case):
    if k < 10:
        upper_case_dict['01_0'+str(k)] = v
    else:
        upper_case_dict['01_'+str(k)] = v

printed_dict = {}
for k, v in zip(range(33), upper_case):
    if k < 10:
        printed_dict['02_0'+str(k)] = v
    else:
        printed_dict['02_'+str(k)] = v

mapping_abc.update(upper_case_dict)
mapping_abc.update(printed_dict)

draw_mapping_abc = {k: v for k, v in zip(range(33), lower_case)}
