# encoding: utf-8

import os
import hashlib

class FileOrganizer():
    # Organizador de arquivo. A intenção é organizar apenas a pasta Downloads, de Windows ou Linux,
    # mas pode ser usado para organizar qualquer pasta.
    # O Script varre a pasta definida em download_folder e começa a fazer distinção pela extensão do
    # arquivo, movendo o arquivo para sua determinada pasta dentro da pasta Downloads, ex:
    # o arquivo C:\Users\username\Downloads\file.jpg será movido para
    # C:\Users\username\Downloads\Imagens\file.jpg
    # O arquivo terá seu hash calculado para evitar enviar dois arquivos iguais para a pasta, mesmo
    # que seus nomes sejam diferentes. Neste caso, o arquivo com hash igual ao já enviado será
    # excluído.

    def __init__(self):
        self.drive = os.getenv('HOMEDRIVE')
        self.home = os.getenv('HOMEPATH')
        self.download_folder = self.drive + self.home + '\Downloads'
        #self.download_folder = 'H:\\8M'

        # self.pastas é a variável pela qual eu vou saber se não estou fazendo uma recursividade exagerada.
        self.pastas = ['PDF', 'Imagens', 'ZIP', 'Office_LibreOffice', 'Instaladores', 'Scripts', 'MP3', 'Videos']

        self.file_hash = []  # Guardará o hash dos arquivos.

        '''
        Extensões de arquivos para organizar.
        Esta tupla contém como "Key" os nomes das pastas onde os arquivos serão realocados
        e como "Value" a extensão do arquivo. 
        '''
        self.extensoes = {
            'PDF':['.pdf', '.PDF'],
            'Imagens':['.jpg', '.JPG', 'jpeg', 'JPEG', '.jpg', '.JPG', '.bmp', '.BMP', '.gif', '.GIF', '.png', '.PNG', '.xcf', '.XCF'],
            'ZIP':['.zip', '.ZIP'],
            'Office_LibreOffice':['.xls', '.XLS', 'xlsx', 'XLSX', '.doc', '.DOC', 'docx', 'DOCX', '.ods', '.ODS', '.odt', '.ODT', '.ppt', '.PPT', 'pptx', 'PPTX', '.csv', '.CSV', '.pps', '.PPS', '.vss', '.VSS', '.met', '.MET', '.odp', '.ODP'],
            'Instaladores':['.exe', '.EXE', '.msi', '.MSI'],
            'Scripts':['.txt', '.TXT', '.sql', '.SQL', 'json', 'JSON', '.dsn', '.DNS', '.log', '.LOG'],
            'MP3':['.mp3', '.MP3'],
            'Videos':['.mp4', '.MP4', '.mov', '.MOV', '.srt', '.SRT', '.wav', '.WAV', '.avi', '.AVI', 'rmvb', 'RMVB', '.3gp', '.3GP'],
        }

    def fileMD5(self, file_name):
        '''
        Faz o cálculo do Hash MD5 do arquivo definido em file_name

        :return: string
        '''

        md5_hash = hashlib.md5()
        a_file = open(file_name, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        a_file.close()

        return digest

    def organizar(self, source_folder):
        '''
        Executa o processo de organização de uma determinada pasta.
        Este processo faz uma busca recursiva na pasta source_folder e suas subpastas.

        :param destination_folder: string
        :param files_extension: string
        :return: None
        '''
        try:
            arquivos = os.listdir(source_folder)

            for arquivo in arquivos:
                fqdn = source_folder + '\\' + arquivo
                fqdn_move = ''

                if os.path.isdir(fqdn):
                    '''
                    Em o local sendo uma pasta, há que se verificar se a pasta não é uma das
                    pastas de destino. Caso seja, ignorar a pasta. Caso contrário, fazer a 
                    busca recursiva.
                    '''
                    if arquivo not in self.pastas:
                        self.organizar(fqdn)
                else:
                    '''
                    Este bloco é acessado quando o objeto na pasta fqdn é um arquivo.
                    Nesse caso, a extensão do arquivo será verificada e, caso ela seja
                    encontrada, o arquivo será movido para a pasta à qual ele está 
                    relacionado, ex: foto1.jpg será enviada para ../Downloads/Imagens
                    '''
                    extensao = arquivo[-4:]

                    for extensao_arquivo in self.extensoes:
                        '''
                        Caso a pasta não tenha sido criada, o script criará a pasta.
                        '''
                        if not os.path.exists(self.download_folder + '\\' + extensao_arquivo):
                            os.mkdir(self.download_folder + '\\' + extensao_arquivo)

                        if extensao in self.extensoes[extensao_arquivo]:
                            fqdn_move = self.download_folder+'\\'+extensao_arquivo+'\\'+arquivo
                            self.mover_arquivo(fqdn, fqdn_move)

                            break  # para sair do loop, pois não tem mais necessidade de varrer o vetor,
                            # uma vez que já sabemos qual a extensão do arquivo e que também o arquivo foi
                            # movido para a pasta de destino.
        except Exception as e:
            print('Erro: {}'.format(e))

    def mover_arquivo(self, origem, destino):
        '''
        Move um arquivo da origem para o destino. Antes de mover, verifica se há algum
        arquivo com o mesmo nome. Além disso, ao mover, insere o hash do arquivo em uma
        lista para verificação. Caso o arquivo a ser movido já exista na lista, isso quer
        dizer que o arquivo existe duas vezes e que não há necessidade de movê-lo novamente,
        pois o hash igual significa que o arquivo origem é exatamente igual ao arquivo destino,
        mesmo que tenha nomes diferentes.

        :param origem: string
        :param destino: string
        :return: boolean
        '''

        hash = self.fileMD5(origem)

        '''
        Primeira parte: verificar se o hash é idêntico.
        Caso seja, remove o arquivo.
        '''
        if hash not in self.file_hash:
            self.file_hash.append(hash)
            if os.path.exists(destino):
                '''
                Aqui os arquivos tem o mesmo nome, mas não tem o mesmo hash, o que significa
                que são totalmente diferentes. Nesse caso, é necessário renomear.
                '''
                destino = self.renomear_destino(destino)

            print('Arquivo {} movido para {}'.format(origem, destino))
            os.rename(origem, destino)
            return True
        else:
            os.remove(origem)
            print('Arquivo {} removido por duplicidade'.format(origem))
            return True

    def renomear_destino(self, destino):
        prenome = ''
        extensao = ''
        arquivo = ''

        fqdn = destino.split('\\')
        file_name = fqdn[-1:]
        file_name = ''.join(file_name)

        arquivo = file_name

        if arquivo[-4:-3] == '.':
            prenome = arquivo[:-4]
            extensao = arquivo[-4:]

        elif arquivo[-5:-4] == '.':
            prenome = arquivo[:-5]
            extensao = arquivo[-5:]

        from random import randint
        randomizado = randint(1000, 5000)
        randomizado = str(randomizado).zfill(4)

        arquivo = prenome + '_' + randomizado + '_' + extensao

        fqdn[len(fqdn)-1] = arquivo

        fqdn = '\\'.join(fqdn)

        return fqdn

a = FileOrganizer()
a.organizar(a.download_folder)
