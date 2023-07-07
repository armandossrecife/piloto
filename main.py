## todo: iteritems is deprecated and will be removed in a future version. Use .items instead.
import requests
import os

def download_arquivo(url, nome):
  response = requests.get(url)
  if response.status_code == 200:
    current_path = os.getcwd()
    file_path = current_path + '/' + nome
    with open(file_path, "wb") as file:
      file.write(response.content)
    print(f"Download do {nome} concluído com sucesso!")

def executa_comando(comando):
  try:
    os.system(comando)
  except Exception as ex:
    print(f"Erro: {ex}")

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

import os
import dao
import pydriller
import utils
import datetime

def testa_extensao_java(arquivo):
    if '.java' in arquivo:
        return True
    else:
        return False 

def clona_repositorio(my_repositorio):
    try:
        print('Clona repositório promocity')
        comando = f'git clone {my_repositorio}'
        os.system(comando)
        print('Repositorio clonado com sucesso!')
    except Exception as ex:
        print(f'Erro na clonagem do repositorio {my_repositorio}: {str(ex)}')

clona_repositorio(my_repositorio='https://github.com/armandossrecife/promocity.git')

print('Cria a sessão de banco de dados')
db_session = dao.create_session()
print('Cria as tabelas do banco')
dao.create_tables()
print('Tabelas criadas com sucesso!')

# Cria a colecao de CommitsComplete
myCommitsCompleteCollection = dao.CommitsCompleteCollection(db_session)
# Cria a colecao de FilesComplete
myFilesCompleteCollection = dao.FilesCompleteCollection(db_session)

qtd_commits = 0

tempo1 = datetime.datetime.now()
print('Analisa commits e arquivos modificados. Aguarde...')
for commit in pydriller.Repository('promocity').traverse_commits():
    try:
        currentCommit = dao.CommitComplete(
        name='promocity' + '_' + commit.hash,
        hash=commit.hash,
        msg=commit.msg,
        author=commit.author.name,
        committer=commit.committer.email,
        author_date=commit.author_date,
        author_timezone=commit.author_timezone,
        committer_date=commit.committer_date,
        committer_timezone=commit.committer_timezone,
        branches=utils.convert_list_to_str(commit.branches),
        in_main_branch=commit.in_main_branch,
        merge=commit.merge,
        modified_files=utils.convert_modifield_list_to_str(commit.modified_files),
        parents=utils.convert_list_to_str(commit.parents),
        project_name=commit.project_name,
        project_path=commit.project_path,
        deletions=commit.deletions,
        insertions=commit.insertions,
        lines=commit.lines,
        files=commit.files,
        dmm_unit_size=commit.dmm_unit_size,
        dmm_unit_complexity=commit.dmm_unit_complexity,
        dmm_unit_interfacing=commit.dmm_unit_interfacing)
        # salva dados do commit na tabela de commits do banco do repositorio
        myCommitsCompleteCollection.insert_commit(currentCommit)
        qtd_commits = qtd_commits + 1
        # analisa cada um dos arquivos modificados no commit
        for file in commit.modified_files:
            try:
                if file is not None and file.filename is not None:
                    currentFile = dao.FileComplete(
                                    name=file.filename,
                                    hash=commit.hash,
                                    old_path=file.old_path,
                                    new_path=file.new_path,
                                    filename=file.filename,
                                    is_java=testa_extensao_java(file.filename),
                                    change_type=file.change_type.name,
                                    diff=str(file.diff),
                                    diff_parsed=utils.convert_dictionary_to_str(file.diff_parsed),
                                    added_lines=file.added_lines,
                                    deleted_lines=file.deleted_lines,
                                    source_code=str(file.source_code),
                                    source_code_before=str(file.source_code_before),
                                    methods=utils.convert_list_to_str(file.methods),
                                    methods_before=utils.convert_list_to_str(file.methods_before),
                                    changed_methods=utils.convert_list_to_str(file.changed_methods),
                                    nloc=file.nloc,
                                    complexity=file.complexity,
                                    token_count=file.token_count,
                                    commit_id=myCommitsCompleteCollection.query_commit_hash(commit.hash))
                    myFilesCompleteCollection.insert_file(currentFile)
            except Exception as ex:
                print(f'Erro ao inserir arquivo {file.filename} na tabela de files do banco!: {str(ex)}')
    except Exception as ex:
        print(f'Erro ao salvar commit {commit.hash} no banco : {str(ex)}')
db_session.close()
tempo2 = datetime.datetime.now()
print('Sessão de banco de dados fechada!')
print(f'Quantidade de commits analisados: {qtd_commits}')
print(f'Tempo de análise: {tempo2-tempo1}')

# 4.2 Carrega as tabelas do banco em dataframes

import pandas as pd
import sqlite3

DATA_BASE='my_promocity.db'
con = sqlite3.connect(DATA_BASE)

my_query_commits = "select * from commitscomplete"
my_query_files = "select * from filescomplete"
my_query_files_commits = "select f.id as 'file_id', f.hash as 'file_hash_commit', f.description as 'file_description', f.is_java as 'file_is_java', f.created_date as 'file_created_date', f.old_path as 'file_old_path', f.new_path as 'file_new_path', f.filename as 'file_filename', f.change_type as 'file_change_type', f.diff as 'file_diff', f.diff_parsed as 'file_diff_parsed', f.added_lines as 'file_added_lines', f.deleted_lines as 'file_deleted_lines', f.source_code as 'file_source_code', f.source_code_before as 'file_source_code_before', f.nloc as 'file_nloc', f.complexity as 'file_complexity', f.token_count as 'file_token_count', f.commit_id as 'file_commit_id', c.* from filescomplete f, commitscomplete c where f.commit_id=c.id"

df_commits_from_db = pd.read_sql_query(my_query_commits, con)
df_files_from_db = pd.read_sql_query(my_query_files, con)
df_files_commits_from_db = pd.read_sql(my_query_files_commits, con)

con.close() 

# Faz alguns ajustes nos dataframes
df_files_from_db['modified_lines'] = df_files_from_db.added_lines + df_files_from_db.deleted_lines
df_files_commits_from_db['modified_lines'] = df_files_commits_from_db.file_added_lines + df_files_commits_from_db.file_deleted_lines
# Lista os commits e seus arquivos modificados
df_commits_from_db[['name', 'modified_files']]

# procura por um commit especifico
df_commits_from_db[['name', 'modified_files']].query("name == 'promocity_fc85e473f543f543c68110d62624180fc3b24606'")

# Lista todos os arquivos e seus commits
df_files_from_db[['name', 'hash']].sort_values('name')

# Mostra as Complexidades Ciclomáticas dos arquivos
df_files_commits_from_db[['file_filename', 'file_complexity', 'author_date']].sort_values(by=['file_filename', 'author_date'], ascending=True)

# Mostra as complexidades ciclomáticas de um determinado arquivo
df_files_commits_from_db[['file_filename', 'file_complexity', 'author_date']].sort_values(by=['file_filename', 'author_date'], ascending=True).query("file_filename == 'UserController.java'")

try: 
  df_commits_from_db.to_csv('promocity_commits.csv') 
  df_files_from_db.to_csv('promocity_files.csv') 
  df_files_commits_from_db.to_csv('promocity_files_commits.csv') 
except Exception as ex: 
  print(f'Erro ao salvar o arquivos .csv: {str(ex)}')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df_files_from_db[['name','modified_lines']]

# Lista arquivos ordenados por nome com suas linhas modificadas
df_files_from_db[['name','modified_lines']].sort_values(by=['name'], ascending=True)

# Agrupa o df por nome do arquivo
df_groupby_name_modified_lines = df_files_from_db[['name','modified_lines']].groupby('name')

# Soma o total de linhas modificadas de cada arquivo
group_files_modified_lines = df_groupby_name_modified_lines.sum()
group_files_modified_lines

# Cria um novo df de Linhas de Código Modificadas
df_locm = group_files_modified_lines.copy()
df_locm = df_locm.reset_index()
df_locm

# Acrescenta uma coluna File
df_locm['File'] = 'File'
df_boxplot_em = df_locm[['modified_lines', 'File']]

# Boxplot do EM (Esforço de Manutenção de Locs Modificadas). Todos os arquivos do repositório
plt.figure(figsize=(6,4))
sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em)

# Remove os arquivos que não foram modificados ao longo do tempo (O linhas modificadas)
df_boxplot_em = df_boxplot_em.drop(df_boxplot_em[df_boxplot_em.modified_lines == 0].index)

plt.figure(figsize=(6,4))
# Constroi o Boxsplot sem os outliers
sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em,  showfliers=False)

list_of_files_modified_lines = group_files_modified_lines.to_dict()
print(f'{ len(list_of_files_modified_lines) }, {list_of_files_modified_lines}')

# Mostra os quatis 
em_q1 = np.percentile(df_boxplot_em.modified_lines, [25])
em_q2 = np.percentile(df_boxplot_em.modified_lines, [50])
em_q3 = np.percentile(df_boxplot_em.modified_lines, [75])
em_q4 = np.percentile(df_boxplot_em.modified_lines, [100])

print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1}, Q2: {em_q2}, Q3: {em_q3}, Q4: {em_q4}')

# Cria um df sem os arquivos de Teste
df_locm_no_test = df_locm[(df_locm["name"].str.contains('Test') == False)]

# Cria um df contendo apenas os arquivos .java de implementacao
df_locm_java_impl = df_locm_no_test[df_locm_no_test['name'].str.contains('.java', regex=False)]
df_locm_java_impl

df_boxplot_em_java_impl = df_locm_java_impl[['modified_lines', 'File']]

plt.figure(figsize=(6,4))
sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em_java_impl)

# Remove os arquivos que não foram modificados ao longo do tempo (O linhas modificadas)
df_boxplot_em_java_impl = df_boxplot_em_java_impl.drop(df_boxplot_em_java_impl[df_boxplot_em_java_impl.modified_lines == 0].index)

plt.figure(figsize=(6,4))
# Constroi o Boxsplot sem os outliers
sns.boxplot(x='File', y='modified_lines', data=df_boxplot_em_java_impl,  showfliers=False)

# Mostra os quatis 
em_q1_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [25])
em_q2_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [50])
em_q3_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [75])
em_q4_java_impl = np.percentile(df_boxplot_em_java_impl.modified_lines, [100])

print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1_java_impl}, Q2: {em_q2_java_impl}, Q3: {em_q3_java_impl}, Q4: {em_q4_java_impl}')

# Mostra as Complexidades Ciclomáticas dos arquivos ordenada crescent pelo tempo
df_cc = df_files_commits_from_db[['file_filename', 'file_complexity', 'author_date']].sort_values(by=['file_filename', 'author_date'], ascending=True)
df_cc.query("file_filename == 'UserController.java'")

# Remove files that has not cc
# cc all files
df_cc_temp = df_cc.copy()
df_cc_temp = df_cc_temp[df_cc_temp.file_complexity.notnull()]

##### Todos os arquivos #####
# Acrescenta uma coluna File
df_cc_temp['File'] = 'File'
df_boxplot_cc_temp = df_cc_temp[['file_complexity', 'File']]

# Boxplot do CC. Todos os arquivos do repositório
plt.figure(figsize=(6,4))
sns.boxplot(x='File', y='file_complexity', data=df_boxplot_cc_temp)

# Mostra os quatis 
em_q1_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [25])
em_q2_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [50])
em_q3_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [75])
em_q4_cc_temp = np.percentile(df_boxplot_cc_temp.file_complexity, [100])

print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1_cc_temp}, Q2: {em_q2_cc_temp}, Q3: {em_q3_cc_temp}, Q4: {em_q4_cc_temp}')

### Apenas os arquivos .java ###
# Cria um df sem os arquivos de Teste
df_cc_temp_no_test = df_cc_temp[(df_cc_temp["file_filename"].str.contains('Test') == False)]

# Cria um df contendo apenas os arquivos .java de implementacao
df_cc_temp_java_impl = df_cc_temp_no_test[df_cc_temp_no_test['file_filename'].str.contains('.java', regex=False)]

df_cc_temp_boxplot_em_java_impl = df_cc_temp_java_impl[['file_complexity', 'File']]

plt.figure(figsize=(6,4))
sns.boxplot(x='File', y='file_complexity', data=df_cc_temp_boxplot_em_java_impl)

# Mostra os quatis 
em_q1_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [25])
em_q2_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [50])
em_q3_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [75])
em_q4_cc_temp_java_impl = np.percentile(df_cc_temp_boxplot_em_java_impl.file_complexity, [100])

print(f'Quartis do Total de Linhas Modificadas: Q1: {em_q1_cc_temp_java_impl}, Q2: {em_q2_cc_temp_java_impl}, Q3: {em_q3_cc_temp_java_impl}, Q4: {em_q4_cc_temp_java_impl}')

# calcula frequência dos arquivos na faixa de commits analisados
list_of_files_frequency_in_commits = {}

# Dataframe agrupados por arquivos e seus commits
df_groupby_name = df_files_from_db[['name', 'hash']].groupby('name')

print(f'Quantidade de grupos: {df_groupby_name.ngroups}')
print(f'Grupos: {df_groupby_name.groups}')

df_files_from_db[['name', 'hash']].query("name=='.gitignore'")

group_files = df_groupby_name.size()
print(group_files)
print('')
list_of_files_frequency_in_commits = group_files.to_dict()
print(f'{ len(list_of_files_frequency_in_commits) }, {list_of_files_frequency_in_commits}')

# Cria um df contendo o arquivo e sua frequencia de commits
df_fc = pd.DataFrame({'name':group_files.index, 'frequency_commits': group_files.values})

df_boxplot_fc = df_fc
# Acrescenta a coluna File
df_boxplot_fc['File'] = 'File'

# Remove as frequencias muito baixas (total de commits < 10)
df_boxplot_fc = df_boxplot_fc.drop(df_boxplot_fc[df_boxplot_fc.frequency_commits < 10].index)

plt.figure(figsize=(6,4))

sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc)

plt.figure(figsize=(6,4))

# Constroi o Boxsplot sem os outliers
sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc, showfliers=False)

fc_q1 = np.percentile(df_boxplot_fc.frequency_commits , [25])
fc_q2 = np.percentile(df_boxplot_fc.frequency_commits , [50])
fc_q3 = np.percentile(df_boxplot_fc.frequency_commits , [75])
fc_q4 = np.percentile(df_boxplot_fc.frequency_commits , [100])

print(f'Quartis da Frequencia de Commits Q1: {fc_q1}, Q2: {fc_q2}, Q3: {fc_q3}, Q4: {fc_q4}')

# Cria um df sem os arquivos de Teste
df_fc_no_test = df_fc[(df_fc["name"].str.contains('Test') == False)]

# Cria um df contendo apenas os arquivos .java de implementacao
df_fc_java_impl = df_fc_no_test[df_fc_no_test['name'].str.contains('.java', regex=False)]

df_boxplot_fc_java_impl = df_fc_java_impl[['frequency_commits', 'File']]

plt.figure(figsize=(6,4))
sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl)

plt.figure(figsize=(6,4))

# Constroi o Boxsplot sem os outliers
sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl, showfliers=False)

# Remove as frequencias muito baixas (total de commits < 3)
df_boxplot_fc_java_impl2 = df_boxplot_fc_java_impl.drop(df_boxplot_fc_java_impl[df_boxplot_fc_java_impl.frequency_commits < 3].index)

plt.figure(figsize=(6,4))

# Constroi o Boxsplot sem os outliers
sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl2, showfliers=False)

fc_q1_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [25])
fc_q2_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [50])
fc_q3_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [75])
fc_q4_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [100])

print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')

# EM from df_arquivos_mais_locs_modificados -> df_locm
print('LOCM')
df_locm.info()

print('')

print('FC')
# FC from df_arquivos_mais_modificados -> df_fc
df_fc.info()

df_em_fc = df_locm[['name','modified_lines']]
df_em_fc['frequency_commits'] = df_fc['frequency_commits']
df_em_fc

df_fator_multiplicacao = df_em_fc.copy()
df_fator_multiplicacao['factor1'] = df_fator_multiplicacao['modified_lines'] * df_fator_multiplicacao['frequency_commits']
df_fator_multiplicacao

plt.style.use('ggplot')

plt.figure(figsize=(12,8))
sns.scatterplot(data=df_em_fc, x='modified_lines', y='frequency_commits')

abbr={'titulo':'Modificações de LoCs x Frequência de Commits', 'modified_lines':'Modificações de Locs', 'frequency_commits':'Frequência de Commits'}

plt.title(f"Análise do Repositório Promocity : {abbr['modified_lines']} x {abbr['frequency_commits']}")
plt.xlabel(abbr['modified_lines'])
plt.ylabel(abbr['frequency_commits'])
          
for i in range(df_em_fc.shape[0]):
  if df_em_fc.modified_lines[i] > em_q3 and df_em_fc.frequency_commits[i] > fc_q3: 
    plt.text(df_em_fc.modified_lines[i], y=df_em_fc.frequency_commits[i], s=df_em_fc.name[i], alpha=0.8, fontsize=8)

plt.show()

# Cria um df sem os arquivos de Teste
df_em_fc_no_test = df_em_fc[(df_em_fc["name"].str.contains('Test') == False)]

# Cria um df contendo apenas os arquivos .java de implementacao
df_em_fc_java_impl = df_em_fc_no_test[df_em_fc_no_test['name'].str.contains('.java', regex=False)]
df_em_fc_java_impl

df_fator_multiplicacao_em_fc_java_impl = df_em_fc_java_impl.copy()
df_fator_multiplicacao_em_fc_java_impl['factor1'] = df_fator_multiplicacao_em_fc_java_impl['modified_lines'] * df_fator_multiplicacao_em_fc_java_impl['frequency_commits']
df_fator_multiplicacao_em_fc_java_impl

s = df_fator_multiplicacao_em_fc_java_impl.copy()

plt.style.use('ggplot')

plt.figure(figsize=(12,8))
sns.scatterplot(data=df_em_fc_java_impl, x='modified_lines', y='frequency_commits')

abbr={'titulo':'Modificações de LoCs x Frequência de Commits', 'modified_lines':'Modificações de Locs', 'frequency_commits':'Frequência de Commits'}

plt.title(f"Análise do Repositório Promocity : {abbr['modified_lines']} x {abbr['frequency_commits']}")
plt.xlabel(abbr['modified_lines'])
plt.ylabel(abbr['frequency_commits'])

plt.show()

lista_temp_index_modified_lines = []
for items in df_em_fc_java_impl.modified_lines.items():
  lista_temp_index_modified_lines.append((items[0], items[1]))

list_initial_critical_files_from_sp = []

plt.style.use('ggplot')
plt.figure(figsize=(12,8))
sns.scatterplot(data=df_em_fc_java_impl, x='modified_lines', y='frequency_commits')

abbr={'titulo':'Modificações de LoCs x Frequência de Commits', 'modified_lines':'Modificações de Locs', 'frequency_commits':'Frequência de Commits'}

plt.title(f"Análise do Repositório Promocity : {abbr['modified_lines']} x {abbr['frequency_commits']}")
plt.xlabel(abbr['modified_lines'])
plt.ylabel(abbr['frequency_commits'])
          
for i in lista_temp_index_modified_lines:
  if df_em_fc_java_impl.modified_lines[i[0]] > em_q3_java_impl and df_em_fc_java_impl.frequency_commits[i[0]] > fc_q3_java_impl: 
      plt.text(df_em_fc_java_impl.modified_lines[i[0]], y=df_em_fc_java_impl.frequency_commits[i[0]], s=df_em_fc_java_impl.name[i[0]], alpha=0.8, fontsize=8)
      list_initial_critical_files_from_sp.append( (df_em_fc_java_impl.name[i[0]], df_em_fc_java_impl.modified_lines[i[0]], df_em_fc_java_impl.frequency_commits[i[0]]) )

#Mean values          
plt.axvline(x=em_q3_java_impl, color='k',linestyle='--', linewidth=1) 
plt.axhline(y=fc_q3_java_impl, color='k', linestyle='--', linewidth=1)           

#Quadrant Marker          
plt.text(x=2000, y=100, s="Q1",alpha=0.8,fontsize=12, color='b')
plt.text(x=2000, y=0, s="Q4",alpha=0.8,fontsize=12, color='b')
plt.text(x=0, y=0, s="Q3", alpha=0.8,fontsize=12, color='b')
plt.text(x=0, y=100, s="Q2", alpha=0.8,fontsize=12, color='b')  

plt.show()

for item in list_initial_critical_files_from_sp:
  print(item)

# Pego da secao de analise de Architectural Smells
# selecao de classes criticas que pertencem ao Q1 (quadrante1) -> Modified LOC ALTA e Frequencia de Commits Alta
my_temp_lista_arquivos_criticos = [('StoreController.java', 439, 11), ('UserController.java', 963, 22), ('UserLocationMonitoring.java', 316, 11), ('Users.java', 350, 11)]

my_temp_lista_arquivos_criticos_names = []
for i in range(0,  len(my_temp_lista_arquivos_criticos)):
  my_temp_lista_arquivos_criticos_names.append(my_temp_lista_arquivos_criticos[i][0])

lista_temp_index_modified_lines = []
for items in df_em_fc_java_impl.modified_lines.items():
  lista_temp_index_modified_lines.append((items[0], items[1]))

list_initial_critical_files_from_sp = []

plt.style.use('ggplot')
plt.figure(figsize=(12,8))
sns.scatterplot(data=df_em_fc_java_impl, x='modified_lines', y='frequency_commits')

abbr={'titulo':'LOCs Modifications x Files Occurrence in Commits', 'modified_lines':'LOCs Modifications', 'frequency_commits':'Files Occurrence in Commits'}

plt.title(f"Analysis of Promocity Repository : {abbr['modified_lines']} x {abbr['frequency_commits']}")
plt.xlabel(abbr['modified_lines'])
plt.ylabel(abbr['frequency_commits'])
          
for i in lista_temp_index_modified_lines:
  if df_em_fc_java_impl.modified_lines[i[0]] > em_q3_java_impl and df_em_fc_java_impl.frequency_commits[i[0]] > fc_q3_java_impl: 
    if df_em_fc_java_impl.name[i[0]] in my_temp_lista_arquivos_criticos_names:
      plt.text(df_em_fc_java_impl.modified_lines[i[0]], y=df_em_fc_java_impl.frequency_commits[i[0]], s=df_em_fc_java_impl.name[i[0]], alpha=0.8, fontsize=8)

#Mean values          
plt.axvline(x=em_q3_java_impl, color='k',linestyle='--', linewidth=1) 
plt.axhline(y=fc_q3_java_impl, color='k', linestyle='--', linewidth=1)           

#Quadrant Marker          
plt.text(x=2000, y=100, s="Q1",alpha=0.8,fontsize=12, color='b')
plt.text(x=2000, y=0, s="Q4",alpha=0.8,fontsize=12, color='b')
plt.text(x=0, y=0, s="Q3", alpha=0.8,fontsize=12, color='b')
plt.text(x=0, y=100, s="Q2", alpha=0.8,fontsize=12, color='b')  

plt.savefig('scatter_plot_mloc_foc.png')
plt.show()

# Gera um arquivo contendo todos os arquivos .java do projeto Cassandra
executa_comando(comando='find promocity/src/main/java/ufc/cmu/promocity -name "*.java" > arquivosjava.txt')

# Cria duas listas contendo o conjunto de arquivos da versão analisada
lista_linhas_arquivos_cassandra = []
lista_colunas_arquivos_cassandra = []

with open('arquivosjava.txt', mode='r+', encoding='utf-8') as file:
  for line in file:  
    line = line.rstrip()
    line = line.replace('promocity/src/main/java/', '')
    line = line.replace('/', '.')
    lista_linhas_arquivos_cassandra.append(line)
    lista_colunas_arquivos_cassandra.append(line)

# Dado 'org.apache.cassandra.index.Index.java'
# Retorne 'pilot/analises/designite/v-3-11-11/src/java/org/apache/cassandra/index/Index.java'

def get_path_file(my_file, src_java_path='promocity/src/main/java/'):
  path_file = None
  my_file = my_file.replace('.java', '') # org.apache.cassandra.index.Index
  my_file = my_file.replace('.', '/') # org/apache/cassandra/index/Index
  my_file = my_file + '.java' # org/apache/cassandra/index/Index.java
  path_file =  src_java_path  + my_file 
  return path_file

def teste_find_word_in_file(my_file, my_word):
    with open(my_file) as f:
        datafile = f.readlines()
        found = False  # This isn't really necessary
        for line in datafile:
          if my_word in line:
            # found = True # Not necessary
            return True
    return False  # Because you finished the search without finding
  
def lista_arquivos_que_dependem_de(my_file, dicionario):
  lista_temp = []
  my_file = my_file.replace('/','.')
  if my_file in dicionario:
    for each in dicionario[my_file]:
      if each[2] == 1: 
        lista_temp.append(each)
  return lista_temp

import datetime

t1 = datetime.datetime.now()

dicionario_dsm = {}
lista_aux = []

for each_file in lista_linhas_arquivos_cassandra:
  for each_elemento_coluna in lista_colunas_arquivos_cassandra:
    my_search = each_elemento_coluna
    my_search = my_search.replace('.java', ';')
    my_path = get_path_file(my_file=each_file)
    if teste_find_word_in_file(my_file=my_path,my_word=my_search):
      item = (each_file, each_elemento_coluna, 1)
    else:
      item = (each_file, each_elemento_coluna, 0)
    lista_aux.append(item)
  dicionario_dsm[each_file] = lista_aux 
  lista_aux = []
  
t2 = datetime.datetime.now()

delta = t2 - t1

print(f'Tempo para criar o dicionarário dsm: {delta}, itens percorridos: {len(dicionario_dsm)}')

temp = 'ufc.cmu.promocity.backend.controller.UserController.java'
temp = temp.replace('/','.')
print(dicionario_dsm[temp])

# Exemplo: Relação de Arquivos que UserController.java depende

i = 1
for tupla in dicionario_dsm[temp]:
  if tupla[2] == 1:
    print(f'{i}, {tupla}')
    i = i + 1

t1 = datetime.datetime.now()

dicionario_dsm_depende_de = {}
lista_aux = []

for each_file in lista_linhas_arquivos_cassandra:
  for each_elemento_coluna in lista_colunas_arquivos_cassandra:
    my_search = each_file
    my_search = my_search.replace('.java', ';')
    my_path = get_path_file(my_file=each_elemento_coluna)
    if teste_find_word_in_file(my_file=my_path,my_word=my_search):
      item = (each_elemento_coluna, each_file, 1)
    else:
      item = (each_elemento_coluna, each_file, 0)
    lista_aux.append(item)
  dicionario_dsm_depende_de[each_file] = lista_aux 
  lista_aux = []
  
t2 = datetime.datetime.now()

delta = t2 - t1

print(f'Tempo para criar o dicionarário dsm: {delta}, itens percorridos: {len(dicionario_dsm_depende_de)}')

# Exemplo: Relação de Arquivos que dependem de UserController.java

i = 1
for tupla in lista_arquivos_que_dependem_de(my_file='ufc.cmu.promocity.backend.controller.UserController.java', dicionario=dicionario_dsm_depende_de):
  if tupla[2] == 1:
    print(f'{i}, {tupla}')
    i += 1

# Exemplo: Relação de Arquivos que dependem de User.java

i = 1
for tupla in lista_arquivos_que_dependem_de(my_file='ufc.cmu.promocity.backend.model.Users.java', dicionario=dicionario_dsm_depende_de):
  if tupla[2] == 1:
    print(f'{i}, {tupla}')
    i += 1

# Dada uma classe e o arquivo texto contendo todos os arquivos do repositorio, 
# retorna o pacote da classe junto com classe
def get_file_package(my_file, my_content):
  with open(my_content, mode='r+', encoding='utf-8') as file:
    for line in file:
      if my_file in line:
        line = line.replace('promocity/src/main/java/', '')
        line = line.replace('/','.')
        line = line.strip()
        return line

# Dada a lista de arquivos criticos [(arquivo1, qtd linhas modificadas, frequencia de commits), (), ...]
# arquivo texto contendo todos os arquivos do repositorio
# dicionario com a DSM file_a uses file_b
# retorna o dicionario com chave file_a e valores lista de arquivos que file_a chama(importa)
def get_dict_file_a_uses_file_b(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm):
  dict_file_a_uses_file_b = {}
  lista_file_a_uses_file_b = []
  for each in lista_arquivos_criticos:
    item = each[0]
    key_file = get_file_package(my_file=item, my_content=content)
    for each_tupla in my_dictionary[key_file]:
      if each_tupla[2] == 1:
        lista_file_a_uses_file_b.append(each_tupla[1])
    dict_file_a_uses_file_b[key_file] = lista_file_a_uses_file_b
    lista_file_a_uses_file_b = []
  return dict_file_a_uses_file_b

# Todo: revisar, pois está substituindo config.java por GuardrailsConfig.java
# Dada a lista de arquivos criticos [(arquivo1, qtd linhas modificadas, frequencia de commits), (), ...]
# arquivo texto contendo todos os arquivos do repositorio
# dicionario com a DSM file_a depende de file_b
# retorna o dicionario com chave file_a e valores lista de arquivos que dependem de file_a
def get_dict_file_impact_other_files(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de):
  dict_file_impact_other_files = {}
  lista_file_a_depends_on_file_b = []
  
  for each in lista_arquivos_criticos:
    item = each[0]
    key_file = get_file_package(my_file=item, my_content=content)
    for tupla in lista_arquivos_que_dependem_de(my_file=key_file, dicionario=my_dictionary):
      if tupla[2] == 1:
        lista_file_a_depends_on_file_b.append(tupla[0])
    dict_file_impact_other_files[key_file] = lista_file_a_depends_on_file_b
    lista_file_a_depends_on_file_b = []
  return dict_file_impact_other_files

lista_arquivos_criticos = [('StoreController.java', 439, 11), ('UserController.java', 963, 22), ('UserLocationMonitoring.java', 316, 11), ('Users.java', 350, 11)]

get_dict_file_a_uses_file_b(lista_arquivos_criticos)

# Relação de Arquivos que dependem de Users.java
dict_file_impact_other_files = {}
lista_file_a_depends_on_file_b = []

for tupla in lista_arquivos_que_dependem_de(my_file='ufc.cmu.promocity.backend.model.Users.java', dicionario=dicionario_dsm_depende_de):
  if tupla[2] == 1:
    lista_file_a_depends_on_file_b.append(tupla[0])
dict_file_impact_other_files['ufc.cmu.promocity.backend.model.Users.java'] = lista_file_a_depends_on_file_b

dict_file_impact_other_files['ufc.cmu.promocity.backend.model.Users.java']

len(dict_file_impact_other_files['ufc.cmu.promocity.backend.model.Users.java'])

# Dado um arquivo chave, mostra a lista de arquivos que dependem do arquivo chave
dict_arquivos_dependentes_arquivos_criticos = get_dict_file_impact_other_files(lista_arquivos_criticos)

lista_arquivos_impactados = []
l_ac = []
l_adac = []
l_tamanho_adac = []
for key, value in dict_arquivos_dependentes_arquivos_criticos.items():
  print(key, value)
  l_ac.append(key)
  l_tamanho_adac.append(len(value))
  l_adac.append(value)

# dict_arquivos_dependentes_arquivos_criticos

df_arquivos_dependentes_arquivos_criticos = pd.DataFrame({'arquivos_criticos':l_ac, 'qtd_arquivos_dependentes':l_tamanho_adac, 'arquivos_dependentes':l_adac})
try: 
  df_arquivos_dependentes_arquivos_criticos.to_csv('arquivos_dependentes_arquivos_criticos.csv')
except Exception as ex:
  print(f'Erro ao salvar o arquivo arquivos_dependentes_arquivos_criticos.csv : {str(ex)}')

for key, value in dict_arquivos_dependentes_arquivos_criticos.items():
  print(f"Mudanças na classe {key} podem impactar {len(value)} classes")

for key, value in dict_arquivos_dependentes_arquivos_criticos.items():
  lista_arquivos_impactados = lista_arquivos_impactados + value

set_lista_arquivos_impactados = set(lista_arquivos_impactados)
lista_arquivos_impactados_unicos = list(set_lista_arquivos_impactados)

# Quantidade de arquivos impactados pelas classes críticas

print(f"Existem {len(lista_arquivos_impactados_unicos)} classes que podem ser impactados pelas {len(lista_arquivos_criticos)} classes críticas.")

print(f'Classes críticas: {len(lista_arquivos_criticos)}')
print(f'Classes impactadas: {len(lista_arquivos_impactados_unicos)}')
print(f'Total de classes .java do sistema: {df_em_fc_java_impl.shape[0]}')

print(f'Existem {len(lista_arquivos_criticos)} arquivos: {[item[0] for item in lista_arquivos_criticos]} que podem impactar {len(lista_arquivos_impactados_unicos)} dos {df_em_fc_java_impl.shape[0]} arquivos .java')
print(f'{len(lista_arquivos_impactados_unicos)} Potenciais arquivos impactados: {lista_arquivos_impactados_unicos}')

# df.groupby(['A','C'])['B'].sum()
df_lm = df_files_commits_from_db.copy()
qtd_lm = df_lm[['file_is_java','file_filename', 'modified_lines']][df_lm.file_is_java==1].groupby('file_filename')['modified_lines'].sum()
df_qtd_lm = qtd_lm.to_frame()
#df_qtd_lm['file_filename'] = df_qtd_lm.index
df_qtd_lm = df_qtd_lm.reset_index()
df_qtd_lm

# Quantidade de linhas modificadas dos arquivos criticos
dict_modified_lines_arquivos_criticos = {}

for each in lista_arquivos_criticos:
  qtd_temp = df_qtd_lm[df_qtd_lm.file_filename == each[0]]['modified_lines'].to_list()
  if len(qtd_temp) == 1:
    dict_modified_lines_arquivos_criticos[each[0]] = qtd_temp[0] 

dict_modified_lines_arquivos_criticos

soma_modified_lines_arquivos_criticos = 0
for key, value in dict_modified_lines_arquivos_criticos.items():
  soma_modified_lines_arquivos_criticos = soma_modified_lines_arquivos_criticos + value

print(f'As {len(dict_modified_lines_arquivos_criticos)} classes criticas mudaram {soma_modified_lines_arquivos_criticos} linhas no sistema')

lista_nomes_arquivos_impactados_unicos = []

for each in lista_arquivos_impactados_unicos:
  each = each.split('.')
  temp = each[-2] + '.' + each[-1]
  lista_nomes_arquivos_impactados_unicos.append(temp)

# Quantidade de linhas modificadas dos arquivos impactados
dict_modified_lines_arquivos_impactados = {}

for each in lista_nomes_arquivos_impactados_unicos:
  qtd_temp = df_qtd_lm[df_qtd_lm.file_filename == each]['modified_lines'].to_list()
  if len(qtd_temp) == 1:
    dict_modified_lines_arquivos_impactados[each] = qtd_temp[0]
  else:
    dict_modified_lines_arquivos_impactados[each] = 0

soma_modified_lines_arquivos_impactados = 0
for key, value in dict_modified_lines_arquivos_impactados.items():
  soma_modified_lines_arquivos_impactados = soma_modified_lines_arquivos_impactados + value

print(f'As {len(dict_modified_lines_arquivos_impactados)} classes impactadas, pelos arquivos críticos, mudaram {soma_modified_lines_arquivos_impactados} linhas no sistema')

## Soma de todas as linhas modificadas pelos arquivos .java 
qtd_arquivos_java = df_qtd_lm.shape[0]
qtd_modified_lines_arquivos_java = df_qtd_lm['modified_lines'].sum()

print(f'{qtd_arquivos_java} mudaram {qtd_modified_lines_arquivos_java} no sistema')

# As classes críticas e as classes impactada correspondem a X linhas modificadas 
# o que dá P % de linhas modificadas no sistema

soma_modified_lines_analisadas = soma_modified_lines_arquivos_criticos + soma_modified_lines_arquivos_impactados

percentual_modified_lines_analisadas = round( (soma_modified_lines_analisadas/qtd_modified_lines_arquivos_java) * 100 , 2)

print(f'As {len(dict_modified_lines_arquivos_criticos)} classes criticas e as {len(dict_modified_lines_arquivos_impactados)} classes impactadas correspondem a {percentual_modified_lines_analisadas}% das linhas modificadas no sistema')

# Dada uma classe critica e um dataframe contendo todos os commits analisados
# retorna a lista de arquivos que sao modificados junto com o arquivo critico
def get_lista_arquivos_modificados_with_critico(filename, df):
  lista_temp_arquivos = []
  lista_temp = []

  lista_arquivos_modificados_com_filename = df[df['modified_files'].str.contains(filename)]['modified_files'].to_list()

  for each in lista_arquivos_modificados_com_filename:
    lista_temp = each.split(',')
    lista_temp_arquivos = lista_temp_arquivos + lista_temp
    lista_temp = []

  set_lista_temp_arquivos = set(lista_temp_arquivos)
  lista_temp_arquivos_unicos = list(set_lista_temp_arquivos)
  return lista_temp_arquivos_unicos

# Data a lista de arquivos criticos e todos os commits da faixa analisada
# retorna um dicionario com chave no arquivo critico e a lista dos arquivos que sao modificados em conjunto com ele.
def get_dict_arquivos_modificados_with_critico(lista, df):
  dict_arquivos_modificados_with_critico = {}
  lista_temp = []
  for filename in lista:
    lista_temp = get_lista_arquivos_modificados_with_critico(filename[0], df)
    dict_arquivos_modificados_with_critico[filename[0]] = lista_temp
    lista_temp = []
  return dict_arquivos_modificados_with_critico

# Dado um arquivo critico, 
# retorna a lista de arquivos impactados por ele
def get_arquivos_impactados_por_file(lista, filename):
  lista_arquivos_criticos = lista
  for key, value in get_dict_file_impact_other_files(lista_arquivos_criticos).items():
    if filename in key: 
      lista_temp = []
      for file in value:
        temp = file.split('.')[-2]
        temp = temp + '' + '.java'
        lista_temp.append(temp)
  return lista_temp

# dicionário de arquivos criticos e seus arquivos que dependem dele e também sao co-change
def get_dict_arquivos_dependem_e_cochange_critico(lista):
  lista_arquivos_criticos = lista
  dict_arquivos_dependem_e_cochange_critico = {}

  for filename in lista_arquivos_criticos:
    lista_temp_dependem_filename = get_arquivos_impactados_por_file(lista_arquivos_criticos, filename[0])
    lista_temp_cochange_filename = dict_arquivo_critico_cochange[filename[0]]

    lista_arquivos_dependem_de_and_cochange_filename = []
    for each in lista_temp_dependem_filename:
      if each in lista_temp_cochange_filename:
        lista_arquivos_dependem_de_and_cochange_filename.append(each)
    
    dict_arquivos_dependem_e_cochange_critico[filename[0]] = lista_arquivos_dependem_de_and_cochange_filename

  return dict_arquivos_dependem_e_cochange_critico

# Dataframe contendo todos os commits da faixa analisada
df = df_commits_from_db[['name', 'modified_files']]

# Lista arquivos críticos
print(f'{len(lista_arquivos_criticos)}, {lista_arquivos_criticos}')

# Arquivos impactados únicos
print(f' {len(lista_arquivos_impactados_unicos)}, {lista_arquivos_impactados_unicos}')

# Dicionário com o arquivo crítico e todos os seus arquivos co-change (além dos arquivos de implementação existem os arquivos .txt, de configuração, testes, entre outros)
dict_arquivo_critico_cochange = get_dict_arquivos_modificados_with_critico(lista_arquivos_criticos, df)
print(f'{len(dict_arquivo_critico_cochange)}, {dict_arquivo_critico_cochange}')

#1) Arquivos que dependem de "UserController":
lista_dependem_storageservice = get_arquivos_impactados_por_file(lista_arquivos_criticos, "UserController.java")
print(f'Arquivos que dependem de "UserController": {len(lista_dependem_storageservice)}')

#2) Arquivos que foram commitados pelo menos uma vez com "UserController.java"
filename = "UserController.java"
lista_cochange_storageservice = dict_arquivo_critico_cochange[filename]
print(f'Arquivos que foram commitados pelo menos uma vez com "UserController.java": {len(lista_cochange_storageservice)}')

#3) Lista arquivos depedentes e cochange com critico
lista_arquivos_dependem_de_and_cochange_storageservice = []
for each in lista_dependem_storageservice:
  if each in lista_cochange_storageservice:
    lista_arquivos_dependem_de_and_cochange_storageservice.append(each)
print(f'QTD de arquivos_dependem_de_and_cochange_UserController: {len(lista_arquivos_dependem_de_and_cochange_storageservice)}')
print('')
print(f'Arquivos que dependem de UserController e são co-change: {lista_arquivos_dependem_de_and_cochange_storageservice}')

# Dicionário contendo o arquivo crítico, os arquivos que ele impacta e são commitados em conjunto pelo menos uma vez.
for key, value in get_dict_arquivos_dependem_e_cochange_critico(lista_arquivos_criticos).items():
  print(key, value)

lista_arquivos_impactados_com_cochange = []
lista_arquivos_criticos_temp = []
lista_dependente_e_cochange = []
lista_tamanho_dependente_e_cochange = []
for key, value in get_dict_arquivos_dependem_e_cochange_critico(lista_arquivos_criticos).items():
  print(f'A classe {key} impacta outras {len(value)} classes que dependem de {key} e são co-change com {key} ')
  lista_arquivos_criticos_temp.append(key)
  lista_dependente_e_cochange.append(value)
  lista_tamanho_dependente_e_cochange.append(len(value))

  lista_arquivos_impactados_com_cochange = lista_arquivos_impactados_com_cochange + value

dict_my_criticos_atd = {'arquivos_criticos': lista_arquivos_criticos_temp, 'qtd_dependentes_e_cochange':lista_tamanho_dependente_e_cochange, 'dependentes_e_cochange':lista_dependente_e_cochange}
df_my_criticos_atd = pd.DataFrame(dict_my_criticos_atd)
print(df_my_criticos_atd)


try:
  df_my_criticos_atd.to_csv('arquivos_dependentes_e_cochange_com_arquivos_criticos.csv')
except Exception as ex:
  print(f'Erro ao salvar o arquivo arquivos_dependentes_e_cochange_com_arquivos_criticos.csv: {str(ex)}')

df_temp2 = df_my_criticos_atd[['arquivos_criticos', 'qtd_dependentes_e_cochange']].sort_values('qtd_dependentes_e_cochange', ascending = False)
df_temp2

sum(df_temp2['qtd_dependentes_e_cochange'])

# dicionario contendo o arquivo impactado e suas linhas modificadas
dict_arquivos_impactados_com_cochange = {}

for each in lista_arquivos_impactados_com_cochange:
  qtd_temp = df_qtd_lm[df_qtd_lm.file_filename == each]['modified_lines'].to_list()
  if len(qtd_temp) == 1:
    dict_arquivos_impactados_com_cochange[each] = qtd_temp[0]
  else:
    dict_arquivos_impactados_com_cochange[each] = 0

print(f'{len(dict_arquivos_impactados_com_cochange)}, {dict_arquivos_impactados_com_cochange}')

soma_modified_lines_arquivos_impactados_com_cochange = 0

for key, value in dict_arquivos_impactados_com_cochange.items():
  soma_modified_lines_arquivos_impactados_com_cochange = soma_modified_lines_arquivos_impactados_com_cochange + value

soma_modified_lines_arquivos_impactados_com_cochange

print(f'Existem {qtd_arquivos_java} classes que mudaram um total de {qtd_modified_lines_arquivos_java} linhas no sistema dentro da faixa analisada')

print(f'Existem {len(dict_arquivos_impactados_com_cochange)} classes que podem indicar ATD e mudaram {soma_modified_lines_arquivos_impactados_com_cochange} linhas no sistema dentro da faixa analisada')

print(f'A estimativa do esforço gasto com ATD foi de {soma_modified_lines_arquivos_impactados_com_cochange} linhas em relação ao total de {qtd_modified_lines_arquivos_java} linhas alteradas no sistema dentro da faixa analisada')

print(f'Percentual de esforço (ATD) gasto com alterações de linhas: {round((soma_modified_lines_arquivos_impactados_com_cochange / qtd_modified_lines_arquivos_java) * 100, 2)}% do total de linhas alteradas dentro da faixa analisada')
