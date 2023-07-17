import pyautogui as pag
import win32gui
import time
import win32con
import os
import pathlib as ptl
from datetime import datetime

class interface:
    mouse = {
            'botao':'left',
            'cliques': 1

        }
    keybo =  {
            'intervalo':'0.2',
            'apertar': 1
        }

class badbot:
    def __init__(self, conf=0.8, classe_processo=None, nome_processo=None):
        self.conf = conf
        self.classe_processo = classe_processo
        self.nome_processo = nome_processo
        self.localPrograma = None
        self.elemento_atual = None
        self.janela_esta = self.status_janela()
        self.interface = interface
        self.caminho_prints = None

    # verifica qual o nível de confiaça necessária para localizar um determinado elemento #
    def get_conf(self, img=None):
        elemento = img
        if elemento is None:
            elemento = self.elemento_atual 
        if elemento is None:
            print('Nenhum elemento foi atribuido')

        conf = 1
        cords = pag.locateCenterOnScreen(elemento, confidence=conf)
        while cords is None:
            if conf == 0:
                return conf
            cords = pag.locateCenterOnScreen(elemento, confidence=conf)
            if cords is None:
                conf = conf - 0.01
            else:
                item = ptl.PurePath(elemento).name
                print(f'Confianca do elemento adquirida: {item} cf: {conf}')
                return conf

    def armazena_Log(self, log, name='log'):
        with open(f'./{name}.txt', 'a') as arquivolog:
            arquivolog.write('\n' + log)

    def print_log(self, txt, error=False):
        txt = datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M-%S: ') + txt
        print(txt)
        self.armazena_Log(txt)
        if error:
            self.armazena_Log(txt, 'log_error')

    # devolve o stado da janela da aplicacao monitorada #
    def status_janela(self):
        window = win32gui.FindWindow(self.classe_processo, self.nome_processo)
        if window:
            tup = win32gui.GetWindowPlacement(window)
            if tup[1] == win32con.SW_SHOWMAXIMIZED:
                print("maximized")
            elif tup[1] == win32con.SW_SHOWMINIMIZED:
                print("minimized")
            elif tup[1] == win32con.SW_SHOWNORMAL:
                print("normal")
        else:
            print("n_loc")

    # abre um programa utilizando o seu local #
    def abrirPrograma(self):
        if self.localPrograma == None:
            print('Nenhum programa foi atribuido')
            return False
        # os.system('"{}"'.format(self.localPrograma))
        os.startfile('"{}"'.format(self.localPrograma))
        return True
    
    # Retorna as cordenadas de uma img selecionada #
    def localizar(self, img=None):
        elemento = img
        if elemento is None:
            elemento = self.elemento_atual  
        return pag.locateOnScreen(elemento, self.conf)

    # Retorna as cordenadas de uma img selecionada dentro de uma regiao especifica #
    def localizar_dentro(self, region_Img, img=None):
        elemento = img
        if elemento is None:
            elemento = self.elemento_atual  
        cords_region = self.localizar(elemento)
        return pag.locateOnScreen(elemento, confidence=self.conf, region=cords_region)

    # Espera na tela ate o elemento aparecer #
    def espera_na_tela(self, img=None, timeout=60.0):
        elemento = img
        if elemento is None:
            elemento = self.elemento_atual  
        tt = 0
        retorno = None
        while retorno is None and tt < timeout:
            retorno = self.localizar(elemento)
            time.sleep(0.5)
            tt += 0.5
        if retorno is None:
            print(f'Elemento nao localizado:{elemento}')
        return retorno
    
    # Move para uma cordenada de um elemento passado ou pre setado #
    def move_para(self, img=None):
        elemento = img
        if elemento is None:
            elemento = self.elemento_atual  
        coords = self.localizar(elemento)
        pag.moveTo(pag.center(coords))

    # procura e clica em uma cordenada de um elemento em img passado ou pre setado #
    def clicar_em(self, img=None):
        elemento = img
        if elemento is None:
            elemento = self.elemento_atual        
        coords = pag.center(self.localizar(elemento))
        self.click(coords)
        
    def click(self, coords):
        coords = pag.center(coords)
        pag.click(coords.x, coords.y,
            button=self.interface.mouse['botao'],
            clicks=self.interface.mouse['cliques'])
        
    def clicar_por_dentro(self, regiao, img):
        elemento = bot.localizar_dentro(regiao, img)
        bot.click(elemento)
    
    def esperar_clicar(self, img, tt=10):
        elemento = bot.espera_na_tela(img, tt)
        bot.click(elemento)

    # escreve um determinado texto #
    def escrever(self, texto=None):
        if texto is None:
            print('Nenhum texto foi atribuido')
        else:
            pag.write(texto, interval=self.interface.keybo['intervalo'])

    # clica em uma determinada tecla por uma determinada quantidade de vezes #
    def tecla(self, tecla=None):
        if tecla is None: # verifica se uma tecla foi atribuida
            print('Nenhuma tecla foi atribuida')
        else:
            pag.press(tecla, self.interface.keybo['apentar'])
    
    # tira um printscreen da tela e salva com texto especifico #
    def tira_ss(self, nome='noName', 
                local=__import__('os').getcwd() + "\\prints\\", 
                extensao='.png'
                ):
        pag.screenshot(local + nome + extensao)