#include <Servo.h> 
int analogPin = A0;
int servoPin1 = 8;
int servoPin2 = 9;
int ledPin = 13;
int val = 0;
Servo myservo1;
Servo myservo2;
String strdeg = "";
    
void setup() {

    myservo1.attach(servoPin1);
    myservo2.attach(servoPin2);
    pinMode(analogPin, INPUT);
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);	// 9600bpsでポートを開く
}

void loop() {
        myservo1.write(90);
        myservo2.write(90);
            delay(500);
        myservo1.write(0);
        myservo2.write(90);
            delay(500);
        myservo1.write(180);
        myservo2.write(90);
            delay(500);  
        myservo1.write(0);
        myservo2.write(90);
            delay(500);
        myservo1.write(90);
        myservo2.write(90);
            myservo1.detach();
            myservo2.detach();
            delay(500);  
        myservo1.write(90);
        myservo2.write(30);
            delay(1000);    
        myservo1.write(90);
        myservo2.write(120);
            delay(1000);            
        myservo1.write(90);
        myservo2.write(90);
            delay(1000);
        myservo1.write(90);
        myservo2.write(90);
            delay(100000000);            
/*    val = analogRead(analogPin);
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
    */

    
}
