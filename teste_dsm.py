import gera_dsm
from git import Repo
import datetime

repo_url = "https://github.com/apache/cassandra.git"
repo_folder = "cassandra"
folder_to_analyse = "cassandra/src/java"
dsm_filename = "dsm_cassandra.txt"

try:
    print(f'Clona o repositório {repo_url}')
    t1 = datetime.datetime.now()
    repo = Repo.clone_from(repo_url, repo_folder)
    t2 = datetime.datetime.now()
    print(f'Clonagem realizada com sucesso! - Tempo: {t2-t1}s')
except Exception as ex: 
    print(f'Erro ao clonar o repositório {repo_url}.')

try:
    print(f'Analisando os arquivos .java do repositório {repo_url}') 
    t1 = datetime.datetime.now()
    analyzer = gera_dsm.JavaFileAnalyzer(folder_to_analyse, dsm_filename)
    analyzer.find_java_files()
    print('Analisa dependências...')
    analyzer.analyze_dependencies()
    print('Gera DMS')
    analyzer.generate_dsm()
    t2 = datetime.datetime.now()
    print(f'Análise e DMS gerada com sucesso! Tempo: {t2-t1}s')
except Exception as ex:
    print(f'Erro ao analisar e gerar a DSM do repositorio {repo_url}')