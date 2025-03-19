#include <DHT.h>

#define DHTPIN D4  // GPIO2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int gasSensorPin = A0;  // MQ2 sensor connected to A0
const int ozoneSensorPin = D3; // Ozone sensor mapped as digital threshold reading

void setup() {
    Serial.begin(115200);
    dht.begin();
}

void loop() {
    // Read MQ2 Gas Sensor
    int gasValue = analogRead(gasSensorPin);
    
    // Read Ozone Sensor (Approximated as Digital)
    int ozoneValue = digitalRead(ozoneSensorPin); // 0 or 1 (approximate threshold)

    // Read DHT11 Sensor
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Derived Parameters:
    float heatIndex = dht.computeHeatIndex(temperature, humidity, false);
    float airQualityIndex = map(gasValue, 0, 1024, 0, 500); // Scale to AQI range

    // Print values to Serial Monitor
    Serial.println("----- Sensor Readings -----");
    Serial.print("MQ2 Gas Sensor (CO/LPG/Smoke) Value: ");
    Serial.println(gasValue);

    Serial.print("Ozone Sensor (Threshold-based) Value: ");
    Serial.println(ozoneValue == HIGH ? "High" : "Low"); // Approximate reading

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println("°C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println("%");

    Serial.print("Heat Index: ");
    Serial.print(heatIndex);
    Serial.println("°C");

    Serial.print("Air Quality Index (Approx): ");
    Serial.println(airQualityIndex);

    Serial.println("--------------------------");
    
    delay(2000);  // Wait 2 seconds before next reading
}
