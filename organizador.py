# encoding: utf-8

import os
import sys
import hashlib
from delphivcl import *

class FileOrganizer(Form):
    # Organizador de arquivo. A intenção é organizar apenas a pasta Downloads, de Windows ou Linux,
    # mas pode ser usado para organizar qualquer pasta.
    # O Script varre a pasta definida em download_folder e começa a fazer distinção pela extensão do
    # arquivo, movendo o arquivo para sua determinada pasta dentro da pasta Downloads, ex:
    # o arquivo C:\Users\username\Downloads\file.jpg será movido para
    # C:\Users\username\Downloads\Imagens\file.jpg
    # O arquivo terá seu hash calculado para evitar enviar dois arquivos iguais para a pasta, mesmo
    # que seus nomes sejam diferentes. Neste caso, o arquivo com hash igual ao já enviado será
    # excluído.

    def __init__(self, owner):
        self.WindowState = "wsNormal"
        self.Width = 1050
        self.Heigh = 400
        self.Position = "poMainFormCenter"
        self.__sm = StyleManager()
        self.__sm.LoadFromFile("styles\\Windows10SlateGray.vsf")
        self.__sm.SetStyle(self.__sm.StyleNames[1])
        self.onClose = self.formOnClose
        self.BorderStyle = "bsSingle"
        self.defaultMargin = 2

        self.painelSuperior(self)
        self.painelDireita(self)
        self.painelEsquerda(self)
        # self.botaoSelectDir(self)
        self.botaoExecutar(self)
        self.fileList(self)

        if sys.platform.startswith("win"):
            self.drive = os.getenv('SystemDrive')
            self.home = os.getenv('USERPROFILE')

        self.download_folder = self.home + '\Downloads'
        self.Caption = "    Organizador de Arquivos: " + self.download_folder

        # self.pastas é a variável pela qual eu vou saber se não estou fazendo uma recursividade exagerada.
        self.pastas = ['PDF', 'Imagens', 'ZIP', 'Office_LibreOffice', 'Instaladores', 'Scripts', 'MP3', 'Videos']

        self.file_hash = []  # Guardará o hash dos arquivos.
        '''
        Extensões de arquivos para organizar.
        Esta tupla contém como "Key" os nomes das pastas onde os arquivos serão realocados
        e como "Value" a extensão do arquivo. 
        '''
        self.extensoes = {
            'PDF':['pdf'],
            'Imagens':['jpg', 'jpeg', 'bmp', 'gif', 'png', 'xcf', 'webp', 'svg', 'ico'],
            'ZIP':['zip', 'gz', 'tar'],
            'Office_LibreOffice':['drawio', 'xls', 'xlsx', 'doc', 'docx', 'ods', 'odt', 'ppt', 'pptx', 'csv', 'pps', 'vss', 'met', 'odp', 'html'],
            'Instaladores':['exe', 'msi', 'msu'],
            'Scripts':['txt', 'sql', 'json', 'dsn', 'log', 'jar'],
            'MP3':['mp3'],
            'Videos':['mp4', 'mov', 'srt', 'wav', 'avi', 'rmvb', '3gp'],
        }

    def formOnClose(self, Sender, action):
        action.Value = caFree

    def painelSuperior(self, sender):
        self.ps = Panel(self)
        self.ps.Margins.Top = self.defaultMargin
        self.ps.Margins.Left = self.defaultMargin
        self.ps.Margins.Right = self.defaultMargin

        self.ps.AlignWithMargins = True
        self.ps.Align = "alTop"
        self.ps.Height = 35
        self.ps.SetProps(Parent=sender)

    def painelDireita(self, sender):
        self.pd = Panel(self)
        self.pd.Margins.Top = self.defaultMargin
        self.pd.Margins.Left = self.defaultMargin
        self.pd.Margins.Right = self.defaultMargin

        self.pd.AlignWithMargins = True
        self.pd.Align = "alRight"
        self.pd.Width = 150
        self.pd.SetProps(Parent=sender)

    def painelEsquerda(self, sender):
        self.pe = Panel(self)
        self.pe.Margins.Top = self.defaultMargin
        self.pe.Margins.Left = self.defaultMargin
        self.pe.Margins.Right = self.defaultMargin

        self.pe.AlignWithMargins = True
        self.pe.Align = "alClient"
        self.pe.SetProps(Parent=sender)

    def botaoSelectDir(self, sender):
        self.bntSelecao = BitBtn(self)
        self.bntSelecao.SetProps(Parent=self.ps)
        self.bntSelecao.Align = "alRight"
        self.bntSelecao.Width = 120
        self.bntSelecao.Caption = "Selecionar Pasta"
        self.bntSelecao.AlignWithMargins = True

        self.oDialog = FileOpenDialog(self)
        self.oDialog.InitialDir = self.download_folder
        self.oDialog.SetProps(Parent=self.ps)

    def botaoExecutar(self, sender):
        self.bntExecutar = BitBtn(self)
        self.bntExecutar.SetProps(Parent=self.pd)
        self.bntExecutar.Align = "alTop"
        self.bntExecutar.Width = 120
        self.bntExecutar.Caption = "Executar"
        self.bntExecutar.AlignWithMargins = True
        self.bntExecutar.Kind = "bkOK"
        self.bntExecutar.OnClick = self.Simbora

    def fileList(self, sender):
        # self.lv = Memo(self)
        # self.lv.SetProps(Parent=self.pe)
        # self.lv.ReadOnly = True
        # self.lv.ScrollBars = 'ssVertical'
        # self.lv.Align = "alClient"
        # self.lv.AlignWithMargins = True

        self.i = Image(self)
        self.i.Align = "alClient"
        self.i.SetProps(Parent=self.pe)
        # #https://www.youtube.com / watch?v = HBzEVgAqBs8
        self.i.Picture.LoadFromFile("https://img.youtube.com/vi/HBzEVgAqBs8/0.jpg")




    def Simbora(self, sender):
        self.lv.Clear()
        self.organizar(self.download_folder)
        ShowMessage("Pasta [ {} ] organizada!".format(self.download_folder))

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
                    extensao = arquivo.split('.')[-1]
                    extensao = extensao.lower()

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
            self.lv.Lines.Add('[MOV] - Arquivo {} MOVIDO para {}'.format(origem, destino))

            os.rename(origem, destino)
        else:
            os.remove(origem)
            print('Arquivo {} removido por duplicidade'.format(origem))
            self.lv.Lines.Add('[DEL] - Arquivo {} EXCLUÍDO por duplicidade'.format(origem))

        self.lv.Update()
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




def main():
    Application.Initialize()
    Application.Icon.LoadFromFile("C:\\Users\\ednoj\\Pictures\\Icones\\icons8-web-analystics-100.ico")
    Main = FileOrganizer(Application)
    Application.Title = Main.Caption
    Main.Show()
    FreeConsole()
    Application.Run()
    Main.Destroy()

if __name__ == '__main__':
    main()


#a = FileOrganizer()
#a.download_folder = 'C:\\Users\\Torres\\Downloads'
#a.organizar(a.download_folder)
