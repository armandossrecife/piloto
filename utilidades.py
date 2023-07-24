import requests
import os
import json
import pandas as pd
import subprocess

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

def create_folder(folder_path):
    '''
    # Usage example
    folder_path = "/path/to/folder"
    create_folder(folder_path)
    '''
    try: 
        # Check if folder exists
        if os.path.exists(folder_path):
            # Remove folder if it exists
            os.rmdir(folder_path)

        # Create the folder
        os.makedirs(folder_path)
    except Exception as ex:
        print(f'Erro ao criar a pasta {folder_path}: {str(ex)}')

def export_csv_from_dict(data_dict, file_path):
    try:
        df = pd.DataFrame.from_dict(data_dict)
        df.to_csv(file_path, index=False)
    except Exception as ex:
        print(f'Erro ao gerar o .csv {file_path}: {str(ex)}')

def export_txt_from_list(lista, file_path):
    try:
        with open(file_path, mode='w') as f_temp:
            for each in lista:
                each = each + '\n'
                f_temp.write(each)
    except Exception as ex:
        print(f'Erro ao gerar o arquivo .txt {file_path} : {str(ex)}')

# Retorna um dicionario onde a chave eh um commit e o valor eh uma lista com os arquivos modificados desse commit em uma lista
def dictionary_commits_from_tags_A_B(diretorio_repositorio, tag_a, tag_b):
    os.chdir(diretorio_repositorio)
    faixa = tag_a + '..' + tag_b
    cmd1 = ["git", "log", "--format='%H'", faixa]
    output1 = subprocess.check_output(cmd1).decode("utf-8")
    commits = output1.splitlines()
    dictionary_commits = {}
    # Analisar os arquivos modificados em cada commit
    for commit in commits:
        commit = commit.replace("'", "")
        cmd2 = ["git", "diff","--name-only",commit]
        output2 = subprocess.check_output(cmd2).decode("utf-8")
        output2 = output2.split('\n')
        dictionary_commits[commit] = output2
    return dictionary_commits
