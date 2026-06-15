import basedosdados as bd
import pandas as pd
import os

# ID do seu projeto Google Cloud
billing_id = "trabalho-econometria-491612" 

query = """
WITH 
dicionario_tipo_vinculo AS (
    SELECT chave AS chave_tipo_vinculo, valor AS descricao_tipo_vinculo
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'tipo_vinculo' AND id_tabela = 'microdados_vinculos'
),
dicionario_vinculo_ativo_3112 AS (
    SELECT chave AS chave_vinculo_ativo_3112, valor AS descricao_vinculo_ativo_3112
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'vinculo_ativo_3112' AND id_tabela = 'microdados_vinculos'
),
dicionario_tipo_admissao AS (
    SELECT chave AS chave_tipo_admissao, valor AS descricao_tipo_admissao
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'tipo_admissao' AND id_tabela = 'microdados_vinculos'
),
dicionario_motivo_desligamento AS (
    SELECT chave AS chave_motivo_desligamento, valor AS descricao_motivo_desligamento
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'motivo_desligamento' AND id_tabela = 'microdados_vinculos'
),
dicionario_indicador_trabalho_parcial AS (
    SELECT chave AS chave_indicador_trabalho_parcial, valor AS descricao_indicador_trabalho_parcial
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'indicador_trabalho_parcial' AND id_tabela = 'microdados_vinculos'
),
dicionario_indicador_trabalho_intermitente AS (
    SELECT chave AS chave_indicador_trabalho_intermitente, valor AS descricao_indicador_trabalho_intermitente
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'indicador_trabalho_intermitente' AND id_tabela = 'microdados_vinculos'
),
dicionario_grau_instrucao_apos_2005 AS (
    SELECT chave AS chave_grau_instrucao_apos_2005, valor AS descricao_grau_instrucao_apos_2005
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'grau_instrucao_apos_2005' AND id_tabela = 'microdados_vinculos'
),
dicionario_sexo AS (
    SELECT chave AS chave_sexo, valor AS descricao_sexo
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'sexo' AND id_tabela = 'microdados_vinculos'
),
dicionario_raca_cor AS (
    SELECT chave AS chave_raca_cor, valor AS descricao_raca_cor
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'raca_cor' AND id_tabela = 'microdados_vinculos'
),
dicionario_tamanho_estabelecimento AS (
    SELECT chave AS chave_tamanho_estabelecimento, valor AS descricao_tamanho_estabelecimento
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'tamanho_estabelecimento' AND id_tabela = 'microdados_vinculos'
),
dicionario_indicador_simples AS (
    SELECT chave AS chave_indicador_simples, valor AS descricao_indicador_simples
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE nome_coluna = 'indicador_simples' AND id_tabela = 'microdados_vinculos'
)
SELECT
    dados.ano as ano,
    dados.sigla_uf AS sigla_uf,
    diretorio_sigla_uf.nome AS sigla_uf_nome,
    diretorio_id_municipio.nome AS id_municipio_nome,
    descricao_tipo_vinculo AS tipo_vinculo,
    descricao_vinculo_ativo_3112 AS vinculo_ativo_3112,
    descricao_tipo_admissao AS tipo_admissao,
    dados.mes_admissao as mes_admissao,
    dados.mes_desligamento as mes_desligamento,
    descricao_motivo_desligamento AS motivo_desligamento,
    dados.tempo_emprego as tempo_emprego,
    dados.quantidade_horas_contratadas as quantidade_horas_contratadas,
    descricao_indicador_trabalho_parcial AS indicador_trabalho_parcial,
    descricao_indicador_trabalho_intermitente AS indicador_trabalho_intermitente,
    dados.valor_remuneracao_media as valor_remuneracao_media,
    diretorio_cnae_2_subclasse.descricao_secao AS cnae_2_subclasse_descricao_secao,
    dados.idade as idade,
    descricao_grau_instrucao_apos_2005 AS grau_instrucao_apos_2005,
    descricao_sexo AS sexo,
    descricao_raca_cor AS raca_cor,
    descricao_tamanho_estabelecimento AS tamanho_estabelecimento,
    diretorio_natureza_juridica.descricao AS natureza_juridica_descricao,
    descricao_indicador_simples AS indicador_simples
FROM `basedosdados.br_me_rais.microdados_vinculos` AS dados
LEFT JOIN (SELECT DISTINCT sigla, nome FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
    ON dados.sigla_uf = diretorio_sigla_uf.sigla
LEFT JOIN (SELECT DISTINCT id_municipio, nome FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio
    ON dados.id_municipio = diretorio_id_municipio.id_municipio
LEFT JOIN (SELECT DISTINCT subclasse, descricao_secao FROM `basedosdados.br_bd_diretorios_brasil.cnae_2`) AS diretorio_cnae_2_subclasse
    ON dados.cnae_2_subclasse = diretorio_cnae_2_subclasse.subclasse
LEFT JOIN (SELECT DISTINCT id_natureza_juridica, descricao FROM `basedosdados.br_bd_diretorios_brasil.natureza_juridica`) AS diretorio_natureza_juridica
    ON dados.natureza_juridica = diretorio_natureza_juridica.id_natureza_juridica
LEFT JOIN `dicionario_tipo_vinculo` ON dados.tipo_vinculo = chave_tipo_vinculo
LEFT JOIN `dicionario_vinculo_ativo_3112` ON dados.vinculo_ativo_3112 = chave_vinculo_ativo_3112
LEFT JOIN `dicionario_tipo_admissao` ON dados.tipo_admissao = chave_tipo_admissao
LEFT JOIN `dicionario_motivo_desligamento` ON dados.motivo_desligamento = chave_motivo_desligamento
LEFT JOIN `dicionario_indicador_trabalho_parcial` ON dados.indicador_trabalho_parcial = chave_indicador_trabalho_parcial
LEFT JOIN `dicionario_indicador_trabalho_intermitente` ON dados.indicador_trabalho_intermitente = chave_indicador_trabalho_intermitente
LEFT JOIN `dicionario_grau_instrucao_apos_2005` ON dados.grau_instrucao_apos_2005 = chave_grau_instrucao_apos_2005
LEFT JOIN `dicionario_sexo` ON dados.sexo = chave_sexo
LEFT JOIN `dicionario_raca_cor` ON dados.raca_cor = chave_raca_cor
LEFT JOIN `dicionario_tamanho_estabelecimento` ON dados.tamanho_estabelecimento = chave_tamanho_estabelecimento
LEFT JOIN `dicionario_indicador_simples` ON dados.indicador_simples = chave_indicador_simples

WHERE 
    dados.ano = 2024 
    AND dados.sigla_uf = 'SC'
    -- Filtro mais flexível para pegar Industria de Transformação
    AND UPPER(diretorio_cnae_2_subclasse.descricao_secao) LIKE '%INDÚSTRIA%TRANSFORMAÇÃO%'
"""

print("Iniciando download dos dados de 2024...")
df = bd.read_sql(query=query, billing_project_id=billing_id)

if not df.empty:
    print(f"Sucesso! Foram encontradas {len(df)} linhas.")
    df.to_csv("dados_rais_sc_industria_2024.csv", index=False, sep=';', encoding='utf-8-sig')
    print("Arquivo 'dados_rais_sc_industria_2024.csv' gerado.")
else:
    print("O filtro de indústria não retornou dados para 2024.")
    print("Tentando listar os setores disponíveis em 2024 para conferência...")
    
    # Query auxiliar só para ver o que tem no banco
    check_query = "SELECT DISTINCT descricao_secao FROM `basedosdados.br_bd_diretorios_brasil.cnae_2`"
    setores = bd.read_sql(query=check_query, billing_project_id=billing_id)
    print("Setores cadastrados no diretório:")
    print(setores)

    # Mostra as 5 primeiras linhas
print("\n--- PRIMEIRAS LINHAS ---")
print(df.head())