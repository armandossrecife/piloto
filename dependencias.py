## todo: iteritems is deprecated and will be removed in a future version. Use .items instead.
import requests
import os

def download_arquivo(url, nome):
    try:
        response = requests.get(url)
        http_status = response.status_code
        if http_status == 200:
            current_path = os.getcwd()
            file_path = current_path + '/' + nome
            try: 
                with open(file_path, "wb") as file:
                    file.write(response.content)
            except Exception as ex: 
                print(f'Erro ao salvar o arquivo: {str(ex)}')
            print(f"Download do {nome} concluído com sucesso!")
    except Exception as ex:
        print(f'Erro no download: {str(ex)}')

def executa_comando(comando):
    try:
        os.system(comando)
    except Exception as ex:
        print(f"Erro: {ex}")