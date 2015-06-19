#include <Servo.h> 
int analogPin = A0;
int servoPin = 9;
int ledPin = 13;
int val = 0;
Servo myservo;
String strdeg = "";
    
void setup() {

    myservo.attach(servoPin);
    pinMode(analogPin, INPUT);
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);	// 9600bpsでポートを開く
}

void loop() {
    val = analogRead(analogPin);
    char valstr[32];
    sprintf(valstr, "%d", val);
    Serial.println(valstr);

    while (Serial.available() > 0) {
      char c = Serial.read();
      strdeg += c;
    }
    String senddeg = strdeg;
    strdeg = "";
    if (senddeg != "") {
      Serial.println(senddeg);
      myservo.write(senddeg.toInt());
      if (senddeg.toInt() > 100) {
        digitalWrite(ledPin, HIGH);
      } else {
        digitalWrite(ledPin, LOW);
      }
    }
    delay(1000);
    
}
