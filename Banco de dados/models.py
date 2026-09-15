from peewee import *
from datetime import datetime

conexao = SqliteDatabase('Meu_Banco.db')

class BaseModel(Model):
    class Meta:
        database = conexao

class Contato(BaseModel):
    nome = CharField()
    telefone = CharField()
    data_cadastro = DateTimeField(default=datetime.now)

    def __str__(self):
        return (f"{self.nome} - {self.telefone} - {self.data_cadastro}")


conexao.connect()

conexao.create_tables([Contato])

