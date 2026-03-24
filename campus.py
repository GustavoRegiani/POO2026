
class Campus:

    def __inif__ (self):
        self.name= ""
        self.cidade = ""
    
    def __str__(self):
        return f"Campus: {self.name}"
    
    
class Estudante:
    def __init__ (self):
        self.data_nasc = ""
        self.cpf = ""
        self.name = ""
        
    def __str__(self):
        return f"Estudante: {self.name}"

class Curso: 
    def __init__ (self):
        self.name = ""
        self.duracao = 0
        self.periodo = 0
        self.campus =  0 



Gustavo = Estudante()
Indio = Estudante()

Gustavo.name = "Gustavo" 
Indio.name= "kuan"


    