from __init__ import badbot
from time import sleep as slp

bot = badbot()

bot.localPrograma = 'C:\\WINDOWS\\system32\\notepad.exe'
bot.abrirPrograma()
slp(0.5)
bot.interface.keybo['intervalo'] = 0.025
bot.escrever('Ola eu sou o badbot, vou te ajudar a fazer seu trampo mais rapido!!!')
bot.interface.keybo['apertar'] = 3
bot.tecla('enter')
slp(0.5)
bot.interface.keybo['apertar'] = 1
bot.escrever('Olha que legal quantas coisas da pra fazer!')
slp(0.5)
bot.clicar_em('win_btn.PNG')
slp(0.5)
bot.clicar_em('win_btn.PNG')
slp(0.5)
print('Acabou!')