key_list = list()

with open('keys.txt') as keys_file:
    key = keys_file.readline()
    while key:
        key = key.rstrip('\n')
        key_list.append(key)
        key = keys_file.readline()

print(key_list)

exist_key = False
for i in key_list:
    if (i == '4631-af6d-469f-0cf5'):
        exist_key = True

if not exist_key: print('deo co')