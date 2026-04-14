class Livro:
    def __init__ (self, titulo, disponivel = True):
        self.titulo = titulo
        self.disponivel = disponivel

    def emprestar (self):
        if (self.disponivel == True):
            self.disponivel = False
            print(f"Livro {self.titulo} emprestado com sucesso")
        else :
           print(f"Livro {self.titulo} já está emprestado")
        
    def devolver (self):
        if(self.disponivel == False):
            self.disponivel = True
            print(f"Livro {self.titulo} devolvido com sucesso")
        else:
            print(f"Livro {self.titulo} não está emprestado")

livro = Livro("Pequeno Príncipe")

livro.emprestar()
livro.emprestar()
livro.devolver()
livro.devolver()