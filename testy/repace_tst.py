def replace_str(str_to_fix):
    corected = {'0':'O', '-':'_'}
    for i in corected.keys():
        str_fixed = str_to_fix.replace(i,corected[i])
        str_to_fix = str_fixed
    return str_fixed

ddd = 'asdf0-000'
sss = '00ds'
zzz = 's-d-'

ddd = replace_str(ddd)
sss = replace_str(sss)
zzz = replace_str(zzz)

print(ddd, sss, zzz)