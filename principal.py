import utilidades
# 1. Carrega dependencias
utilidades.carrega_dependencias()

import extracao
# 2. Extrai informacoes de commits e arquivos modificados em cada commmit
extracao.extrai_informacoes_repositorio(my_repositorio='https://github.com/armandossrecife/promocity.git', nome_repositorio='promocity')

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
print('Calcula frequencia dos commits')
df_fc, df_boxplot_fc = scatter_plots.calcula_frequencia_commits(df_files_from_db)

print('Gera o boxplot da frequencia de commits')
scatter_plots.gera_boxplot_frequencia_commits(df_boxplot_fc)

print('Calcula os quartiles das frequencias de commits')
fc_q1,fc_q2, fc_q3, fc_q4 = scatter_plots.calcula_quartiles_frequencia_commits(df_boxplot_fc)

print('Gera o boxplot da FOC apenas dos arquivos .java')
df_fc_java_impl, df_boxplot_fc_java_impl, df_boxplot_fc_java_impl2 = scatter_plots.gera_boxplot_frequencia_commits_only_java(df_fc)

print('Calcula os quartiles dos FOCs apenas dos arquivos .java com limite < 3')
fc_q1_java_impl, fc_q2_java_impl, fc_q3_java_impl, fc_q4_java_impl = scatter_plots.calcula_quartiles_frequencia_commmits_no_outliers_less_3(df_boxplot_fc_java_impl2)

print('Gera o dataframe de AMLOC e FOC')
df_em_fc = scatter_plots.gera_df_foc_amloc(df_accumulated_modified_locs, df_fc)

print('Gera o dataframe (fator de multiplicacao) de AMLOC e FOC')
df_fator_multiplicacao = scatter_plots.gera_df_fator_foc_amloc(df_em_fc)

print('Gera o scatter plot AMLOC e FOC')
df_em_fc_java_impl, df_fator_multiplicacao_em_fc_java_impl = scatter_plots.gera_scatter_plot_foc_amloc_only_java(df_em_fc)

print('Gera o scatter plot AMLOC e FOC com Quadrantes')
list_initial_critical_files_from_sp = scatter_plots.gera_scatter_plot_foc_amloc_com_quadrantes(df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl)

print('Gera o scatter FINAL plot AMLOC e FOC com Quadrantes')
list_critical_files = scatter_plots.gera_scatter_plot_final_foc_amloc_com_quadrantes(list_initial_critical_files_from_sp, df_em_fc_java_impl, em_q3_java_impl, fc_q3_java_impl)

print('Lista de arquivos críticos baseado em AMLOC e FOC:')
print(list_critical_files)