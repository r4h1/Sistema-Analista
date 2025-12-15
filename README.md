Sistema de Diagnóstico Inteligente para Monitoramento Elétrico e Manutenção Preditiva

Este repositório contém o código-fonte do Sistema de Diagnóstico Inteligente (SDI) desenvolvido como Trabalho de Conclusão de Curso (TCC).
O sistema tem como objetivo o monitoramento de variáveis elétricas, registro de eventos, atuação automatizada sobre cargas e análise preditiva de falhas, utilizando tecnologias de IoT, banco de dados local e Inteligência Artificial.

📐 Arquitetura Geral do Sistema

O sistema foi projetado com uma arquitetura distribuída e modular, composta por três camadas principais:

Camada de Aquisição e Atuação (ESP32)

Camada de Servidor Central (Raspberry Pi)

Camada de Interface e Consulta (Analista)

A comunicação entre os módulos ocorre predominantemente via MQTT, garantindo baixo consumo de rede e funcionamento em ambientes com conectividade limitada.

🔌 ESP32 #1 — Aquisição de Dados Elétricos

O ESP32 #1 é responsável pela leitura contínua das variáveis elétricas, incluindo:

Tensão (V)

Corrente (A)

Temperatura (°C)

Funções principais:

Aquisição periódica dos sensores

Publicação dos dados via MQTT

Envio das leituras para armazenamento no servidor central

Dados armazenados:

Os dados são enviados ao Raspberry Pi, que os insere na tabela historico_dados do banco SQLite, contendo:

Timestamp

Identificação do sensor

Tipo de dado

Valor medido

🔧 ESP32 #2 — Atuação e Registro de Eventos

O ESP32 #2 é responsável pela atuação sobre cargas elétricas, utilizando um módulo de 8 relés.

Funções principais:

Recebimento de comandos via MQTT

Acionamento e desligamento de relés

Geração de logs de eventos do sistema

Logs gerados:

Os eventos são registrados no banco de dados do Raspberry Pi na tabela logs_eventos, incluindo:

Timestamp

Tipo de evento (ex: atuação automática)

Descrição textual

⚠️ Não são gerados gráficos para o ESP32 #2, pois sua função é exclusivamente atuar e registrar eventos.

🖥️ Raspberry Pi — Servidor Central

O Raspberry Pi atua como núcleo do sistema, desempenhando os seguintes papéis:

Funções principais:

Broker MQTT (Mosquitto)

Armazenamento local dos dados (SQLite)

Compartilhamento de arquivos via rede (Samba)

Execução da camada de análise preditiva

Banco de Dados

SQLite

Arquivo: dados_sensores.db

Tabelas principais:

historico_dados

logs_eventos

O uso de SQLite garante simplicidade, baixo consumo de recursos e independência de servidores externos.

🤖 Analista — Interface Inteligente de Consulta

O Analista é um assistente executado no notebook do usuário, responsável por:

Consultas ao banco de dados do Raspberry Pi

Geração de gráficos automáticos (PNG)

Interação por comandos de voz ou texto

Respostas em linguagem natural

Tecnologias utilizadas:

SpeechRecognition (voz online)

gTTS + pydub + pygame (síntese de fala)

SQLite (consultas remotas)

Matplotlib (geração de gráficos)

Exemplos de comandos:

Analista tensão média última hora

Analista gerar gráfico de tensão

Analista eventos

Analista atuação do sistema

Os gráficos são salvos automaticamente na pasta compartilhada do Raspberry Pi.

📊 Camada Preditiva (Inteligência Artificial)

O sistema implementa uma camada de manutenção preditiva, utilizando:

Random Forest Classifier

Biblioteca Scikit-learn

Objetivo:

Detectar tendências de falha a partir do comportamento estatístico da tensão elétrica ao longo do tempo.

Processo:

Extração de janelas temporais

Cálculo de features estatísticas:

Média

Desvio padrão

Mínimo

Máximo

Inclinação (tendência)

Classificação do estado do sistema:

Normal

Alerta Preditivo

O modelo treinado é salvo em arquivo .pkl e pode ser integrado ao sistema principal.

▶️ Como Executar (Resumo)
Raspberry Pi
sudo apt update
sudo apt install mosquitto mosquitto-clients python3-pip
pip install sqlite3 pandas scikit-learn joblib


Iniciar o broker MQTT

Executar o script de recepção e armazenamento de dados

(Opcional) Executar o simulador de dados

Notebook (Analista)
pip install speechrecognition gtts pydub pygame matplotlib


Ajustar o caminho do banco de dados compartilhado

Executar o script do Analista

Utilizar comandos de voz ou texto

📂 Organização do Repositório (Sugestão)
├── esp32_1_aquisicao/
├── esp32_2_reles/
├── raspberry_servidor/
├── analista/
├── machine_learning/
├── docs/
└── README.md

📌 Observações Importantes

O sistema foi testado em ambiente controlado com dados simulados e reais.

A arquitetura permite funcionamento offline, sem dependência de nuvem.

O projeto foi desenvolvido com foco acadêmico e didático.

📜 Licença

"All Rights Reserved" (Todos os direitos reservados).
