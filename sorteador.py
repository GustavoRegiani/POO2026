import random

num = random.randint(1, 10)
print (num)
while(True):
    num2 = int(input('escreva um numero entre 1 e 10'))
    if(num2 >= 1 and num2 <=10):
        if(num2 == num):
            print ('acertou')
            break
        else:
            print('errou tente denovo')
    else:
        print('escreva o numero certo')

        