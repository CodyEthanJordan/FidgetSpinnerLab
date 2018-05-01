// Code by CodyEthanJordan, part of an introductory lab activity
// feel free to use, full details about lab activity at http://codyethanjordan.com/physics/fidgetSpinnerLab/
// code hosted at https://github.com/CodyEthanJordan/FidgetSpinnerLab

int lightPin = 0;

void setup() {
  Serial.begin(74880); //NOTE: if you change the baud rate here, you will also need to change this value in the Python script to read code
}

void loop() {
  Serial.println(analogRead(0));
  delayMicroseconds(10);
  
}
