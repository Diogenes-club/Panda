int analogPinX = A3;
int analogPinY = A4;
int analogPinZ = A5;
int valx,valy,valz;

void setup() {
      pinMode(analogPinX, INPUT);
      pinMode(analogPinY, INPUT);
      pinMode(analogPinZ, INPUT);
      Serial.begin(9600);	// 9600bpsでポートを開く
}

void loop() {
    valx = analogRead(analogPinX);
    valy = analogRead(analogPinY);
    valz = analogRead(analogPinZ);
    
    char valstr[32];
    sprintf(valstr, "%d,%d,%d", valx, valy, valz);
    Serial.println(valstr);
    
    delay(1000);
}
