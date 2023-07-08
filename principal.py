import utilidades

# 1. Carrega dependencias
#utilidades.carrega_dependencias()

import extracao

# extrai informacoes de commits e arquivos modificados em cada commmit
#extracao.extrai_informacoes_repositorio(my_repositorio='https://github.com/armandossrecife/promocity.git')

import carrega_dataframes

df_commits_from_db, df_files_from_db, df_files_commits_from_db = carrega_dataframes.load_dataframes(database_name=carrega_dataframes.DATA_BASE)

print(df_commits_from_db)
print(df_files_from_db)
print(df_files_commits_from_db)
