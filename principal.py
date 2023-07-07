import dependencias
import extracao

def carrega_dependencias():
    print("Teste de análise de repositorios")
    print('Faz o dowload das dependências...')

    url1='https://raw.githubusercontent.com/mining-software-repositories/pilot3/main/requirements.txt'
    nome1='requirements.txt'
    url2='https://raw.githubusercontent.com/mining-software-repositories/pilot3/main/dao.py'
    nome2='dao.py'
    url3='https://raw.githubusercontent.com/mining-software-repositories/pilot3/main/utils.py'
    nome3='utils.py'

    dependencias.download_arquivo(url=url1, nome=nome1)
    dependencias.download_arquivo(url=url2, nome=nome2)
    dependencias.download_arquivo(url=url3, nome=nome3)

    dependencias.executa_comando(comando='pip3 install -r requirements.txt')
    print('Dependências instaladas com sucesso!')

# extrai informacoes de commits e arquivos modificados em cada commmit
def extrai_informacoes():
    extracao.extrai_informacoes_repositorio(my_repositorio='https://github.com/armandossrecife/promocity.git')

