import utilidades
import extracao
import carrega_dataframes
import analisa_metricas
import os

DATA_BASE = "my_promocity.db"
URL_REPOSITORIO_GIT = 'https://github.com/armandossrecife/promocity.git'
NOME_REPOSITORIO = 'promocity'

# 1. Carrega dependencias
utilidades.carrega_dependencias()

# 2. Extrai informacoes de commits e arquivos modificados em cada commmit
extracao.extrai_informacoes_repositorio(my_repositorio=URL_REPOSITORIO_GIT, nome_repositorio=NOME_REPOSITORIO)

# 3. Carrega os dados das tabelas em dataframes
print('Carrega os dados nos dataframes')
df_commits_from_db, df_files_from_db, df_files_commits_from_db = carrega_dataframes.load_dataframes(database_name=DATA_BASE)
# 3.1 Faz alguns ajustes nos dataframes para o calculo de AMLOC
df_files_from_db['modified_lines'] = df_files_from_db.added_lines + df_files_from_db.deleted_lines
df_files_commits_from_db['modified_lines'] = df_files_commits_from_db.file_added_lines + df_files_commits_from_db.file_deleted_lines
print('Dataframes carregados com sucesso!')

# Cria uma pasta com o nome do repositorio dentro da pasta graficos
current_path = os.getcwd()
pasta_grafico_repositorio_boxplot = current_path + '/' + 'graficos' + '/'+ NOME_REPOSITORIO + '/' + 'boxplot'
pasta_quartis_repositorio = current_path + '/' + 'quartis' + '/'+ NOME_REPOSITORIO
utilidades.create_folder(pasta_grafico_repositorio_boxplot)
utilidades.create_folder(pasta_quartis_repositorio)

# 4. Faz a analise das metricas de AMLOC
print('Calcula o AMLOC')
df_accumulated_modified_locs, df_accumulated_modified_locs_boxplot, group_files_modified_lines = analisa_metricas.get_accumulated_modified_locs(df_files_from_db)
print('Gera o boxplot de AMLOC de todos os arquivos do repositório')
analisa_metricas.gera_boxplot_accumulated_modified_locs(df_accumulated_modified_locs_boxplot, NOME_REPOSITORIO)
print('Gera o boxplot de AMLOC')
df_accumulated_modified_locs_boxplot_validos = analisa_metricas.get_accumulated_modified_locs_boxplot_valid(df_accumulated_modified_locs_boxplot, NOME_REPOSITORIO)
print('Calcula os quartiles de AMLOC')
em_q1, em_q2, em_q3, em_q4 = analisa_metricas.get_quartiles_offiles_modified_lines(group_files_modified_lines,df_accumulated_modified_locs_boxplot_validos, NOME_REPOSITORIO)
print('Calcula o AMLOC dos arquivos .java')
df_locm_java_impl = analisa_metricas.get_df_accumulated_modified_java_files(df_accumulated_modified_locs)
print('Gera o boxplot de AMLOC dos arquivos .java')
df_boxplot_em_java_impl = analisa_metricas.show_boxplot_accumulated_modified_java_files(df_locm_java_impl, NOME_REPOSITORIO)
print('Calcula o AMLOC dos arquivos .java (Válidos - arquivos que modificaram pelo menos uma vez)')
df_boxplot_em_java_impl_valid = analisa_metricas.get_accumulated_modified_java_files_valid(df_boxplot_em_java_impl, NOME_REPOSITORIO)
print('Calcula os quartiles referente ao AMLOC dos arquivos .java')
em_q1_java_impl, em_q2_java_impl, em_q3_java_impl, em_q4_java_impl = analisa_metricas.get_quartiles_offiles_modified_lines_java_files_valid(df_boxplot_em_java_impl_valid, NOME_REPOSITORIO)

# 5. Faz a analise das metricas de Complexidade Ciclomatica
print('Calculo da Complexidade Ciclomatica')
df_complexidade_ciclomatica = analisa_metricas.get_complexidade_ciclomatica(df_files_commits_from_db)
print(df_complexidade_ciclomatica)
print('Calcula o boxplot de complexidade ciclomática')
df_cc_temp,df_boxplot_cc_temp = analisa_metricas.get_boxplot_complexidade_ciclomatica(df_complexidade_ciclomatica, NOME_REPOSITORIO)
print('Calcula os quartiles das complexidades ciclomáticas')
em_q1_cc_temp,em_q2_cc_temp, em_q3_cc_temp, em_q4_cc_temp = analisa_metricas.get_quartiles_complexidade_ciclomatica(df_boxplot_cc_temp, NOME_REPOSITORIO)
print('Calcula a complexidade ciclomática apenas dos arquivos .java')
df_cc_temp_java_impl, df_cc_temp_boxplot_em_java_impl = analisa_metricas.get_boxplot_complexidade_ciclomatica_only_java(df_cc_temp, NOME_REPOSITORIO)
print('Calcula os quartiles de complexidade ciclomática dos arquivos .java')
em_q1_cc_temp_java_impl, em_q2_cc_temp_java_impl, em_q3_cc_temp_java_impl, em_q4_cc_temp_java_impl= analisa_metricas.get_quartiles_complexidade_ciclomatica_java_impl(df_cc_temp_boxplot_em_java_impl, NOME_REPOSITORIO)

# 6. Faz a analise de FOCs (frequencia dos commits)
print('Calcula frequencia dos commits')
df_fc, df_boxplot_fc = analisa_metricas.calcula_frequencia_commits(df_files_from_db)
print('Gera o boxplot da frequencia de commits')
analisa_metricas.gera_boxplot_frequencia_commits(df_boxplot_fc, NOME_REPOSITORIO)
print('Calcula os quartiles das frequencias de commits')
fc_q1,fc_q2, fc_q3, fc_q4 = analisa_metricas.calcula_quartiles_frequencia_commits(df_boxplot_fc, NOME_REPOSITORIO)
print('Gera o boxplot da FOC apenas dos arquivos .java')
df_fc_java_impl, df_boxplot_fc_java_impl, df_boxplot_fc_java_impl2 = analisa_metricas.gera_boxplot_frequencia_commits_only_java(df_fc, NOME_REPOSITORIO)
fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl = analisa_metricas.calcula_quartiles_frequencia_commmits_no_outliers_less_3(df_boxplot_fc_java_impl2, NOME_REPOSITORIO)