from datetime import datetime
import textwrap

# -------------------------------
# CLASSES DE MODELO
# -------------------------------

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Conta:
    def __init__(self, numero, cliente, agencia="0001", limite=500, limite_saques=3):
        self.agencia = agencia
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0
        self.extrato = ""
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"{datetime.now()} - Depósito: R$ {valor:.2f}\n"
            print("✅ Depósito realizado com sucesso!")
        else:
            print("❌ Valor inválido para depósito.")

    def sacar(self, valor):
        if valor <= 0:
            print("❌ Valor inválido para saque.")
        elif valor > self.saldo:
            print("❌ Saldo insuficiente.")
        elif valor > self.limite:
            print("❌ Valor excede o limite de saque.")
        elif self.numero_saques >= self.limite_saques:
            print("❌ Limite de saques diários atingido.")
        else:
            self.saldo -= valor
            self.extrato += f"{datetime.now()} - Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
            print("✅ Saque realizado com sucesso!")

    def exibir_extrato(self):
        print("\n=========== EXTRATO ===========")
        print(self.extrato if self.extrato else "Nenhuma movimentação realizada.")
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("===============================")

    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.cliente.nome}"


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def buscar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def criar_cliente(self):
        cpf = input("CPF: ")
        if self.buscar_cliente(cpf):
            print("⚠️ Já existe um cliente com este CPF.")
            return

        nome = input("Nome completo: ")
        data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
        endereco = input("Endereço (rua, nº, bairro, cidade/sigla): ")

        cliente = Cliente(nome, cpf, data_nascimento, endereco)
        self.clientes.append(cliente)
        print("✅ Cliente criado com sucesso!")

    def criar_conta(self):
        cpf = input("CPF do cliente: ")
        cliente = self.buscar_cliente(cpf)

        if not cliente:
            print("❌ Cliente não encontrado. Cadastre-o primeiro.")
            return

        numero_conta = len(self.contas) + 1
        conta = Conta(numero=numero_conta, cliente=cliente)
        self.contas.append(conta)
        cliente.adicionar_conta(conta)
        print(f"✅ Conta criada com sucesso! Número: {numero_conta}")

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self.contas:
            print("=" * 50)
            print(conta)

# -------------------------------
# MENU PRINCIPAL
# -------------------------------

def menu():
    menu = """\n
    ================ MENU ================
    [1]\tNovo Cliente
    [2]\tNova Conta
    [3]\tDepositar
    [4]\tSacar
    [5]\tExtrato
    [6]\tListar Contas
    [0]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "1":
            banco.criar_cliente()

        elif opcao == "2":
            banco.criar_conta()

        elif opcao == "3":
            cpf = input("CPF do cliente: ")
            cliente = banco.buscar_cliente(cpf)
            if cliente and cliente.contas:
                conta = cliente.contas[0]
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)
            else:
                print("❌ Cliente ou conta não encontrados.")

        elif opcao == "4":
            cpf = input("CPF do cliente: ")
            cliente = banco.buscar_cliente(cpf)
            if cliente and cliente.contas:
                conta = cliente.contas[0]
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)
            else:
                print("❌ Cliente ou conta não encontrados.")

        elif opcao == "5":
            cpf = input("CPF do cliente: ")
            cliente = banco.buscar_cliente(cpf)
            if cliente and cliente.contas:
                conta = cliente.contas[0]
                conta.exibir_extrato()
            else:
                print("❌ Cliente ou conta não encontrados.")

        elif opcao == "6":
            banco.listar_contas()

        elif opcao == "0":
            print("Saindo... 👋")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
