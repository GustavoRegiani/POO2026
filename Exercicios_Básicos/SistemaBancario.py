class Conta:
    def __init__(self, numero, titular, saldo_inicial=0):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo_inicial

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de  R$ {valor} realizado com sucesso!")
            print(f"Novo saldo de {self.titular}: R$ {self.saldo:.2f}")
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de  R$ {valor} realizado com sucesso!")
            print(f"Novo saldo de {self.titular}: R$ {self.saldo:.2f}")
            return True
        else:
            print(f"Saldo insuficiente para saque!")
            print(f"Saldo atual de {self.titular}: R$ {self.saldo:.2f}")
            return False

    def transferir(self, destino, valor):
        print(f"Iniciando transferência de R$ {valor:.2f} para {destino.titular}...")
        # Reutilizamos o método sacar para validar o saldo
        if self.saldo >= valor:
            self.saldo -= valor
            destino.saldo += valor
            print(f"Transferência realizada com sucesso!")
            print(f"Saldo de {self.titular}: R$ {self.saldo:.2f}")
            print(f"Saldo de {destino.titular}: R$ {destino.saldo:.2f}")
            return True
        else:
            print(f"Transferência não realizada: Saldo insuficiente.")
            return False
        

 # 1. Criar duas contas bancárias
conta1 = Conta(1, "João", 1000.00)
conta2 = Conta(2, "Maria", 500.00)

# 2. Exibir o saldo inicial das contas
print("--- Saldo inicial ---")
print(f"{conta1.titular}: R$ {conta1.saldo:.2f}")
print(f"{conta2.titular}: R$ {conta2.saldo:.2f}")
print("-" * 20)

# 3. Realizar um depósito (João: +200)
conta1.depositar(200.00)
print("-" * 20)

# 4. Realizar um saque (Maria: -300)
conta2.sacar(300.00)
print("-" * 20)

# 5. Realizar uma transferência (João para Maria: 400)
conta1.transferir(conta2, 400.00)
print("-" * 20)

# 6. Testar saque com saldo insuficiente (Maria tenta sacar 1000)
conta2.sacar(1000.00)
print("-" * 20)

# 7. Exibir saldo final das contas
print("--- Saldo final ---")
print(f"{conta1.titular}: R$ {conta1.saldo:.2f}")
print(f"{conta2.titular}: R$ {conta2.saldo:.2f}")