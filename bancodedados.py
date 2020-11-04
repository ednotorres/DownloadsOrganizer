# encoding: utf-8

import os
import hashlib
import mysql.connector
from time import sleep

def fileMD5(file_name):
    md5_hash = hashlib.md5()
    a_file = open(file_name, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='organizar')

cursor = cnx.cursor()

pasta = 'E:\\Imagens'
pasta_mysql = 'E:\\\\Imagens'

arquivos = os.listdir(pasta)
id = ''
contador = 1
repetidos = 0

for arquivo in arquivos:
    file_name = pasta+'\\'+arquivo
    if os.path.isfile(file_name):
        file_name_mysql = pasta+'\\\\'+arquivo
        id = fileMD5(file_name)
        print('Procurando o MD5 {} no banco de dados. Arquivo: {}'.format(id, file_name))
        cursor.execute('SELECT * from fotos where md5="'+id+'"')
        linhas = cursor.fetchone()
        sleep(0.2)
        if linhas == None:
            cursor.execute('INSERT INTO fotos (md5, nome) VALUES("{}", "{}")'.format(id, file_name_mysql))
            cnx.commit()
        else:
            arquivo_duplicado = linhas[1]
            try:
                cursor.execute('INSERT INTO repetidas (md5, nome_original, nome_duplicada) VALUES("{}", "{}", "{}")'.format(id, arquivo_duplicado, file_name_mysql))
                cnx.commit()
                print('Foto repetida. Movendo arquivo {} para a pasta REPETIDOS.'.format(file_name))
                if not os.path.exists(pasta + '\REPETIDOS'):
                    os.mkdir(pasta + '\REPETIDOS')
                os.rename(pasta + '\\' + arquivo, pasta + '\REPETIDOS' + '\\' + arquivo)
                repetidos = repetidos + 1
            except:
                print('Erro ao tentar inserir os dados da foto em "duplicados".')

    print('{} itens verificados. {} itens repetidos.'.format(contador, repetidos))
    contador = contador + 1


cnx.close()