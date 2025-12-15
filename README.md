# ⚡ Sistema de Diagnóstico Inteligente (S.I.A.D.E.)

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Plataforma-Raspberry%20Pi%20%7C%20ESP32-red)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-lightgrey)

> **TCC - Engenharia Elétrica - Universidade Católica de Petrópolis (2025)**
> *Monitoramento Elétrico, Automação e Manutenção Preditiva via IoT e IA.*

---

## 📖 Sobre o Projeto

Este repositório contém a arquitetura de software do **Sistema de Diagnóstico Inteligente**, desenvolvido para monitorar variáveis elétricas, registrar eventos, atuar automaticamente sobre cargas e realizar análises preditivas de falhas.

O diferencial do sistema é sua arquitetura híbrida (Online/Offline), utilizando protocolo MQTT para comunicação leve e Inteligência Artificial rodando localmente para antecipar problemas antes que eles ocorram.

---

## 📐 Arquitetura do Sistema

O sistema opera de forma distribuída em três camadas principais:

1.  **Camada de Aquisição e Atuação:** Microcontroladores ESP32.
2.  **Camada de Servidor Central:** Raspberry Pi (Broker, Banco de Dados e IA).
3.  **Camada de Interface:** Software "Analista" (Comando de Voz e Dashboards).

<img width="387" height="248" alt="image" src="https://github.com/user-attachments/assets/8f3997c9-48de-45a1-8bc6-854e48885ccd" />

---

## 🛠️ Módulos do Sistema

### 🔌 1. ESP32 #1 — Aquisição de Dados
Responsável pela leitura contínua ("Sensing Node") e envio via MQTT.
* **Sensores:** Tensão (ZMPT101B), Corrente (SCT-013), Temperatura.
* **Protocolo:** MQTT (JSON).
* **Função:** Coleta dados brutos e envia para o servidor a cada 2 segundos.

### 🔧 2. ESP32 #2 — Atuação
Responsável pela proteção e controle ("Actuator Node").
* **Hardware:** Módulo de 8 Relés.
* **Função:** Recebe comandos de desligamento (automático via IA ou manual via usuário) e registra logs de atuação.

### 🖥️ 3. Raspberry Pi — O Cérebro
Atua como servidor central local (*Edge Computing*).
* **Broker MQTT:** Mosquitto.
* **Banco de Dados:** SQLite (`dados_sensores.db`).
* **IA:** Executa o modelo de predição em tempo real.

### 🤖 4. "O Analista" — Interface Inteligente
Software desktop para interação homem-máquina.
* **Comandos de Voz:** "Qual a tensão média?", "Gerar gráfico".
* **Tecnologias:** `SpeechRecognition`, `gTTS`, `Matplotlib`.
* **Saída:** Áudio e Gráficos gerados automaticamente na pasta compartilhada.

---

## 📊 Inteligência Artificial (Camada Preditiva)

O sistema utiliza um modelo de Machine Learning (**Random Forest Classifier**) treinado para detectar tendências de anomalia (ex: queda gradual de tensão) antes da falha crítica.

<img width="679" height="405" alt="image" src="https://github.com/user-attachments/assets/9ea29b4d-c9fa-4241-930e-cdaa66068b8e" />

> **⚠️ Nota sobre Propriedade Intelectual:**
> Este repositório contém os scripts de treinamento e lógica de inferência para fins acadêmicos. O **dataset original** (14.000 registros) e o arquivo do modelo treinado (`.pkl`) **não estão incluídos** para proteção de propriedade intelectual e desenvolvimento comercial futuro.

---

## ▶️ Como Executar

Siga os passos abaixo para configurar o ambiente e rodar o sistema.

### 1. Preparação do Ambiente (Banco de Dados e Dependências)

Execute os comandos abaixo no terminal para criar a estrutura do banco de dados e instalar as bibliotecas necessárias:

# --- NO RASPBERRY PI (SERVIDOR) ---

# 1. Gerar estrutura do banco de dados (sem dados prévios)
python criar_banco.py

# 2. Instalar Broker MQTT e ferramentas de sistema
sudo apt install mosquitto mosquitto-clients

# 3. Instalar bibliotecas Python do Servidor
pip install paho-mqtt pandas scikit-learn joblib

# --- NO NOTEBOOK (INTERFACE ANALISTA) ---

# 4. Instalar bibliotecas Python da Interface
pip install SpeechRecognition gTTS pydub pygame matplotlib

### 2. Ordem de Execução
Iniciar o Servidor: No Raspberry Pi, execute os scripts de recepção de dados e IA.

Conectar Hardware: Ligue os ESP32 (eles se conectarão automaticamente ao Wi-Fi e ao Broker MQTT).

Iniciar Interface: No notebook, rode o assistente:

python analista_voz.py

📜 Licença e Autoria
Autor: Robson da Cruz Augusto Orientador: Prof. Felipe de Oliveira Baldner

Copyright © 2025. Todos os direitos reservados. O código deste repositório é disponibilizado para fins de avaliação acadêmica. A reprodução comercial ou uso do dataset/modelo proprietário sem autorização é proibida.
