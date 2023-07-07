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
print(df_commits_from_db[['name', 'modified_files']])

# procura por um commit especifico
df_commits_from_db[['name', 'modified_files']].query("name == 'promocity_fc85e473f543f543c68110d62624180fc3b24606'")

# Lista todos os arquivos e seus commits
print(df_files_from_db[['name', 'hash']].sort_values('name'))

# Mostra as Complexidades Ciclomáticas dos arquivos
df_files_commits_from_db[['file_filename', 'file_complexity', 'author_date']].sort_values(by=['file_filename', 'author_date'], ascending=True)

# Mostra as complexidades ciclomáticas de um determinado arquivo
df_files_commits_from_db[['file_filename', 'file_complexity', 'author_date']].sort_values(by=['file_filename', 'author_date'], ascending=True).query("file_filename == 'UserController.java'")