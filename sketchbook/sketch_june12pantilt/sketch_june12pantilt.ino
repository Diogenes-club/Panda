#include <Servo.h>
#include <string.h>
#include <pthread.h>

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

void setup() {
    pthread_t thread;
    pthread_create(&thread, NULL, loop_thread, NULL);

    pinMode(gyroPinX, INPUT);
    pinMode(gyroPinY, INPUT);
    pinMode(gyroPinZ, INPUT);

    pinMode(touchPin1, OUTPUT);
    pinMode(touchPin2, INPUT);

    Serial.begin(9600);    // 9600bpsでポートを開く
}

void *loop_thread(void *param) {
    while(1) {
        /* シリアル通信から1行とりだす */
        String strSer = "";
        while (Serial.available() > 0) {
            char c = Serial.read();
            if (c == '\n') break;
            strSer += c;
        }

        /* シリアル命令を解析 */

        char opName[20];
        int opValue;
        sscanf(strSer.data(), "%s:%d", opName, &opValue);
        if (strcmp(opName, "pan") == 0) {  //  パン
            myservo1.attach(servoPin1);
            myservo1.write(opValue);
        } else if (strcmp(opName, "tilt") == 0) {  //  チルト
            myservo2.attach(servoPin2);
            myservo2.write(opValue);
        } else if (strcmp(opName, "nod") == 0) {  //  うなずく
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
        } else if (strcmp(opName, "shake") == 0) {  //  いやいや
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
        } else if (strcmp(opName, "detach") == 0) {  //  完全停止
            myservo1.detach();
            myservo2.detach();
        }
        return NULL;
    }
}

void loop() {
    /* ジャイロセンサーの値 */
    valX = analogRead(gyroPinX);
    valY = analogRead(gyroPinY);
    valZ = analogRead(gyroPinZ);

    char charStr[32];
    sprintf(charStr, "%d,%d,%d", valX, valY, valZ);
    Serial.println(charStr);

    /* タッチセンサーの値 */
    int rechargeTime = 0;
    digitalWrite(touchPinA1, HIGH);
    while (digitalRead(touchPinA2) != HIGH) {
        rechargeTime++;
    }
    Serial.println("sensor1:" + to_string(rechargeTime));
}
