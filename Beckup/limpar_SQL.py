from pontuação import Pontuacao, db


def limpar_sql():
    db.connect(reuse_if_open=True)
    try:
        registros_removidos = Pontuacao.delete().execute()
        print(f"Registros removidos: {registros_removidos}")
    finally:
        db.close()


if __name__ == "__main__":
    limpar_sql()
