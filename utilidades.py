import requests
import os

def download_arquivo(url: str, nome: str):
    try:
        response = requests.get(url, timeout=60)
        http_status = response.status_code
        if http_status == 200:
            current_path = os.getcwd()
            file_path = current_path + '/' + nome
            try: 
                with open(file_path, "wb") as file:
                    file.write(response.content)
            except Exception as ex: 
                print(f'Erro ao salvar o arquivo {nome}: {str(ex)}')
            print(f"Download do {nome} concluído com sucesso!")
    except Exception as ex:
        print(f'Erro no download: {str(ex)}')

def executa_comando(comando: str):
    try:
        os.system(comando)
    except Exception as ex:
        print(f"Erro: {ex}")

def testa_extensao_java(arquivo: str):
    checa_extensao = '.java' in arquivo
    return checa_extensao

def clona_repositorio(my_repositorio: str):
    try:
        print(f'Clona repositório {my_repositorio}')
        comando = f'git clone {my_repositorio}'
        os.system(comando)
        print('Repositorio clonado com sucesso!')
    except Exception as ex:
        print(f'Erro na clonagem do repositorio {my_repositorio}: {str(ex)}')

def carrega_dependencias():
    print("Teste de análise de repositorios")
    print('Faz o dowload das dependências...')

    url1='https://raw.githubusercontent.com/mining-software-repositories/pilot3/main/requirements.txt'
    nome1='requirements.txt'
    url2='https://raw.githubusercontent.com/mining-software-repositories/pilot3/main/dao.py'
    nome2='dao.py'
    url3='https://raw.githubusercontent.com/mining-software-repositories/pilot3/main/utils.py'
    nome3='utils.py'

    download_arquivo(url=url1, nome=nome1)
    download_arquivo(url=url2, nome=nome2)
    download_arquivo(url=url3, nome=nome3)

    executa_comando(comando='pip3 install -r requirements.txt')
    print('Dependências instaladas com sucesso!')
