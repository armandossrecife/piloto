import utilidades

# 1. Carrega dependencias
#utilidades.carrega_dependencias()

import extracao

# extrai informacoes de commits e arquivos modificados em cada commmit
#extracao.extrai_informacoes_repositorio(my_repositorio='https://github.com/armandossrecife/promocity.git')

import carrega_dataframes

df_commits_from_db, df_files_from_db, df_files_commits_from_db = carrega_dataframes.load_dataframes(database_name=carrega_dataframes.DATA_BASE)

# Faz alguns ajustes nos dataframes para o calculo de AMLOC
df_files_from_db['modified_lines'] = df_files_from_db.added_lines + df_files_from_db.deleted_lines
df_files_commits_from_db['modified_lines'] = df_files_commits_from_db.file_added_lines + df_files_commits_from_db.file_deleted_lines

import analisa_metricas

print('Calcula o AMLOC')
df_accumulated_modified_locs, df_accumulated_modified_locs_boxplot, group_files_modified_lines = analisa_metricas.get_accumulated_modified_locs(df_files_from_db)

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