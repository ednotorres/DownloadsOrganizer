# encoding: utf-8

import os
import hashlib


class Desduplicar():
    lista = []
    item = 0
    pasta_destino = ''
    '''
        Esta classe visa varrer todos os aruqivos de uma determinada pasta e suas sub-pastas
        em busca de arquivos duplicados.
        Caso os encontre, cocolca-os em uma pasta chamada duplicados para remoção manual.
    '''

    def varrer_pastas(self, pasta):
        fqdn = ''

        try:
            arquivos = os.listdir(pasta)

            for arquivo in arquivos:
                self.item = self.item + 1
                hashMD5 = ''
                fqdn = pasta + '\\' + arquivo
                if arquivo != 'Arquivo Morto':
                    if os.path.isdir(fqdn):
                        self.item = self.item - 1
                        self.varrer_pastas(fqdn)
                    elif os.path.isfile(fqdn):
                        hashMD5 = self.get_md5(fqdn)
                        print('#{}\t{}\n{}'.format(self.item, hashMD5, fqdn))
                        if hashMD5 in self.lista:
                            os.rename(fqdn, self.pasta_destino+arquivo)
                            print('#'*50)
                            print('#{}\t {} duplicado'.format(self.item, fqdn))
                            print('#' * 50)
                        else:
                            self.lista.append(hashMD5)

        except Exception as e:
            print('#' * 50)
            print('Erro: {}'.format(e))
            print('#' * 50)
            self.item = self.item - 1





    def get_md5(self, file_name):
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

a = Desduplicar()
a.pasta_destino = 'z:\\Arquivo Morto\\duplicados\\'
a.varrer_pastas('z:')
