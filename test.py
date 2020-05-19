x = '6d5b'

for i in x:
    try:
        int('0x' + i, 16)
    except ValueError as err:
        print("Error!")
        print(err)
        print("End of Error!")
