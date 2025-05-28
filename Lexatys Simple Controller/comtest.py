coms1 = ['COM1']
coms2 = ['COM1', 'COM3']

difCOM = list(set(coms1) ^ set(coms2))
print(difCOM)