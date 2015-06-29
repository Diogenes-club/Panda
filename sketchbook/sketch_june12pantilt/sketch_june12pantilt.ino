#include <Servo.h>
#include <string.h>
#include <pthread.h>

int servoPin1 = 8;
int servoPin2 = 9;
Servo myservo1;
Servo myservo2;

void setup() {
    pthread_t thread;
    pthread_create(&thread, NULL, loop_thread, NULL);
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
        if (strcmp(opName, "pan") == 0) {
            myservo1.attach(servoPin1);
            myservo1.write(opValue);
        } else if (strcmp(opName, "tilt") == 0) {
            myservo2.attach(servoPin2);
            myservo2.write(opValue);
        } else if (strcmp(opName, "nod") == 0) {
            for (int i = 0; i < opValue; i++) {
                myservo1.attach(servoPin1);
                myservo2.attach(servoPin2);
                myservo1.write(90);
                myservo2.write(30);
                delay(1000);
                myservo2.write(120);
                delay(1000);
            }
            myservo2.write(90);
        } else if (strcmp(opName, "detach") == 0) {
            myservo1.detach();
            myservo2.detach();
        }
        return NULL;
    }
}

void loop() {
}
