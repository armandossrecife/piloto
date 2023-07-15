URL_REPOSITORIO_GIT = 'https://github.com/google/gson.git'
NOME_REPOSITORIO = 'gson'
import utilidades
# 1. Carrega dependencias
utilidades.carrega_dependencias()

import extracao
# 2. Extrai informacoes de commits e arquivos modificados em cada commmit
extracao.extrai_informacoes_repositorio(my_repositorio=URL_REPOSITORIO_GIT, nome_repositorio=NOME_REPOSITORIO)

import carrega_dataframes
# 3. Carrega os dados das tabelas em dataframes
df_commits_from_db, df_files_from_db, df_files_commits_from_db = carrega_dataframes.load_dataframes(database_name=carrega_dataframes.DATA_BASE)

# 3.1 Faz alguns ajustes nos dataframes para o calculo de AMLOC
df_files_from_db['modified_lines'] = df_files_from_db.added_lines + df_files_from_db.deleted_lines
df_files_commits_from_db['modified_lines'] = df_files_commits_from_db.file_added_lines + df_files_commits_from_db.file_deleted_lines

import analisa_metricas
# 4. Faz a analise das metricas de AMLOC
print('Calcula o AMLOC')
df_accumulated_modified_locs, df_accumulated_modified_locs_boxplot, group_files_modified_lines = analisa_metricas.get_accumulated_modified_locs(df_files_from_db)

print('Gera o boxplot de AMLOC de todos os arquivos do repositório')
analisa_metricas.gera_boxplot_accumulated_modified_locs(df_accumulated_modified_locs_boxplot)

print('Gera o boxplot de AMLOC')
df_accumulated_modified_locs_boxplot_validos = analisa_metricas.get_accumulated_modified_locs_boxplot_valid(df_accumulated_modified_locs_boxplot)

print('Calcula os quartiles de AMLOC')
em_q1, em_q2, em_q3, em_q4 = analisa_metricas.get_quartiles_offiles_modified_lines(group_files_modified_lines,df_accumulated_modified_locs_boxplot_validos)

print('Calcula o AMLOC dos arquivos .java')
df_locm_java_impl = analisa_metricas.get_df_accumulated_modified_java_files(df_accumulated_modified_locs)
print('Gera o boxplot de AMLOC dos arquivos .java')
df_boxplot_em_java_impl = analisa_metricas.show_boxplot_accumulated_modified_java_files(df_locm_java_impl)

print('Calcula o AMLOC dos arquivos .java (Válidos - arquivos que modificaram pelo menos uma vez)')
df_boxplot_em_java_impl_valid = analisa_metricas.get_accumulated_modified_java_files_valid(df_boxplot_em_java_impl)
print('Calcula os quartiles referente ao AMLOC dos arquivos .java')
em_q1_java_impl, em_q2_java_impl, em_q3_java_impl, em_q4_java_impl = analisa_metricas.get_quartiles_offiles_modified_lines_java_files_valid(df_boxplot_em_java_impl_valid)

# 5. Faz a analise das metricas de Complexidade Ciclomatica
print('Calculo da Complexidade Ciclomatica')
df_complexidade_ciclomatica = analisa_metricas.get_complexidade_ciclomatica(df_files_commits_from_db)
print(df_complexidade_ciclomatica)
print('Calcula o boxplot de complexidade ciclomática')
df_cc_temp,df_boxplot_cc_temp = analisa_metricas.get_boxplot_complexidade_ciclomatica(df_complexidade_ciclomatica)
print('Calcula os quartiles das complexidades ciclomáticas')
em_q1_cc_temp,em_q2_cc_temp, em_q3_cc_temp, em_q4_cc_temp = analisa_metricas.get_quartiles_complexidade_ciclomatica(df_boxplot_cc_temp)

print('Calcula a complexidade ciclomática apenas dos arquivos .java')
df_cc_temp_java_impl, df_cc_temp_boxplot_em_java_impl = analisa_metricas.get_boxplot_complexidade_ciclomatica_only_java(df_cc_temp)
print('Calcula os quartiles de complexidade ciclomática dos arquivos .java')
em_q1_cc_temp_java_impl, em_q2_cc_temp_java_impl, em_q3_cc_temp_java_impl, em_q4_cc_temp_java_impl= analisa_metricas.get_quartiles_complexidade_ciclomatica_java_impl(df_cc_temp_boxplot_em_java_impl)

import scatter_plots
# 6. Faz a analise de FOCs e geracao dos scatter plots AMLOC e FOC
print('Faz a análise de AMLOC,FOC e Scatter Plot')

print('Calcula frequencia dos commits')
df_fc, df_boxplot_fc = scatter_plots.calcula_frequencia_commits(df_files_from_db)

print('Gera o boxplot da frequencia de commits')
scatter_plots.gera_boxplot_frequencia_commits(df_boxplot_fc)

print('Calcula os quartiles das frequencias de commits')
fc_q1,fc_q2, fc_q3, fc_q4 = scatter_plots.calcula_quartiles_frequencia_commits(df_boxplot_fc)

print('Gera o boxplot da FOC apenas dos arquivos .java')
df_fc_java_impl, df_boxplot_fc_java_impl, df_boxplot_fc_java_impl2 = scatter_plots.gera_boxplot_frequencia_commits_only_java(df_fc)

fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl = scatter_plots.calcula_quartiles_frequencia_commmits_no_outliers_less_3(df_boxplot_fc_java_impl2)

df_em_fc = scatter_plots.gera_df_foc_amloc(df_accumulated_modified_locs, df_fc)

df_fator_multiplicacao = scatter_plots.gera_df_fator_foc_amloc(df_em_fc)

df_em_fc_java_impl, df_fator_multiplicacao_em_fc_java_impl = scatter_plots.gera_scatter_plot_foc_amloc(df_em_fc)

list_initial_critical_files_from_sp = scatter_plots.gera_scatter_plot_foc_amloc_com_quadrantes(df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl)

list_critical_files = scatter_plots.gera_scatter_plot_final_foc_amloc_com_quadrantes(list_initial_critical_files_from_sp, df_em_fc_java_impl, em_q3_java_impl, fc_q2_java_impl)

import analise_dependencias_arquivos as ada

print('Faz a análise das dependências dos arquivos')

path_projeto_src_java = "gson/gson/src/main/java/"

# Faz a análise das dependências dos arquivos

ada.gera_arquivos_java(path_projeto=path_projeto_src_java, nome_arquivo='arquivosjava.txt')

lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra = ada.cria_duas_listas_arquivos_analisados(nome_arquivo='arquivosjava.txt', diretorio_src_main=path_projeto_src_java)

dicionario_dsm = ada.cria_dicionario_dsm(lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra, path_main=path_projeto_src_java)

dicionario_dsm_depende_de = ada.cria_dicionario_dsm_depende_de(lista_linhas_arquivos_cassandra, lista_colunas_arquivos_cassandra, path_main=path_projeto_src_java)

lista_arquivos_criticos = list_critical_files
print(len(lista_arquivos_criticos))
print(lista_arquivos_criticos)

# arquivosjava.txt e dicionario_dsm
ada.get_dict_file_a_uses_file_b(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm, path_main=path_projeto_src_java)

ada.get_dict_file_a_uses_file_b(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de, path_main=path_projeto_src_java)

dict_arquivos_dependentes_arquivos_criticos, lista_arquivos_impactados, l_ac, l_adac, l_tamanho_adac = ada.mostra_lista_arquivos_dependentes(lista_arquivos_criticos, content='arquivosjava.txt', my_dictionary=dicionario_dsm_depende_de, path_main=path_projeto_src_java)

df_arquivos_dependentes_arquivos_criticos = ada.gera_df_arquivos_dependentes_arquivos_criticos(l_ac, l_tamanho_adac, l_adac)

lista_arquivos_impactados_unicos = ada.gera_lista_arquivos_impactados_unicos(dict_arquivos_dependentes_arquivos_criticos, lista_arquivos_impactados)
print(f'Arquivos impactados unicos: {lista_arquivos_impactados_unicos}')

lista_nomes_arquivos_impactados_unicos, df_qtd_lm, dict_modified_lines_arquivos_criticos, soma_modified_lines_arquivos_criticos = ada.relatorio_linhas_alteradas_pelas_classes_criticas(lista_arquivos_impactados_unicos,lista_arquivos_criticos, df_em_fc_java_impl, df_files_commits_from_db)

print('Testes de impacto de mudancas')

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

print(f'{qtd_arquivos_java} arquivos mudaram {qtd_modified_lines_arquivos_java} LOC no sistema')

# As classes críticas e as classes impactada correspondem a X linhas modificadas
# o que dá P % de linhas modificadas no sistema

soma_modified_lines_analisadas = soma_modified_lines_arquivos_criticos + soma_modified_lines_arquivos_impactados

percentual_modified_lines_analisadas = round( (soma_modified_lines_analisadas/qtd_modified_lines_arquivos_java) * 100 , 2)

print(f'As {len(dict_modified_lines_arquivos_criticos)} classes criticas e as {len(dict_modified_lines_arquivos_impactados)} classes impactadas correspondem a {percentual_modified_lines_analisadas}% das linhas modificadas no sistema')


# Dataframe contendo todos os commits da faixa analisada
df = df_commits_from_db[['name', 'modified_files']]

# Lista arquivos críticos
print(f'{len(lista_arquivos_criticos)}, {lista_arquivos_criticos}')

# Arquivos impactados únicos
print(f' {len(lista_arquivos_impactados_unicos)}, {lista_arquivos_impactados_unicos}')

# Dicionário com o arquivo crítico e todos os seus arquivos co-change (além dos arquivos de implementação existem os arquivos .txt, de configuração, testes, entre outros)
dict_arquivo_critico_cochange = ada.get_dict_arquivos_modificados_with_critico(lista_arquivos_criticos, df)
print(f'{len(dict_arquivo_critico_cochange)}')




