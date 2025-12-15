#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // Usaremos JSON para enviar os dados
#include <ZMPT101B.h>
#include <DHT.h>

// --- CONFIGURAÇÕES ---
const char* ssid = "Diagnostico-IoT";
const char* password = "diagnostico123";
const char* mqtt_server = "10.0.0.101"; // IP do Raspberry Pi

#define SENSITIVITY 500.0f
#define DHTPIN 27
#define DHTTYPE DHT11
#define CURRENT_SENSOR_PIN 33
#define VOLTAGE_SENSOR_PIN 32

// !! CONFIRMAR SE ESTE É O VALOR DO SEU RESISTOR DE CARGA !!
#define BURDEN_RESISTOR_VALUE 33.0
// O SCT-013 100A:50mA tem uma relação de espiras de 2000:1 (100A / 0.050A)
#define SENSOR_TURNS_RATIO 2000.0

// Variável global para guardar o offset medido (ponto de bias DC)
double adc_offset = 0.0;

// Tópico MQTT para publicar os dados
const char* topico_dados = "esp/esp1/dados";

WiFiClient espClient;
PubSubClient client(espClient);
ZMPT101B voltageSensor(VOLTAGE_SENSOR_PIN, 60.0);
DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  delay(10);
  Serial.print("\nConectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado! IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando ao MQTT...");
    // Gera um Client ID único para evitar conflitos
    String clientId = "ESP32_Sensor_";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("conectado");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

// Le e calcula tensão
double readCurrentRMS(int pin) {
  // Amostra os dados por vários ciclos da onda de 60Hz para ter uma boa média
  long tempo_inicio = millis();
  double soma_quadrados = 0;
  int num_amostras = 0;

  while (millis() - tempo_inicio < 100) { // Amostra por 100ms (6 ciclos de 60Hz)
    // Lê o valor do ADC e remove o offset DC medido na calibração
    double leitura_adc_sem_offset = analogRead(pin) - adc_offset;
    soma_quadrados += leitura_adc_sem_offset * leitura_adc_sem_offset;
    num_amostras++;
  }

  if (num_amostras == 0) return 0.0;

  // Calcula a tensão RMS no pino do ADC
  double tensao_adc_rms = sqrt(soma_quadrados / num_amostras);

  // Converte o valor do ADC (0-4095) de volta para a tensão real (0-3.3V)
  double tensao_rms_no_pino = tensao_adc_rms * (3.3 / 4095.0);

  // Calcula a corrente RMS que passa pelo resistor de carga (I = V/R)
  double corrente_secundaria_rms = tensao_rms_no_pino / BURDEN_RESISTOR_VALUE;

  // Aplica a relação de espiras do sensor para encontrar a corrente primária
  double corrente_primaria_rms = corrente_secundaria_rms * SENSOR_TURNS_RATIO;
  
  return corrente_primaria_rms;
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  voltageSensor.setSensitivity(SENSITIVITY);

  // --- NOVO: Bloco de Calibração do Sensor de Corrente ---
  Serial.println("Iniciando calibração do sensor de corrente SCT-013.");
  Serial.println("Garanta que não há corrente passando pelo sensor.");
  long soma_offset = 0;
  int num_leituras_calibracao = 1000;
  for (int i = 0; i < num_leituras_calibracao; i++) {
    soma_offset += analogRead(CURRENT_SENSOR_PIN);
    delay(1);
  }
  adc_offset = (double)soma_offset / num_leituras_calibracao;
  Serial.print("Calibração concluída. Offset ADC medido: ");
  Serial.println(adc_offset);
  // --- FIM DO BLOCO DE CALIBRAÇÃO ---

  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Leitura dos sensores
  float tensao = voltageSensor.getRmsVoltage();
  float temperatura = dht.readTemperature();
  float corrente = readCurrentRMS(CURRENT_SENSOR_PIN);

  // Checagem para leituras inválidas do DHT
  if (isnan(temperatura)) {
    Serial.println("Falha na leitura do sensor DHT!");
    delay(2000);
    return;
  }

  // Cria um documento JSON para enviar todos os dados de uma vez
  StaticJsonDocument<200> doc;
  doc["tensao"] = tensao;
  doc["corrente"] = corrente;
  doc["temperatura"] = temperatura;

  // Serializa o JSON para uma string
  char buffer[200];
  serializeJson(doc, buffer);

  // Publica a string JSON no tópico MQTT
  client.publish(topico_dados, buffer);

  Serial.println("-------------------------------");
  Serial.print("Dados enviados via MQTT: ");
  Serial.println(buffer);
  Serial.println("-------------------------------");

  delay(5000);
}
