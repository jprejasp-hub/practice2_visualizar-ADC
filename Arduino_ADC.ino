const int PIN_POT = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int adc = analogRead(PIN_POT);
  Serial.println(adc);
  delay(500);
}
