import os
import time
import pandas as pd

class Usuarios:
    def __init__(self, cpf, usuario, senha, saldo):
        self.cpf = cpf
        self.usuario = usuario
        self.senha = senha
        self.saldo = saldo


class Movimentacoes:
    def __init__(self, cpf, tipo_movimentacao, valor):
        self.cpf = cpf
        self.tipo_movimentacao = tipo_movimentacao
        self.valor = valor

lista_usuarios = []
lista_movimentacoes = []

def CriarUsuario():

    os.system('cls') or None

    print("Sistema de Cadastramento de usuários!")
    print("-----------------------------------------------------------------")
    print("")

    validar_documento = 0
    documento = input("Digite seu CPF: ")

    for i in lista_usuarios:

        if i.cpf == documento:
            validar_documento = 1
    
    if validar_documento == 0:

        nome = input("Digite seu nome: ")
        senha = input("Cadastre sua senha: ")
        saldo = 0.00

        novo_usuario = Usuarios(documento, nome, senha, saldo)

        lista_usuarios.append(novo_usuario)

        print("Usuário cadastrado com sucesso!")

        time.sleep(3)

        InicioSoftware()

    else:

        print("Este documento já esta cadastrado. Realize login para continuar!")

        time.sleep(3)

        InicioSoftware()


def RealizarLogin():

    os.system('cls') or None

    validar_login = 0
    validar_senha = 0

    print("Realize o Login na DIO Python Bank")
    print("-----------------------------------------------------------------")
    print("")

    if len(lista_usuarios) < 1:

        print("Não existe nenhum usuário cadastrado no banco de dados.")
        print("Cadastre novos usuários para utilizar o sistema")

        time.sleep(3)

        InicioSoftware()

    documento = input("Digite o documento: ")

    for i in lista_usuarios:
        if i.cpf == documento:

            user_usuario = i.usuario
            user_senha = i.senha
            validar_login = 1
    
    if validar_login == 0:

        print("Usuário não foi cadastrado no sistema!")
        print("Realize primeiramente o cadastro para ter acesso ao sistema!")

        time.sleep(3)

        InicioSoftware()
    
    else:

        senha = input("Digite sua senha: ")

        if user_senha == senha:

            print("Usuário foi validado no sistema!")
            print(f"Bem-Vindo {user_usuario}!")
            
            time.sleep(3)

            AcessarSistema(documento)
        
        else:

            print("Senha não foi validada! Tente realizar login novamente.")

            time.sleep(3)

            RealizarLogin()

def RealizarDeposito(cpf, valor):

    for i in lista_usuarios:
        if i.cpf == cpf:

            i.saldo = i.saldo + valor

            movimentacao = Movimentacoes(cpf, "Deposito", valor)
            lista_movimentacoes.append(movimentacao)

def RealizarSaque(cpf, valor):

    for i in lista_usuarios:
        if i.cpf == cpf:
            i.saldo = i.saldo - valor

            movimentacao = Movimentacoes(cpf, "Saque", valor)
            lista_movimentacoes.append(movimentacao)

def RealizarTransferencia(cpf, cpf_destino, valor):

    for i in lista_usuarios:
        if i.cpf == cpf:

            i.saldo = i.saldo - valor

            movimentacao = Movimentacoes(cpf, "Transferencia Enviada", valor)
            lista_movimentacoes.append(movimentacao)
        
        if i.cpf == cpf_destino:

            i.saldo = i.saldo + valor

            movimentacao = Movimentacoes(cpf_destino, "Transferencia Recebida", valor)
            lista_movimentacoes.append(movimentacao)
    

def AlterarSenha(cpf, novasenha):

    for i in lista_usuarios:
        if i.cpf == cpf:
            i.senha = novasenha    

def AcessarSistema(cpf):

    os.system('cls') or None

    for i in lista_usuarios:
        if i.cpf == cpf:

            user_usuario = i.usuario
            user_saldo = i.saldo
            user_senha = i.senha
    
    print(f"DIO Python Bank - Bem-vindo {user_usuario}")
    print("-----------------------------------------------------------------")
    print("")

    print(f"Seu saldo atual é de: R$ {user_saldo:.2f}")
    print("")
    print("O que deseja fazer?")

    print("""
    (1) Deposito
    (2) Transferencia
    (3) Saque
    (4) Extrato
    (5) Alterar Senha
    (6) Sair
    """)

    codigo = int(input("digite o código: "))

    if codigo == 1:

        os.system('cls') or None

        print(f"DIO Python Bank - Bem-vindo {user_usuario}")
        print("-----------------------------------------------------------------")
        print("")

        print(f"Seu saldo atual é de: R$ {user_saldo:.2f}")
        print("")
        deposito = input("Insira o valor do deposito: ")
        depositoCorrigido = deposito.replace(",", ".")
        valor_deposito = float(depositoCorrigido)

        senha_autenticacao = input("Insira senha para validar a transação: ")

        if user_senha == senha_autenticacao:

            RealizarDeposito(cpf, valor_deposito)

            print("Deposito realizado com sucesso!")

            time.sleep(3)

            AcessarSistema(cpf)

        else:

            print("Movimentação não validada! Tente novamente.")

            time.sleep(3)

            AcessarSistema(cpf)
    
    elif codigo == 3:

        os.system('cls') or None

        print(f"DIO Python Bank - Bem-vindo {user_usuario}")
        print("-----------------------------------------------------------------")
        print("")

        print(f"Seu saldo atual é de: R$ {user_saldo:.2f}")
        print("")
        saque = input("Insira o valor de saque: ")
        saqueCorrigido = saque.replace(",", ".")
        valor_saque = float(saqueCorrigido)

        if valor_saque > user_saldo:

            print("Você não possui saldo suficiente para realizar essa movimentação.")
            print("Deposite recursos e tente novamente")

            time.sleep(3)

            AcessarSistema(cpf)


        senha_autenticacao = input("Insira senha para validar a transação: ")

        if user_senha == senha_autenticacao:

            RealizarSaque(cpf, valor_saque)

            print("Saque realizado com sucesso!")

            time.sleep(3)

            AcessarSistema(cpf)

        else:

            print("Movimentação não validada! Tente novamente.")

            time.sleep(3)

            AcessarSistema(cpf)

    elif codigo == 2:

        os.system('cls') or None

        print(f"DIO Python Bank - Bem-vindo {user_usuario}")
        print("-----------------------------------------------------------------")
        print("")

        print(f"Seu saldo atual é de: R$ {user_saldo:.2f}")
        print("")
        documento_destino = input("Insira o documento destino: ")
        valida_documento_destino = 0

        for i in lista_usuarios:
            if i.cpf == documento_destino:
                valida_documento_destino = 1
                destino_usuario = i.usuario
        
        if valida_documento_destino == 0:

            print("Não localizado documento de destino.")
            print("Tente novamente!")

            time.sleep(3)

            AcessarSistema(cpf)
        
        else:

            print(f"Usuário destino: {destino_usuario}")

            print("Está correto?")

            print("""
    (1) Sim
    (2) Não
            """)

            codigo = int(input("Insira o codigo: "))

            if codigo == 1:

                valor = input("Insira o valor para transferencia: ")
                valorCorrigido = valor.replace(",",".")
                valor_tranferencia = float(valorCorrigido)

                if user_saldo < valor_tranferencia:

                    print("Você não possui saldo suficiente para esta movimentação")
                    time.sleep(3)

                    AcessarSistema(cpf)

                else:

                    senha_autenticacao = input("Insira senha para validar a transação: ")

                    if user_senha == senha_autenticacao:

                        RealizarTransferencia(cpf, documento_destino, valor_tranferencia)

                        print("Transferencia realizada com sucesso!")

                        time.sleep(3)

                        AcessarSistema(cpf)

                    else:

                        print("Movimentação não validada! Tente novamente.")

                        time.sleep(3)

                        AcessarSistema(cpf)
            
            else:
                
                print("Movimentação cancelada pelo usuário.")

                time.sleep(3)

                AcessarSistema(cpf)

    elif codigo == 4:

        os.system('cls') or None

        print(f"DIO Python Bank - Bem-vindo {user_usuario}")
        print("-----------------------------------------------------------------")
        print("")
        print("Extrato Bancário")
        print("")
        print("")

        extrato_bancario_usuario = []
        tipo = []
        valor = []
        n = 1
        
        for i in lista_movimentacoes:
            if i.cpf == cpf:
                tipo.append(i.tipo_movimentacao)
                valor.append(i.valor)
        
        tabela = pd.DataFrame((zip(tipo, valor)), columns=["Tipo Movimentacao", "Valor"])

        tabela.index += 1

        print(tabela)

        print("")
        print("")

        input("Pressione ENTER para voltar")

        AcessarSistema(cpf) 


    elif codigo == 5:

        os.system('cls') or None

        print(f"DIO Python Bank - Bem-vindo {user_usuario}")
        print("-----------------------------------------------------------------")
        print("")

        senha_autenticacao = input("Digite sua senha atual: ")

        if senha_autenticacao == user_senha:

            nova_senha = input("Digite a nova senha: ")
            AlterarSenha(cpf, nova_senha)

            print("Senha foi alterada com sucesso")
            AcessarSistema(cpf)

        else:

            print("Senha não confere.")
            print("Para sua segurança iremos realilzar logoff")
            print("DIO Python Bank agradece sua preferencia!")

            time.sleep(3)

            InicioSoftware()

    elif codigo == 6:

        os.system('cls') or None

        print(f"DIO Python Bank - Bem-vindo {user_usuario}")
        print("-----------------------------------------------------------------")
        print("")

        print("Deseja realmente sair do sistema?")

        print("""
    (1) Sim
    (2) Não
        """)

        codigo = int(input("Digita sua opção: "))

        if codigo == 1:

            os.system('cls') or None

            print("Obrigado por utilizar a DIO Python Bank!")

            time.sleep(3)

            InicioSoftware()
        
        else:

            AcessarSistema(cpf)

    else:

        print("Código Invalido. Tente novamente.")

        time.sleep(3)

        AcessarSistema(cpf)


    


def InicioSoftware():

    os.system('cls') or None

    print("Bem vindo ao DIO Python Bank")
    print("Selecione a movimentação desejada: ")
    print("""
    (1) Criar novo usuário
    (2) Realizar login
    """)

    codigo = int(input("Digite o código: "))

    if codigo == 1:
        CriarUsuario()
    elif codigo == 2:
        RealizarLogin()
    else:
        print("Código Invalido!")



InicioSoftware()