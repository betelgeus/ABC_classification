lower_case = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
upper_case = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

mapping_abc = {}

for k, v in zip(range(33), lower_case):
    if k < 10:
        mapping_abc['00_0'+str(k)+'_00'] = v
    else:
        mapping_abc['00_'+str(k)+'_00'] = v


upper_case_dict = {}

for k, v in zip(range(33), upper_case):
    if k < 10:
        upper_case_dict['01_0'+str(k)+'_00'] = v
    else:
        upper_case_dict['01_'+str(k)+'_00'] = v


mapping_abc.update(upper_case_dict)