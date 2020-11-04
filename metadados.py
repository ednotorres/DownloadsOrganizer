# encoding: utf-8

import os
import time
from stat import * # ST_SIZE etc


pasta = 'E:\\Imagens'

arquivos = os.listdir(pasta)
meses = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

for arquivo in arquivos:
    file_name = pasta + '\\' + arquivo
    extensao = file_name.lower()
    if os.path.isfile(file_name):
        atributos = os.stat(file_name)

        modificado = time.asctime(time.localtime(atributos[ST_MTIME]))
        modificado = modificado.split(' ')

        if len(modificado) == 6:
            mes = meses[modificado[1]]
            dia = modificado[3]
            hora = modificado[4]
            ano = modificado[5]
        else:
            mes = meses[modificado[1]]
            dia = modificado[2]
            hora = modificado[3]
            ano = modificado[4]

        # print('----------------------------')
        # print(modificado)
        #print('{}: {}/{}/{} - {} + {}'.format(file_name, ano, mes, dia, hora, arquivo[-8:-4]))
        # print('----------------------------')

        hora = ''.join(hora.split(':'))

        if extensao.endswith('.jpg'):
            extensao = extensao[-3:]
        else:
            extensao = extensao[-4:]

        nome_arquivo = '{}_{}_{}_{}{}.{}'.format(ano, mes, dia, hora, arquivo[-8:-4], extensao)

        novo_nome = pasta + '\\' + nome_arquivo


        #print('de \t{} \tpara \t{}'.format(file_name, novo_nome))

        try:
            os.rename(file_name, novo_nome)
        except:
            pass
#        print('Foto tirada em {}/{}/{} às {}'.format(dia, mes, ano, hora))
#        print('Nome do arquivo:{}_{}_{}_{}'.format(ano, mes, dia, hora))




# a = os.stat('E:\\Imagens\\001 (2).jpg')
#
# acessado = time.asctime(time.localtime(a[ST_ATIME]))
# modificado = time.asctime(time.localtime(a[ST_MTIME]))
# alterado = time.asctime(time.localtime(a[ST_CTIME]))
#
# modificado = modificado.split(' ')
# #print(modificado)
#
# mes = meses[modificado[1]]
# dia = modificado[2]
# hora = modificado[3]
# hora = ''.join(hora.split(':'))
# ano = modificado[4]
#
# if 'E:\\Imagens\\rel_antes_1.jpeg'.endswith('.jpeg'):
#     extensao = 'E:\\Imagens\\rel_antes_1.jpeg'[-4:]
# else:
#     extensao = 'E:\\Imagens\\rel_antes_1.jpeg'[-3:]
#
#
# nome_arquivo = '{}_{}_{}_{}.{}'.format(ano, mes, dia, hora, extensao)
# print('Foto tirada em {}/{}/{} às {}'.format(dia, mes, ano, hora))
# #print('Nome do arquivo:{}_{}_{}_{}'.format(ano, mes, dia, hora))
# print(nome_arquivo)
# print('')
#
# print(acessado)
# print(modificado)
# print(alterado)