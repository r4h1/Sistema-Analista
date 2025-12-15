
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
DB_PATH = r"\\10.0.0.101\compartilhado\dados_sensores.db"
MODELO_PATH = "modelo_preditivo.pkl"

# ---------------- FUNÇÕES AUXILIARES ----------------
def carregar_dados():
    """
    Lê os dados do banco e retorna como DataFrame.
    """
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT timestamp, tipo_dado, valor FROM historico_dados"
    df = pd.read_sql_query(query, conn, parse_dates=["timestamp"])
    conn.close()
    return df

# SUBSTITUA SUA FUNÇÃO PELA VERSÃO FINAL E CORRIGIDA
def extrair_features(df, janela_min=10):
    """
    Extrai features estatísticas de forma robusta, lidando com duplicatas
    e usando um método de fatiamento mais seguro (máscara booleana).
    """
    # Passo 1: Limpeza e preparação inicial dos dados
    # Garante que não há timestamps duplicados (pegando a média) e ordena.
    df = df.groupby(['timestamp', 'tipo_dado']).valor.mean().reset_index()
    df.sort_values(by="timestamp", inplace=True)
    
    dados_features = []
    janela = timedelta(minutes=janela_min)

    # Passo 2: Iterar por cada tipo de sensor
    for sensor in df["tipo_dado"].unique():
        df_sensor = df[df["tipo_dado"] == sensor]

        if df_sensor.empty or len(df_sensor) < 4:
            continue

        # Passo 3: Criar as janelas deslizantes de forma segura
        inicio = df_sensor["timestamp"].min()
        fim = df_sensor["timestamp"].max()
        
        t_atual = inicio
        while t_atual + janela <= fim:
            # --- CORREÇÃO PRINCIPAL AQUI ---
            # Usando máscara booleana em vez de .loc[] para fatiar.
            # Isso é mais robusto contra índices não-únicos ou irregulares.
            mask = (df_sensor['timestamp'] >= t_atual) & (df_sensor['timestamp'] < t_atual + janela)
            janela_df = df_sensor.loc[mask]
            
            if len(janela_df) > 3:
                valores = janela_df["valor"].values
                media = np.mean(valores)
                desvio = np.std(valores)
                minimo = np.min(valores)
                maximo = np.max(valores)

                x = np.arange(len(valores))
                if len(x) > 1:
                    inclinacao, _ = np.polyfit(x, valores, 1)
                else:
                    inclinacao = 0

                # Lógica de rotulagem
                if sensor == "tensao" and minimo < 110:
                    classe = 1
                elif sensor == "corrente" and maximo > 8:
                    classe = 1
                elif sensor == "temperatura" and maximo > 60:
                    classe = 1
                else:
                    classe = 0

                dados_features.append([sensor, media, desvio, minimo, maximo, inclinacao, classe])
            
            t_atual += timedelta(minutes=1)

    colunas = ["sensor", "media", "desvio", "minimo", "maximo", "inclinacao", "classe"]
    return pd.DataFrame(dados_features, columns=colunas)
# ---------------- TREINAMENTO ----------------
def treinar_modelo():
    df = carregar_dados()
    print(f" {len(df)} registros carregados do banco.")

    dataset = extrair_features(df, janela_min=10)
    print(f" {len(dataset)} janelas de tempo processadas.")

    if dataset.empty:
        print(" Não há dados suficientes para treinar o modelo.")
        return

    X = dataset[["media", "desvio", "minimo", "maximo", "inclinacao"]]
    y = dataset["classe"]

    # Divide treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Avaliação
    acc = modelo.score(X_test, y_test)
    print(f" Acurácia do modelo: {acc * 100:.2f}%")

    # Salvar modelo
    joblib.dump(modelo, MODELO_PATH)
    print(f" Modelo salvo em {MODELO_PATH}")

# ---------------- EXECUÇÃO ----------------
if __name__ == "__main__":
    treinar_modelo()
