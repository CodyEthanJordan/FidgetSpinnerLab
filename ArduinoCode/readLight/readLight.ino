
int lightPin = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(1000000);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial.write(analogRead(lightPin));
  Serial.println(analogRead(0));
  
}
