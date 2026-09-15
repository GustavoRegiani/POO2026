nome = input ("Nome: ")
idade = input ("idade")
idade = int(idade)
salario = float(input("Salário: R$"))

print (f"ola {nome}. voce tem {idade} anos")
if(salario >= 10000):
    print(f"Você ganha muito bem seu cuzao do carai: R${salario:.2f}")
elif(salario >= 200 ):
    print(f'Voce é um lixo ganha só R${salario:.2f}')
else:
    print(f'sai da rua mendigo do cão só R$ :{salario:.2f}')

