from typing_extensions import Self
import pyautogui as pag, \
    os, \
    time
import subprocess

from datetime import datetime

def armazena_Log(log, name='log'):
    with open(f'./{name}.txt', 'a') as arquivolog:
        arquivolog.write('\n' + log)

def print_log(txt, error=False):
    txt = datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M-%S: ') + txt
    print(txt)
    armazena_Log(txt)
    if error:
        armazena_Log(txt, 'log_error')


class Elementos:

    # verifica qual o nível de confiaça necessária para localizar um determinado elemento #
    def pegaConfianca(printElemento):
        if printElemento == None:
            print_log('Nenhum elemento foi atribuido')
            return False

        conf = 1
        cords = pag.locateCenterOnScreen(printElemento, confidence=conf)
        while cords is None:
            if conf == 0:
                return conf
            cords = pag.locateCenterOnScreen(printElemento, confidence=conf)
            if cords is None:
                conf = conf - 0.1
            else:
                return conf

    # retorna as cordenadas do centro de um elemento #
    def retCordsCentro(printElemento=None, conf=1):
        if printElemento == None:
            print_log('Nenhum elemento foi atribuido')
            return False

        return pag.locateCenterOnScreen(printElemento, confidence=conf)

    # clica em uma determinada tecla por uma determinada quantidade de vezes #
    def tecla(tecla=None, vezes=1):
        if tecla == 'None': # verifica se uma tecla foi atribuida
            print_log('Nenhuma tecla foi atribuida')
            return False # retorna falso se não for atribuida uma tecla

        pag.press(tecla, vezes)
        return True

    # abre um programa utilizando o seu loal #
    def abrirPrograma(localPrograma=None):
        if localPrograma == None:
            print_log('Nenhum programa foi atribuido')
            return False

        # os.system('"{}"'.format(localPrograma))
        os.startfile('"{}"'.format(localPrograma))
        return True

    # verifica se um elemento está presente na tela, utilizando uma print do mesmo #
    # usa o nível de confiança para encontrar elemento na tela#
    def checaElemento(printElemento, conf=1):
        return True if pag.locateCenterOnScreen(printElemento, confidence=conf) else False

    # espera até que o elemento apareça na tela#
    def esperaElemento(printElemento, conf=1, timeout=999999):
        tempo = 0
        while Elementos.checaElemento(printElemento, conf) == False:
            time.sleep(0.5)
            tempo += 0.5
            if tempo > timeout:
                return False

        time.sleep(2)
        print_log('Elemento encontrado')
        return True

    # espera até que o elemento apareça na tela e clica nele# 
    def esperaElementoClica(printElemento, conf=1, timeout=999999, botaoMouse='l', quantidadeDeClicks=1):
        valida = Elementos.esperaElemento(printElemento, conf, timeout)
        if valida == True:
            Elementos.clicaNoCentro(printElemento, conf, botaoMouse, quantidadeDeClicks)

    # simula a digitação um determinado texto #
    def escreve(texto=None, intervalo=0):
        if texto == None:
            print_log('Nenhum texto foi atribuido')
            return False

        pag.write(texto, intervalo)
        return True

    # clica no centro do elemento com a confiança e o botão do mouse selecionado #
    # use "l" para esquerda e "d" para direait#
    def clicaNoCentro(printElemento=None, conf=1, botaoMouse='l', quantidadeDeClicks=1):
        coordenadas = Elementos.retCordsCentro(printElemento, conf)
        if coordenadas != False:
            time.sleep(0.5)
            pag.click(coordenadas.x, coordenadas.y, button='left' if botaoMouse.lower() == 'l' or botaoMouse.lower() == 'left' else 'right', clicks=quantidadeDeClicks)
