import time
import pandas as pd
import os
from supabase import create_client
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SECRET_KEY")
supabase = create_client(url, key)


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

    documento = input("Digite seu CPF: ")
    time.sleep(1)

    buscadados = supabase.table('tb_usuarios').select("*").filter('cpf','eq', documento).execute().data

    if len(buscadados) < 1:

        nome = input("Digite seu nome: ")
        senha = input("Cadastre sua senha: ")
        saldo = 0.00

        user_cad = []

        novo_usuario = {"nome": nome, "cpf": documento, "senha": senha, "saldo": saldo}

        user_cad.append(novo_usuario)

        #lista_usuarios.append(novo_usuario)

        try:

            data = json.loads(supabase.table('tb_usuarios').insert(user_cad).execute())

        except json.decoder.JSONDecodeError:
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

    listaUsuarios = supabase.table('tb_usuarios').select("id").execute().data

    if len(listaUsuarios) < 1:

        print("Não existe nenhum usuário cadastrado no banco de dados.")
        print("Cadastre novos usuários para utilizar o sistema")

        time.sleep(3)

        InicioSoftware()

    documento = input("Digite o documento: ")

    retornoUsuario = supabase.table("tb_usuarios").select("*").filter("cpf", "eq", documento).execute().data

    if len(retornoUsuario) < 1:
    
        print("Usuário não foi cadastrado no sistema!")
        print("Realize primeiramente o cadastro para ter acesso ao sistema!")

        time.sleep(3)

        InicioSoftware()
    
    else:

        senha = input("Digite sua senha: ")

        if retornoUsuario[0]["senha"] == senha:

            print("Usuário foi validado no sistema!")
            print(f"Bem-Vindo {retornoUsuario[0]['nome']}!")
            
            time.sleep(3)

            AcessarSistema(documento)
        
        else:

            print("Senha não foi validada! Tente realizar login novamente.")

            time.sleep(3)

            RealizarLogin()

def RealizarDeposito(cpf, valor):

    saldoAtual = supabase.table('tb_usuarios').select('saldo').filter('cpf', 'eq', cpf).execute().data

    saldoAtual2 = float(saldoAtual[0]["saldo"])

    novoSaldo = saldoAtual2 + valor

    data_hora_atual = datetime.now()
    data_hora_atual_texto = data_hora_atual.strftime("%d/%m/%Y %H:%M")


    try:

        data = supabase.table("tb_usuarios").update({"saldo": novoSaldo}).filter('cpf', 'eq', cpf).execute()

    except json.decoder.JSONDecodeError:
        
        print("")
    
    try:

        data2 = supabase.table("tb_movimentacoes").insert({"data_movimentacao": data_hora_atual_texto, "cpf_movimentacao": cpf, "tipo_movimentacao": "Depósito", "valor": valor}).execute()

    except json.decoder.JSONDecodeError:
        
        print("")

    

def RealizarSaque(cpf, valor):

    saldoAtual = supabase.table('tb_usuarios').select('saldo').filter('cpf', 'eq', cpf).execute().data
    saldoAtual2 = float(saldoAtual[0]["saldo"])
    novoSaldo = saldoAtual2 - valor

    data_hora_atual = datetime.now()
    data_hora_atual_texto = data_hora_atual.strftime("%d/%m/%Y %H:%M")

    try:

        supabase.table("tb_usuarios").update({"saldo": novoSaldo}).filter('cpf', 'eq', cpf).execute()

    except json.decoder.JSONDecodeError:
        
        print("")
    
    try:
        supabase.table("tb_movimentacoes").insert({"data_movimentacao": data_hora_atual_texto, "cpf_movimentacao": cpf, "tipo_movimentacao": "Saque", "valor": valor}).execute()
    except json.decoder.JSONDecodeError:
        print("")

def RealizarTransferencia(cpf, cpf_destino, valor):

    userOrigem = supabase.table("tb_usuarios").select("nome, saldo").filter("cpf", 'eq', cpf).execute().data
    userDestino = supabase.table("tb_usuarios").select("nome, saldo").filter("cpf", 'eq', cpf_destino).execute().data

    novoSaldoOrigem = userOrigem[0]["saldo"] - valor
    novoSaldoDestino = userDestino[0]["saldo"] + valor

    data_hora_atual = datetime.now()
    data_hora_atual_texto = data_hora_atual.strftime("%d/%m/%Y %H:%M")

    try:
        supabase.table("tb_usuarios").update({"saldo": novoSaldoOrigem}).filter('cpf', 'eq', cpf).execute()
    except json.decoder.JSONDecodeError:
        print("")
    try:
        supabase.table("tb_usuarios").update({"saldo": novoSaldoDestino}).filter('cpf', 'eq', cpf_destino).execute()
    except json.decoder.JSONDecodeError:
        print("")
    try:
        supabase.table("tb_movimentacoes").insert({"data_movimentacao": data_hora_atual_texto, "cpf_movimentacao": cpf, "tipo_movimentacao": "Transferencia Enviada", "usuario_destino": cpf_destino, "valor": valor}).execute()
    except json.decoder.JSONDecodeError:
        print("")
    try:
        supabase.table("tb_movimentacoes").insert({"data_movimentacao": data_hora_atual_texto, "cpf_movimentacao": cpf_destino, "tipo_movimentacao": "Transferencia Recebida", "usuario_origem": cpf, "valor": valor}).execute()
    except json.decoder.JSONDecodeError:
        print("")
    

def AlterarSenha(cpf, novasenha):

    try:
        supabase.table("tb_usuarios").update({"senha": novasenha}).filter('cpf', 'eq', cpf).execute()
    except json.decoder.JSONDecodeError:
        print("")

def AcessarSistema(cpf):

    os.system('cls') or None

    dadosUser = supabase.table('tb_usuarios').select("*").filter("cpf", "eq", cpf).execute().data

    user_usuario = dadosUser[0]["nome"]
    user_saldo = dadosUser[0]["saldo"]
    user_senha = dadosUser[0]["senha"]
    
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

        userDestino = supabase.table("tb_usuarios").select("nome").filter("cpf", "eq", documento_destino).execute().data
        
        if len(userDestino) < 1:

            print("Não localizado documento de destino.")
            print("Tente novamente!")

            time.sleep(3)

            AcessarSistema(cpf)
        
        else:

            print("Usuário destino: "+ userDestino[0]["nome"])

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

        dataMovimentacao = []
        tipo = []
        valor = []

        dadosMovimentacoes = supabase.table("tb_movimentacoes").select("*").filter("cpf_movimentacao", "eq", cpf).execute().data
        
        if len(dadosMovimentacoes) > 0:

            for i in dadosMovimentacoes:
                
                dataMovimentacao.append(i["data_movimentacao"])

                if (i["tipo_movimentacao"] == "Transferencia Enviada") or (i["tipo_movimentacao"] == "Transferencia Recebida"):
                    if (i["usuario_destino"] != None):

                        usuarioDestino = supabase.table("tb_usuarios").select("nome").filter("cpf", "eq", i["usuario_destino"]).execute().data

                        tipoDaMovimentacao = f"{i['tipo_movimentacao']} para {usuarioDestino[0]['nome']}"

                        tipo.append(tipoDaMovimentacao)

                    elif (i["usuario_origem"] != None):

                        usuarioOrigem = supabase.table("tb_usuarios").select("nome").filter("cpf", "eq", i["usuario_origem"]).execute().data

                        tipoDaMovimentacao = f"{i['tipo_movimentacao']} de {usuarioOrigem[0]['nome']}"

                        tipo.append(tipoDaMovimentacao)

                else:

                    tipo.append(i["tipo_movimentacao"])

                valor.append(i["valor"])


            
            tabela = pd.DataFrame((zip(dataMovimentacao, tipo, valor)), columns=["Data da Movimentação", "Tipo Movimentacao", "Valor"])

            tabela.index += 1

            print(tabela)

        else:
            print("Não foram localizadas movimentações!")
        
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