"""
    BOT MHI v2
    - Analise em 1 minuto
    - Entradas para 1 minuto
    - Calcular as cores das velas de cada quadrado, ultimas 3 velas, minutos: 2, 3 e 4 / 7, 8 e 9
    - Entrar contra a maioria
    - Adicioando MHI2
    - Adicionado opção de binárias

    - Estrategia retirada do video https://www.youtube.com/watch?v=FePy1GY2wqQ	
"""
import datetime
import sys
import time
from datetime import datetime

from iqoptionapi.stable_api import IQ_Option

while True:
    try:
        email = (
            input("Digite seu email:: ")
        )
        break
    except:
        print("\n Errou")

while True:
    try:
        password = (
            input("Digite sua senha:: ")
        )
        break
    except:
        print("\n errou")


def stop(lucro, gain, loss):
    if lucro <= float("-" + str(abs(loss))):
        print("Stop Loss batido!")
        sys.exit()

    if lucro >= float(abs(gain)):
        print("Stop Gain Batido!")
        sys.exit()


def Martingale(valor, payout):
    lucro_esperado = valor * payout
    perca = float(valor)

    while True:
        if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
            return round(valor, 2)
            break
        valor += 0.01


def Payout(par):
    API.subscribe_strike_list(par, 1)
    while True:
        d = API.get_digital_current_profit(par, 1)
        if d != False:
            d = round(int(d) / 100, 2)
            break
        time.sleep(1)
    API.unsubscribe_strike_list(par, 1)

    return d


print(
    """
        Nao é um simples bot MHI
      https://www.youtube.com/channel/UCshkYTJUvfzyvkMsQ44G6_w
 ------------------------------------
 Source principal by IQcoding
 Modificado e aprimorado Por Mestre Wolf
 com Suport + Resistencia
 https://t.me/+wsvgAr0RJ0UxMDkx
"""
)


API = IQ_Option(email, password)
API.connect()
while True:
    try:
        modo = (
            input("DIGITE MODO, PRACTICE OU REAL:: ")
        )
        break
    except:
        print("\n Errou")

API.change_balance(f"{modo}")  # PRACTICE / REAL

if API.check_connect():
    print(" Conectado com sucesso!")
else:
    print(" Erro ao conectar")
    input("\n\n Aperte enter para sair")
    sys.exit()


while True:
    try:
        operacao = int(
            input("\n Deseja operar na\n  1 - Digital\n  2 - Binaria\n  :: ")
        )

        if operacao > 0 and operacao < 3:
            break
    except:
        print("\n Opção invalida")

while True:
    try:
        tipo_mhi = int(
            input(" Deseja operar a favor da\n  1 - Minoria\n  2 - Maioria\n  :: ")
        )

        if tipo_mhi > 0 and tipo_mhi < 3:
            break
    except:
        print("\n Opção invalida")


"""
    CONFIG DEFAULT
        operar binária
        minoria
        martingale 2
        stop loss 10
        stop gain 20
"""

par = input(" Indique uma paridade para operar: ").upper()
valor_entrada = float(input(" Indique um valor para entrar: "))
valor_entrada_b = float(valor_entrada)

martingale = int(input(" Indique a quantia de martingales: "))
martingale += 1

stop_loss = float(input(" Indique o valor de Stop Loss: "))
stop_gain = float(input(" Indique o valor de Stop Gain: "))

lucro = 0
payout = Payout(par)
while True:
    minutos = float(((datetime.now()).strftime("%S")))
    entrar = True if minutos > 58.0 else False
    print("Hora de entrar?", entrar, "/ Minutos:", minutos)
    velas = API.get_candles(par, 60, 3, time.time())
    j = 0
    support = (velas[j]["max"] > velas[j - 1]['max']
               and velas[j]['max'] > velas[j + 1]['max']
               and velas[j + 1]['max'] > velas[j + 2]['max']
               )

    resistencia = (velas[j]["min"] < velas[j - 1]['min']
                   and velas[j]['min'] < velas[j + 1]['min']
                   and velas[j + 1]['min'] < velas[j + 2]['min']
                   )
    # print(support)
    # print(resistencia)

    if resistencia == True:
        compra = False
        venda = True
        print(resistencia)
        print('venda')

    elif support == True:
        compra = True
        venda = False
        print(support)
        print('compra')

    else:
        compra = False
        venda = False
        print("esperando")
    if entrar and compra != venda:
        print("\n\nIniciando operação!")
        dir = False
        print("Verificando cores..", end="")
        velas = API.get_candles(par, 60, 3, time.time())

        velas[0] = (
            "g"
            if velas[0]["open"] < velas[0]["close"]
            else "r"
            if velas[0]["open"] > velas[0]["close"]
            else "d"
        )
        velas[1] = (
            "g"
            if velas[1]["open"] < velas[1]["close"]
            else "r"
            if velas[1]["open"] > velas[1]["close"]
            else "d"
        )
        velas[2] = (
            "g"
            if velas[2]["open"] < velas[2]["close"]
            else "r"
            if velas[2]["open"] > velas[2]["close"]
            else "d"
        )

        cores = velas[0] + " " + velas[1] + " " + velas[2]
        print(cores)

        if cores.count("g") > cores.count("r") and cores.count("d") == 0:
            dir = "put" if tipo_mhi == 1 else "call"
        if cores.count("r") > cores.count("g") and cores.count("d") == 0:
            dir = "call" if tipo_mhi == 1 else "put"

        if dir:
            dsakdpas ="call"
            rhgtrgehgt ="put"
            print("Direção:", dir)
            if compra == True and dir == dsakdpas:
                dir = "call"
            elif venda == True and dir == rhgtrgehgt:
                dir = "put"
            else:
                dir = False
            print("Direção:", dir)
            valor_entrada = valor_entrada_b
            time.sleep(61)
            for i in range(martingale):

                status, id = (
                    API.buy_digital_spot(par, valor_entrada, dir, 1)
                    if operacao == 1
                    else API.buy(valor_entrada, par, dir, 1)
                )

                if status:
                    blablabla = API.get_balance()
                    time.sleep(60)
                    while True:
                        betsies = API.get_balance()
                        valor = betsies - blablabla
                        print(valor)
                        if status:
                            valor = (
                                valor
                                if valor > 0
                                else float("-" + str(abs(valor_entrada)))
                            )
                            lucro += round(valor, 2)

                            print("Resultado operação: ", end="")
                            print(
                                "WIN /" if valor > 0 else "LOSS /",
                                round(valor, 2),
                                "/",
                                round(lucro, 2),
                                ("/ " + str(i) + " GALE" if i > 0 else ""),
                            )

                            valor_entrada = Martingale(valor_entrada, payout)

                            stop(lucro, stop_gain, stop_loss)

                            break

                    if valor > 0:
                        break

                else:
                    print("\nERRO AO REALIZAR OPERAÇÃO\n\n")

    time.sleep(0.5)
