num1 = input('fala 1 numero ae:')
opr = input('falaum operador matematico ae:')
num2 = input('fala oto numero ae:')
num1=int(num1)
num2=int(num2)

if(opr == '*'):
    resultado=num1*num2
    print(resultado)
elif(opr == '+'):
    resultado=num1+num2
    print(resultado)
elif(opr == '-'):
    resultado=num1-num2
    print(resultado)
elif(opr == '/'):
    resultado=num1/num2
    print(resultado)
else:
    print(f'escreve um certo fdp')
