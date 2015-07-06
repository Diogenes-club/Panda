#include <Servo.h>
#include <string.h>
#include <stdio.h>

int servoPin1 = 8;
int servoPin2 = 9;
Servo myservo1;
Servo myservo2;

int gyroPinX = A3;
int gyroPinY = A4;
int gyroPinZ = A5;
int valX,valY,valZ;

int touchPinA1 = 13;
int touchPinA2 = 12;

unsigned long time0, time1;
void setup() {
    pinMode(gyroPinX, INPUT);
    pinMode(gyroPinY, INPUT);
    pinMode(gyroPinZ, INPUT);

    pinMode(touchPinA1, OUTPUT);
    pinMode(touchPinA2, INPUT);

    Serial.begin(9600);
    time0 = millis();
}

void uplink_func() {
        String strSer = "";
        while (Serial.available() > 0) {
            char c = Serial.read();
            if (c == '\n') break;
            strSer += c;
        }

        char opName[20];
        int opValue;
        sscanf(strSer.c_str(), "%s:%d", opName, &opValue);
        if (strcmp(opName, "pan") == 0 && opValue >= 0 && opValue <= 180) {
            myservo1.attach(servoPin1);
            myservo1.write(opValue);
        } else if (strcmp(opName, "tilt") == 0 && opValue >= 0 && opValue <= 180) {
            myservo2.attach(servoPin2);
            myservo2.write(opValue);
        } else if (strcmp(opName, "nod") == 0 && opValue < 5) {
            for (int i = 0; i < opValue; i++) {
                myservo1.attach(servoPin1);
                myservo2.attach(servoPin2);
                myservo1.write(90);
                myservo2.write(30);
                delay(500);
                myservo2.write(120);
                delay(500);
            }
            myservo2.write(90);
        } else if (strcmp(opName, "shake") == 0 && opValue < 5) {
            for (int i = 0; i < opValue; i++) {
                myservo1.attach(servoPin1);
                myservo2.attach(servoPin2);
                myservo1.write(0);
                myservo2.write(90);
                delay(500);
                myservo1.write(180);
                delay(500);
            }
            myservo2.write(90);
        } else if (strcmp(opName, "detach") == 0) {
            myservo1.detach();
            myservo2.detach();
        }
}

void downlink_func() {
    valX = analogRead(gyroPinX);
    valY = analogRead(gyroPinY);
    valZ = analogRead(gyroPinZ);

    char charStr[32];
    sprintf(charStr, "gyro:%d,%d,%d", valX, valY, valZ);
    Serial.println(charStr);

    int rechargeTime = 0;
    digitalWrite(touchPinA1, HIGH);
    while (digitalRead(touchPinA2) != HIGH) {
        rechargeTime++;
    }
    
    char charStr2[32];
    sprintf(charStr2, "sensor1:%d", rechargeTime);
    Serial.println(charStr2);
}

void loop() {
  downlink_func();
  time1 = millis();
  if (time1 - time0 > 1000) {
    uplink_func();
    time0 = time1;
  }
}
