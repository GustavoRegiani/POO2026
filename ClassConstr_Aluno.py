class Aluno:
    def __init__(self, nome, idade, curso, nota):
        self.nome = nome
        self.idade = idade
        self.curso = curso
        self.nota=nota

    def apresentar(self):
        return(f"Olá, meu nome é {self.nome}, tenho {self.idade} anos e faço o curso de {self.curso}.")
    
    def calcular_media(self):
        nota1=self.nota[0]
        nota2=self.nota[1]
        nota3=self.nota[2]
        media = (nota1+nota2+nota3)/3

        return (media)


aluno1 = Aluno("Gustavo", 17, "informática", [8.0, 8.0, 9.0] )
print(aluno1.apresentar())
print(aluno1.calcular_media())