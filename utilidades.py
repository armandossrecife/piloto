import requests
import os
import json

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
    print('Carrega dependências do projeto...')
    executa_comando(comando='pip3 install -r requirements.txt')
    print('Dependências instaladas com sucesso!')

def convert_list_to_str(lista):
    temp = ''
    if len(lista) > 0:
        temp = ','.join( str(v) for v in lista)
    return temp

def convert_modifield_list_to_str(lista):
    list_aux = []
    for each in lista:
        list_aux.append(each.filename)
    str = convert_list_to_str(list_aux)
    return str

def convert_dictionary_to_str(dictionary):
    temp = ''
    if len(dictionary) > 0:
        temp = str(json.dumps(dictionary))
    return temp
