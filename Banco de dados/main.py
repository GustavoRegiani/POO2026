from models import Contato, conexao 


while True:

    print("\n===== AGENDA DE CONTATOS =====")
    print("1 - Cadastrar contato")
    print("2 - Ver todos os contatos")
    print("3 - Buscar contato pelo nome")
    print("4 - Editar contato pelo ID")
    print("5 - Excluir contato pelo ID")
    print("6 - Sair")

    opção = input("Escolha uma opção: ")

    if opção == "1":
        nome = input("Digite o nome do contato: ")
        telefone = input("Digite o telefone do contato: ")

        contato = Contato.create(
            nome=nome,
            telefone=telefone
        )

        print(f"Contato {contato.nome} cadastrado com sucesso!")
    elif opção == "2":
        contatos = Contato.select()

        if not contatos.exists():
             print("Nenhum contato cadastrado.")
        else:
            print("\n===== LISTA DE CONTATOS =====")
            for contato in contatos:
               print(f"ID: {contato.id} - {contato}")

    elif opção == "3":
        nome = input("Digite o nome ou parte do nome: ")

        contatos = Contato.select().where(
            Contato.nome.contains(nome)
        )

        if not contatos.exists():
            print("Nenhum contato encontrado.")
        else:
             for contato in contatos:
              print(f"ID: {contato.id} - {contato}")

    elif opção == "4":
        
            id_contato = input("Digite o ID do contato: ")

            contato = Contato.get_or_none(Contato.id == id_contato)

            if contato is None:
                print("Contato não encontrado.")
            else:
                print(f"Contato atual: {contato}")

            novo_nome = input("Novo nome (Enter para manter): ")
            novo_telefone = input("Novo telefone (Enter para manter): ")

            if novo_nome != "":
                contato.nome = novo_nome

            if novo_telefone != "":
                contato.telefone = novo_telefone

            contato.save()

            print("Contato atualizado com sucesso!")

    elif opção == "5":
        id_contato = input("Digite o ID do contato: ")

        contato = Contato.get_or_none(Contato.id == id_contato)

        if contato is None:
            print("Contato não encontrado.")
        else:
            contato.delete_instance()
            print("Contato excluído com sucesso!")
    elif opção == "6":
        print("Saindo do programa...")
        conexao.close()
        break
    else:
        print("Opção inválida. Tente novamente.")

    
