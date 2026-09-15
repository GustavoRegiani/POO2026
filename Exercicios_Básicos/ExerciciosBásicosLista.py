numeros = ["0"] * 10
for i in range (0 , len('numeros')-1 ):
    print(numeros[i])

a = 1
while(a<=20):
    print(a)
    a+=1

def soma_valores (n1, n2):
    return n1+n2

n1 = int(input('fale um valor'))
n2 = int(input('fale outro valor'))

print(soma_valores(n1, n2))

lista = [""] * 5
lista[0] = 'nesp'
lista[1] = 'curitiba'
lista[2] ='maringa'
lista[3] = 'londrina'
lista[4] = 'pvai'

for i in lista:
    print (i)

def verificar_par (n1):
    if (n1%2 == 0):
      return True
    else:
         return False

num1 = int(input("escreve um numero:"))
           
if(verificar_par(num1)):
     print("é par")
else:
     print("é inpar")

while(True):
    numero = int(input("digite um numero inteiro"))
    if (numero == 0):
        print("programa encerrado")
        break

