from peewee import *


db = SqliteDatabase('pontuacao.db')


class Pontuacao(Model):
    nome = CharField()
    tempo = FloatField(default=0.0)

    class Meta:
        database = db


def garantir_estrutura_banco():
    db.connect(reuse_if_open=True)
    try:
        tabela_existe = db.execute_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pontuacao'"
        ).fetchone()

        if tabela_existe is None:
            db.create_tables([Pontuacao])
            return

        colunas = [
            linha[1]
            for linha in db.execute_sql('PRAGMA table_info(pontuacao)').fetchall()
        ]

        if 'tempo' not in colunas:
            db.execute_sql('ALTER TABLE pontuacao ADD COLUMN tempo REAL DEFAULT 0.0')
    finally:
        db.close()


garantir_estrutura_banco()