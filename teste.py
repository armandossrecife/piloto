import utilidades
import extracao
import carrega_dataframes
import datetime

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


