import os

print("enviando email")
comando_email = "git config user.email \"gustavoregianidesouza@gmail.com\"  "
os.system(comando_email)

print ("➕adicionando")
comando1 = "git add *"
os.system(comando1)
mensagem = input("🔠Mensagem do commit: ")
if (len(mensagem) < 2):
    print("mensagem muito curta ‼️‼️‼️")
    mensagem = input("🔠Mensagem do commit: ")

print("👍registrando alterações:")
comando2 = f"git commit -m \"{mensagem}\" "
os.system(comando2)

print('↩️retornando alterações')
comando3 = "git push"
os.system(comando3)