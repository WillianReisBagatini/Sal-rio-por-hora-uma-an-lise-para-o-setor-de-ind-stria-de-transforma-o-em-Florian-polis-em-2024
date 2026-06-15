import pandas as pd
import numpy as np

# --- 1. CARREGAMENTO ---
nome_arquivo = "dados_rais_sc_industria_2024.csv"
print(f"Lendo base de dados: {nome_arquivo}...")
df = pd.read_csv(nome_arquivo, sep=';', encoding='utf-8-sig')

# --- 2. FILTROS BÁSICOS (Geografia, Vínculo e Consistência) ---
print("Aplicando filtros de Florianópolis e CLT...")
df = df[df['id_municipio_nome'].astype(str).str.strip() == 'Florianópolis']

vinculos_desejados = ['CLT U/PJ IND', 'CLT U/PJ DET']
df = df[df['tipo_vinculo'].str.strip().isin(vinculos_desejados)]

df = df[(df['quantidade_horas_contratadas'] >= 40) & 
        (df['quantidade_horas_contratadas'] <= 44) & 
        (df['valor_remuneracao_media'] > 0)]

# --- 3. CRIAÇÃO DAS VARIÁVEIS ---
df['salario_hora'] = df['valor_remuneracao_media'] / (df['quantidade_horas_contratadas'] * 4)
df['ln_salario_hora'] = np.log(df['salario_hora'])

# --- 4. FILTRO DE OUTLIERS COM 1,5 DESVIO PADRÃO ---
# Aqui o código calcula a média e o desvio da base filtrada
media_ln = df['ln_salario_hora'].mean()
dp_ln = df['ln_salario_hora'].std()

# Definimos os limites usando 1.5 em vez de 2.0
limite_inferior = media_ln - (1.5 * dp_ln)
limite_superior = media_ln + (1.5 * dp_ln)

print(f"Limpando outliers usando 1.5 DP (Intervalo: {limite_inferior:.4f} a {limite_superior:.4f})")
df_filtrado = df[(df['ln_salario_hora'] >= limite_inferior) & (df['ln_salario_hora'] <= limite_superior)]

# --- 5. AMOSTRAGEM ALEATÓRIA ---
print("Gerando amostra aleatória de 200 observações...")
if len(df_filtrado) >= 200:
    df_amostra = df_filtrado.sample(n=200, random_state=42)
else:
    print(f"Aviso: A base resultante possui apenas {len(df_filtrado)} registros.")
    df_amostra = df_filtrado.copy()

# --- 6. EXPORTAÇÃO PARA CSV ---
nome_saida_csv = "amostra_15dp_floripa.csv"
df_amostra.to_csv(nome_saida_csv, index=False, sep=';', encoding='utf-8-sig')

print(f"Arquivo CSV gerado com sucesso: {nome_saida_csv}")
print(f"Total de observações na amostra: {len(df_amostra)}")