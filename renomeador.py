# encoding: utf-8

import os
import random

pasta = 'E:\Imagens\\burst'

arquivos = os.listdir(pasta)

for arquivo in arquivos:
    # Começar com arquivos que começam com WP
    # if arquivo.startswith('IMG-'):
    #     novo_nome = arquivo[4:8] + '.' + arquivo[8:10] + '.' + arquivo[10:12] + '_' + arquivo[16:]
    #     os.rename(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome)
    #     print('{} agora é {}'.format(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome))

    # if arquivo.startswith('2015'):
    #     novo_nome = arquivo[0:4] + '.' + arquivo[4:6] + '.' + arquivo[6:8] + '_' + arquivo[-10:]
    #     os.rename(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome)
    #     print('{} agora é {}'.format(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome))

    # if arquivo.find('.2017.') > -1:
    #     pass
    #     print(arquivo)
    #     novo_nome = arquivo[3:]
    #     os.rename(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome)
    #     print(novo_nome)

    #print(arquivo[4:8])
    # if arquivo[4:8] == '2018':
    #     print(arquivo)
    #     novo_nome = arquivo[4:8] + '.' + arquivo[0:2] + '.' + arquivo[2:4] + '_' + arquivo[7:]
    #     #os.rename(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome)
    #     print(novo_nome)
    #     print('{} agora é {}'.format(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome))

    # if arquivo.startswith('.'):
    #     pass
    #     print(arquivo)
    #     novo_nome = arquivo[1:]
    #     #os.rename(pasta +'\\'+ arquivo, pasta + '\\(1)' + novo_nome)
    #     print(novo_nome)
    #
     if arquivo.startswith('IMG_'):
        if len(arquivo) > 12:
           if arquivo.find('BURST') > -1:
               novo_nome = arquivo[4:8] + '.' + arquivo[8:10] + '.' + arquivo[10:12] + arquivo[12:22] + arquivo[22:23] + arquivo[28:31] + arquivo[-4:]
           else:
               novo_nome = arquivo[4:8] + '.' + arquivo[8:10] + '.' + arquivo[10:12] + arquivo[12:22] + arquivo[-3:]

           os.rename(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome)
           print('{} agora é {}'.format(pasta +'\\'+ arquivo, pasta + '\\' + novo_nome))
