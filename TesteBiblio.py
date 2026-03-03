import random
from  math import sqrt, pow, floor 

valor = random.randint(1, 10)
print (valor)
while(True):
    valor1 = input('digite um valor:')
    valor1 = int(valor1)
    if (valor1 >= 1 and valor1 <=10):
        break
if(valor1 == valor ):
    print('boa fera')
else:
    print('errou tente denovo')

cont = 0
while(cont <= 10):
    print ('0 a 10', cont )
    cont = cont + 1