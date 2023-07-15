import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def calcula_frequencia_commits(df_files_from_db):
  # calcula frequência dos arquivos na faixa de commits analisados
  list_of_files_frequency_in_commits = {}

  # Dataframe agrupados por arquivos e seus commits
  df_groupby_name = df_files_from_db[['name', 'hash']].groupby('name')

  print(f'Quantidade de grupos: {df_groupby_name.ngroups}')
  print(f'Grupos: {df_groupby_name.groups}')

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
  return df_fc, df_boxplot_fc

def gera_boxplot_frequencia_commits(df_boxplot_fc):
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc)
  plt.figure(figsize=(6,4))
  plt.savefig('boxplot_frequencia_commmits.png')
  # Constroi o Boxsplot sem os outliers
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc, showfliers=False)
  plt.savefig('boxplot_frequencia_commmits_no_outliers.png')

def calcula_quartiles_frequencia_commits(df_boxplot_fc):
  fc_q1 = np.percentile(df_boxplot_fc.frequency_commits , [25])
  fc_q2 = np.percentile(df_boxplot_fc.frequency_commits , [50])
  fc_q3 = np.percentile(df_boxplot_fc.frequency_commits , [75])
  fc_q4 = np.percentile(df_boxplot_fc.frequency_commits , [100])

  print(f'Quartis da Frequencia de Commits Q1: {fc_q1}, Q2: {fc_q2}, Q3: {fc_q3}, Q4: {fc_q4}')
  return fc_q1, fc_q2, fc_q3, fc_q4

def gera_boxplot_frequencia_commits_only_java(df_fc):
  # Cria um df sem os arquivos de Teste
  df_fc_no_test = df_fc[(df_fc["name"].str.contains('Test') == False)]

  # Cria um df contendo apenas os arquivos .java de implementacao
  df_fc_java_impl = df_fc_no_test[df_fc_no_test['name'].str.contains('.java', regex=False)]

  df_boxplot_fc_java_impl = df_fc_java_impl[['frequency_commits', 'File']]

  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl)
  plt.savefig('boxplot_frequencia_commmits_only_java.png')

  plt.figure(figsize=(6,4))
  # Constroi o Boxsplot sem os outliers
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl, showfliers=False)
  plt.savefig('boxplot_frequencia_commmits_only_java_no_outliers.png')

  # Remove as frequencias muito baixas (total de commits < 3)
  df_boxplot_fc_java_impl2 = df_boxplot_fc_java_impl.drop(df_boxplot_fc_java_impl[df_boxplot_fc_java_impl.frequency_commits < 3].index)
  plt.figure(figsize=(6,4))
  # Constroi o Boxsplot sem os outliers
  sns.boxplot(x='File', y='frequency_commits', data=df_boxplot_fc_java_impl2, showfliers=False)
  plt.savefig('boxplot_frequencia_commmits_only_java_no_outliers_less_3.png')
  return df_fc_java_impl, df_boxplot_fc_java_impl, df_boxplot_fc_java_impl2

def calcula_quartiles_frequencia_commmits_java_impl(df_fc_java_impl):
  fc_q1_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [25])
  fc_q2_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [50])
  fc_q3_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [75])
  fc_q4_java_impl = np.percentile(df_fc_java_impl.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')
  return fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl

def calcula_quartiles_frequencia_commmits_no_outliers(df_boxplot_fc_java_impl):
  fc_q1_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [25])
  fc_q2_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [50])
  fc_q3_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [75])
  fc_q4_java_impl = np.percentile(df_boxplot_fc_java_impl.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')
  return fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl

def calcula_quartiles_frequencia_commmits_no_outliers_less_3(df_boxplot_fc_java_impl2):
  fc_q1_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [25])
  fc_q2_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [50])
  fc_q3_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [75])
  fc_q4_java_impl = np.percentile(df_boxplot_fc_java_impl2.frequency_commits , [100])
  print(f'Quartis da Frequencia de Commits Q1: {fc_q1_java_impl}, Q2: {fc_q2_java_impl}, Q3: {fc_q3_java_impl}, Q4: {fc_q4_java_impl}')
  return fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl

def gera_df_foc_amloc(df_accumulated_modified_locs, df_fc):
  df_em_fc = df_accumulated_modified_locs[['name','modified_lines']]
  df_em_fc['frequency_commits'] = df_fc['frequency_commits']
  return df_em_fc

def gera_df_fator_foc_amloc(df_em_fc):
  df_fator_multiplicacao = df_em_fc.copy()
  df_fator_multiplicacao['factor1'] = df_fator_multiplicacao['modified_lines'] * df_fator_multiplicacao['frequency_commits']
  return df_fator_multiplicacao

def gera_scatter_plot_foc_amloc(df_em_fc, em_q3, fc_q3):
  plt.style.use('ggplot')
  plt.figure(figsize=(12,8))
  sns.scatterplot(data=df_em_fc, x='modified_lines', y='frequency_commits')
  abbr={'titulo':'Modificações de LoCs x Frequência de Commits', 'modified_lines':'Modificações de Locs', 'frequency_commits':'Frequência de Commits'}
  plt.title(f"Análise do Repositório Promocity : {abbr['modified_lines']} x {abbr['frequency_commits']}")
  plt.xlabel(abbr['modified_lines'])
  plt.ylabel(abbr['frequency_commits'])

  for i in range(df_em_fc.shape[0]):
    if df_em_fc.modified_lines[i] > em_q3[0] and df_em_fc.frequency_commits[i] > fc_q3[0]:
      plt.text(df_em_fc.modified_lines[i], y=df_em_fc.frequency_commits[i], s=df_em_fc.name[i], alpha=0.8, fontsize=8)
  plt.savefig('scatter_plot_foc_amloc.png')
  plt.show()

def gera_scatter_plot_foc_amloc(df_em_fc):
  # Cria um df sem os arquivos de Teste
  df_em_fc_no_test = df_em_fc[(df_em_fc["name"].str.contains('Test') == False)]
  # Cria um df contendo apenas os arquivos .java de implementacao
  df_em_fc_java_impl = df_em_fc_no_test[df_em_fc_no_test['name'].str.contains('.java', regex=False)]

  df_fator_multiplicacao_em_fc_java_impl = df_em_fc_java_impl.copy()
  df_fator_multiplicacao_em_fc_java_impl['factor1'] = df_fator_multiplicacao_em_fc_java_impl['modified_lines'] * df_fator_multiplicacao_em_fc_java_impl['frequency_commits']

  s = df_fator_multiplicacao_em_fc_java_impl.copy()

  plt.style.use('ggplot')
  plt.figure(figsize=(12,8))
  sns.scatterplot(data=df_em_fc_java_impl, x='modified_lines', y='frequency_commits')
  abbr={'titulo':'Modificações de LoCs x Frequência de Commits', 'modified_lines':'Modificações de Locs', 'frequency_commits':'Frequência de Commits'}
  plt.title(f"Análise do Repositório Promocity : {abbr['modified_lines']} x {abbr['frequency_commits']}")
  plt.xlabel(abbr['modified_lines'])
  plt.ylabel(abbr['frequency_commits'])
  plt.savefig('scatter_plot_foc_amloc_only_java.png')
  plt.show()
  return df_em_fc_java_impl, df_fator_multiplicacao_em_fc_java_impl

def gera_scatter_plot_foc_amloc_com_quadrantes(df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl):
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
    if df_em_fc_java_impl.modified_lines[i[0]] > em_q3_java_impl[0] and df_em_fc_java_impl.frequency_commits[i[0]] > fc_q3_java_impl[0]:
        plt.text(df_em_fc_java_impl.modified_lines[i[0]], y=df_em_fc_java_impl.frequency_commits[i[0]], s=df_em_fc_java_impl.name[i[0]], alpha=0.8, fontsize=8)
        list_initial_critical_files_from_sp.append( (df_em_fc_java_impl.name[i[0]], df_em_fc_java_impl.modified_lines[i[0]], df_em_fc_java_impl.frequency_commits[i[0]]) )

  #Mean values
  plt.axvline(x=em_q3_java_impl, color='k',linestyle='--', linewidth=1)
  plt.axhline(y=fc_q3_java_impl, color='k', linestyle='--', linewidth=1)

  #Quadrant Marker
  plt.text(x=500, y=10, s="Q1",alpha=0.8,fontsize=12, color='b')
  plt.text(x=500, y=0, s="Q4",alpha=0.8,fontsize=12, color='b')
  plt.text(x=0, y=0, s="Q3", alpha=0.8,fontsize=12, color='b')
  plt.text(x=0, y=10, s="Q2", alpha=0.8,fontsize=12, color='b')
  plt.savefig('scatter_plot_foc_amloc_only_java_com_quadrantes.png')
  plt.show()
  return list_initial_critical_files_from_sp

def gera_scatter_plot_final_foc_amloc_com_quadrantes(list_initial_critical_files_from_sp, df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl):
  for item in list_initial_critical_files_from_sp:
    print(item)
  # Pego da secao de analise de Architectural Smells
  # selecao de classes criticas que pertencem ao Q1 (quadrante1) -> Modified LOC ALTA e Frequencia de Commits Alta
  # my_temp_lista_arquivos_criticos = [('StoreController.java', 439, 11), ('UserController.java', 963, 22), ('UserLocationMonitoring.java', 316, 11), ('Users.java', 350, 11)]
  my_temp_lista_arquivos_criticos = list_initial_critical_files_from_sp

  my_temp_lista_arquivos_criticos_names = []
  for i in range(0,  len(my_temp_lista_arquivos_criticos)):
    my_temp_lista_arquivos_criticos_names.append(my_temp_lista_arquivos_criticos[i][0])

  lista_temp_index_modified_lines = []
  for items in df_em_fc_java_impl.modified_lines.items():
    lista_temp_index_modified_lines.append((items[0], items[1]))

  list_critical_files = []

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
        list_critical_files.append( (df_em_fc_java_impl.name[i[0]], df_em_fc_java_impl.modified_lines[i[0]], df_em_fc_java_impl.frequency_commits[i[0]]) )

  #Mean values
  plt.axvline(x=em_q3_java_impl, color='k',linestyle='--', linewidth=1)
  plt.axhline(y=fc_q3_java_impl, color='k', linestyle='--', linewidth=1)

  #Quadrant Marker
  plt.text(x=500, y=10, s="Q1",alpha=0.8,fontsize=12, color='b')
  plt.text(x=500, y=0, s="Q4",alpha=0.8,fontsize=12, color='b')
  plt.text(x=0, y=0, s="Q3", alpha=0.8,fontsize=12, color='b')
  plt.text(x=0, y=10, s="Q2", alpha=0.8,fontsize=12, color='b')

  plt.savefig('scatter_plot_mloc_foc_final_java_com_quadrantes.png')
  plt.show()
  return list_critical_files

def gera_scatter_plot_final_foc_amloc_com_quadrantes(list_initial_critical_files_from_sp, df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl):
  for item in list_initial_critical_files_from_sp:
    print(item)
  # Pego da secao de analise de Architectural Smells
  # selecao de classes criticas que pertencem ao Q1 (quadrante1) -> Modified LOC ALTA e Frequencia de Commits Alta
  my_temp_lista_arquivos_criticos = list_initial_critical_files_from_sp

  my_temp_lista_arquivos_criticos_names = []
  for i in range(0,  len(my_temp_lista_arquivos_criticos)):
    my_temp_lista_arquivos_criticos_names.append(my_temp_lista_arquivos_criticos[i][0])

  lista_temp_index_modified_lines = []
  for items in df_em_fc_java_impl.modified_lines.items():
    lista_temp_index_modified_lines.append((items[0], items[1]))

  list_critical_files = []

  plt.style.use('ggplot')
  plt.figure(figsize=(12,8))
  sns.scatterplot(data=df_em_fc_java_impl, x='modified_lines', y='frequency_commits')

  abbr={'titulo':'LOCs Modifications x Files Occurrence in Commits', 'modified_lines':'LOCs Modifications', 'frequency_commits':'Files Occurrence in Commits'}

  plt.title(f"Analysis of Promocity Repository : {abbr['modified_lines']} x {abbr['frequency_commits']}")
  plt.xlabel(abbr['modified_lines'])
  plt.ylabel(abbr['frequency_commits'])

  for i in lista_temp_index_modified_lines:
    if df_em_fc_java_impl.modified_lines[i[0]] > em_q3_java_impl[0] and df_em_fc_java_impl.frequency_commits[i[0]] > fc_q3_java_impl[0]:
      if df_em_fc_java_impl.name[i[0]] in my_temp_lista_arquivos_criticos_names:
        plt.text(df_em_fc_java_impl.modified_lines[i[0]], y=df_em_fc_java_impl.frequency_commits[i[0]], s=df_em_fc_java_impl.name[i[0]], alpha=0.8, fontsize=8)
        list_critical_files.append( (df_em_fc_java_impl.name[i[0]], df_em_fc_java_impl.modified_lines[i[0]], df_em_fc_java_impl.frequency_commits[i[0]]) )

  #Mean values
  plt.axvline(x=em_q3_java_impl, color='k',linestyle='--', linewidth=1)
  plt.axhline(y=fc_q3_java_impl, color='k', linestyle='--', linewidth=1)

  #Quadrant Marker
  plt.text(x=500, y=10, s="Q1",alpha=0.8,fontsize=12, color='b')
  plt.text(x=500, y=0, s="Q4",alpha=0.8,fontsize=12, color='b')
  plt.text(x=0, y=0, s="Q3", alpha=0.8,fontsize=12, color='b')
  plt.text(x=0, y=10, s="Q2", alpha=0.8,fontsize=12, color='b')

  plt.savefig('scatter_plot_mloc_foc_final_java_com_quadrantes.png')
  plt.show()
  return list_critical_files