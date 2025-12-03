#Danilo ferreira coelho
import re
from class_banco import *

cpfs_cadastrados = []

def validar_cpf(cpf):
    if not cpf.isdigit() or len(cpf) != 11:
        print("Erro! O CPF deve ter 11 dígitos numéricos.")
        return False

    if cpf in cpfs_cadastrados:
        print("Erro! Este CPF já está cadastrado.")
        return False

    if cpf == cpf[0] * 11:
        print("Erro! CPF inválido (dígitos repetidos).")
        return False

    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto1 = (soma1 * 10) % 11
    if resto1 == 10:
        resto1 = 0

    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto2 = (soma2 * 10) % 11
    if resto2 == 10:
        resto2 = 0

    if int(cpf[9]) == resto1 and int(cpf[10]) == resto2:
        return True
    else:
        print("Erro! CPF inválido.")
        return False


def validar_telefone(telefone):
    telefone = telefone.strip()
    if not telefone.startswith("(") or ")" not in telefone:
        print("Telefone inválido! Deve iniciar com (DD) ou (código do país). Ex: (89)99999-9999 ou (1)9999999999.")
        return False

    telefone_numerico = re.sub(r'\D', '', telefone)
    if len(telefone_numerico) < 10 or len(telefone_numerico) > 13:
        print("Telefone inválido! Deve ter entre 10 e 13 dígitos.")
        return False

    if telefone_numerico == telefone_numerico[0] * len(telefone_numerico):
        print("Telefone inválido! Dígitos repetidos não são permitidos.")
        return False

    return True


def menu_principal():
    print("\n+----------- Menu Principal -----------+")
    print(":1 - Fazer login                       :")
    print(":2 - Criar conta                       :")
    print(":0 - Sair                              :")
    print("+--------------------------------------+")


def menu_conta():
    print("\n+------------ Menu Conta --------------+")
    print(":1 - Depositar                         :")
    print(":2 - Transferir                        :")
    print(":3 - Sacar                             :")
    print(":4 - Estatísticas                      :")
    print(":0 - Sair                              :")
    print("+--------------------------------------+")


contas = []
contador_contas = 0

while True:
    menu_principal()
    escolha = input("Escolha uma opção: ")

    if escolha == "0":
        print("Encerrando o sistema. Obrigado por utilizar.")
        break

    elif escolha == "2":
        print("\n+---------- Criação de Conta ----------+")
        while True:
            titular = input("Digite o nome do titular: ").strip()
            titular = ' '.join(titular.split())
            if len(titular.replace(' ', '')) >= 3 and all(c.isalpha() or c == ' ' for c in titular):
                break
            else:
                print("Nome inválido! Deve ter pelo menos 3 letras e não conter números ou símbolos.")

        while True:
            telefone = input("Digite seu telefone com (DDD) ou (código do país): ").strip()
            if validar_telefone(telefone):
                break

        endereco = input("Digite seu endereço: ").strip()

        while True:
            cpf = input("Digite seu CPF (somente números): ").strip()
            if validar_cpf(cpf):
                cpfs_cadastrados.append(cpf)
                break

        while True:
            senha = input("Crie uma senha de 6 dígitos: ").strip()
            if len(senha) == 6 and senha.isdigit():
                break
            else:
                print("Senha inválida! A senha deve ter exatamente 6 dígitos numéricos.")

        numero_conta = 1000 + contador_contas
        nova_conta = Banco(numero_conta, titular, senha, cpf, endereco, telefone)
        contas.append(nova_conta)
        contador_contas += 1
        print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

    elif escolha == "1":
        try:
            numero_login = int(input("Digite o número da conta: "))
            senha_login = input("Digite a senha: ").strip()
        except ValueError:
            print("Entrada inválida, tente novamente.")
            continue

        conta_logada = next((c for c in contas if c.numero == numero_login and c.senha == senha_login), None)

        if conta_logada:
            print(f"Bem-vindo, {conta_logada.titular}!")
            while True:
                menu_conta()
                opcao = input("Escolha uma opção: ")

                if opcao == "0":
                    print("Saindo da conta...")
                    break

                elif opcao in ["1", "2", "3", "4"]:
                    senha_tentativa = input("Digite sua senha novamente para confirmar: ").strip()
                    if senha_tentativa != conta_logada.senha:
                        print("Senha incorreta. Operação não autorizada.")
                        continue

                    if opcao == "1":
                        try:
                            valor = float(input("Digite o valor a depositar: "))
                            conta_logada.depositar(valor)
                        except ValueError:
                            print("Valor inválido. Digite apenas números.")

                    elif opcao == "2":
                        tipo_transferencia = input("Deseja transferir para (1) Número da conta ou (2) PIX (CPF)? ").strip()
                        destino_conta = None

                        if tipo_transferencia == "1":
                            try:
                                destino_numero = int(input("Digite o número da conta de destino: "))
                                destino_conta = next((c for c in contas if c.numero == destino_numero), None)
                            except ValueError:
                                print("Número de conta inválido.")
                                continue
                        elif tipo_transferencia == "2":
                            destino_cpf = input("Digite o CPF do destinatário: ").strip()
                            destino_conta = next((c for c in contas if c.pix == destino_cpf), None)
                        else:
                            print("Opção inválida.")
                            continue

                        if destino_conta:
                            try:
                                valor = float(input("Digite o valor a transferir: "))
                                conta_logada.transferir(destino_conta, valor)
                            except ValueError:
                                print("Valor inválido. Digite apenas números.")
                        else:
                            print("Conta de destino não encontrada.")

                    elif opcao == "3":
                        try:
                            valor = float(input("Digite o valor a sacar: "))
                            conta_logada.sacar(valor)
                        except ValueError:
                            print("Valor inválido. Digite apenas números.")

                    elif opcao == "4":
                        print(f"\n--- Dados da Conta ---")
                        print(f"Número da conta: {conta_logada.numero}")
                        print(f"Titular: {conta_logada.titular}")
                        print(f"CPF: {conta_logada.cpf}")
                        print(f"Chave PIX (CPF): {conta_logada.pix}")
                        print(f"Endereço: {conta_logada.endereco}")
                        print(f"Telefone: {conta_logada.telefone}")
                        print(f"Saldo atual: R${conta_logada.saldo:,.2f}")

                else:
                    print("Opção inválida. Tente novamente.")
        else:
            print("Conta ou senha incorreta. Tente novamente.")

    else:
        print("Opção inválida. Tente novamente.")