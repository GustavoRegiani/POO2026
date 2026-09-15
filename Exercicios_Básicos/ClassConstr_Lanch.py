class Pedido:
    def __init__ (self, produto, quantidade, preco_unitario):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    def descrever(self):
        PrecoFinal = self.preco_unitario*self.quantidade
        return f"Pedido: {self.quantidade} x {self.produto} = Total: {PrecoFinal}"

pedido = Pedido("Misto Quente", 4, 7.00)
print(pedido.descrever())
