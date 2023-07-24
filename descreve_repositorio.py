import os
import pandas as pd
import utilidades

# Descreve informacoes de linguages, loc, cc sobre o repositorio via analise de comandos de SO

def gera_df_info_repositorio(pasta_n_commit):
      # Quantidade de arquivos na pasta nome_repositorio
      # Quantidade de commits do repositorio nome_repositorio
      # Tamanho (MB) da pasta nome_repositorio
      # Quantidade de colaboradores (devs que commitaram pelo menos uma vez no projeto nome_repositorio)
      # Data do primeiro commit do projeto nome_repositorio
      # Data do ultimo commit do projeto nome_repositorio
  try:
    os.environ['REPOSITORIO_INICIAL'] = pasta_n_commit
    qtd_arquivos = "find $REPOSITORIO_INICIAL -type f | wc -l"
    qtd_commits = "cd $REPOSITORIO_INICIAL && git log --oneline | grep -c .""
    tamanho_pasta_mb = "du -hs --block-size=1M $REPOSITORIO_INICIAL | cut -f1"
    qtd_colaboradores_commits = 'cd $REPOSITORIO_INICIAL && git log --pretty=format:"%ae" | sort -u | grep -v "noreply.github.com" | wc -l'
    data_primeiro_commit ="cd $REPOSITORIO_INICIAL && git log --reverse --pretty=format:%ad --date=short | head -1"
    data_ultimo_commit = "cd $REPOSITORIO_INICIAL && git log -1 --pretty=format:%ad --date=short"

    dict_info_repo = {
      'nome':pasta_n_commit,
      'qtd_arquivos':qtd_arquivos,
      'qtd_commits':qtd_commits,
      'tamanho_pasta_mb':tamanho_pasta_mb,
      'qtd_colaboradores_commits':qtd_colaboradores_commits,
      'data_primeiro_commit':data_primeiro_commit,
      'data_ultimo_commit':data_ultimo_commit,
    }

    df_info_repo = pd.DataFrame(dict_info_repo)
  except Exception as e:
    print(f'Erro: {str(e)}')
  return df_info_repo

def gera_df_dados(pasta_n_commit):
  lista_linguagens, lista_files, lista_blank, lista_comment, lista_code = list(), list(), list(), list(), list()
  l_temp = []
  vl_temp = []
  os.environ['REPOSITORIO_INICIAL'] = pasta_n_commit
  try:
    # Detalha os tipos de arquivos que aparecem no repositório do nome_repositorio
    relacao_linguagens = "cd $REPOSITORIO_INICIAL && cloc ."
    linguagens_encontradas = relacao_linguagens[(utilidades.checa_indice_language(relacao_linguagens)+2):]
    for linha in linguagens_encontradas:
      elementos = linha.split(' ')
      novos_elementos = []
      linguagem_encontrada = []
      valores_da_linguagem = []
      for item in elementos:
        if item != '':
          novos_elementos.append(item)
      linguagem_encontrada.append(novos_elementos[:-4])
      valores_da_linguagem.append(novos_elementos[-4:])
      l_temp = l_temp + linguagem_encontrada
      vl_temp = vl_temp + valores_da_linguagem

    l_temp = l_temp[:-3]
    vl_temp = vl_temp[:-3]
    for i,each in enumerate(vl_temp):
      lista_files.append(each[0])
      lista_blank.append(each[1])
      lista_comment.append(each[2])
      lista_code.append(each[3])
  except Exception as e:
    print(f'Erro: {str(e)}')
  try:
    dict_dados_linguagens = {
    'linguagens':l_temp,
    'files':lista_files,
    'blank':lista_blank,
    'comment':lista_comment,
    'code':lista_code
    }
    df_dados_linguagens = pd.DataFrame(dict_dados_linguagens)
    df_dados_linguagens['files'] = df_dados_linguagens['files'].apply(lambda x: int(x))
    df_dados_linguagens['blank'] = df_dados_linguagens['blank'].apply(lambda x: int(x))
    df_dados_linguagens['comment'] = df_dados_linguagens['comment'].apply(lambda x: int(x))
    df_dados_linguagens['code'] = df_dados_linguagens['code'].apply(lambda x: int(x))
  except Exception as e2:
    print(f'Erro: {str(e2)}')

  return df_dados_linguagens

def gera_df_dados_repositorios(df_info_repo, df_info_repo_cf):
  df_repo = None
  try:
    l_cf = df_info_repo_cf.columns.tolist()
    c_c1 = df_info_repo.iloc[0].to_list()
    c_cf = df_info_repo_cf.iloc[0].to_list()

    dict_repo= {
        'descricao':l_cf,
        'dados_c1':c_c1,
        'dados_cf':c_cf
    }
    df_repo = pd.DataFrame(dict_repo)
  except Exception as e:
    print(f'Erro: {str(3)}')
  return df_repo

def gera_df_dados_repositorios2(df_info_repo, df_info_repo_cf):
  df_repo = None
  try:
    l_cf = df_info_repo_cf.columns.tolist()
    c_c1 = df_info_repo.iloc[0].to_list()
    c_cf = df_info_repo_cf.iloc[0].to_list()

    dict_repo= {
        'dados_cf':c_cf
    }
    df_repo = pd.DataFrame(dict_repo)
  except Exception as e:
    print(f'Erro: {str(3)}')
  return df_repo

def gera_df_design_smells(pasta_testes, lista):
  path_file = pasta_testes + '/' + 'designCodeSmells.csv'
  df_ds = pd.read_csv(path_file)
  elemento = pasta_testes,df_ds
  lista.append(elemento)
  return df_ds