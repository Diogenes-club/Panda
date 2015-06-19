//ハイパスフィルタの変数
int const N = 10;
 
int a[N];
 
void setup(){
  for(int i=0; i<N; i++){
    a[i] = 0;
  }
  Serial.begin(9600);
 
  //タッチパネル本体
  pinMode(13,OUTPUT);
  pinMode(12,INPUT);
  //確認用LED
  pinMode(5, OUTPUT);
}
 
void loop(){
  //充電時間用の変数
  a[0] = 0;
  //一度HIGHにして
  digitalWrite(13, HIGH);
 
  //12番ピンがHIGHになるまで(=充電時間)をカウント
  while (digitalRead(12)!=HIGH){
    a[0]++;
  }
  //LOWに戻す
  digitalWrite(13, LOW);
 
  //たまに値がぶれるのでローパスフィルタをかける。
  float ave = 0;
  for(int i=0; i<N; i++){
    ave += a[0];
  }
  ave /= N;
 
  //値チェック
  Serial.println(a[0]);
 
  //この20という数字が大きければ鈍感に、小さければ敏感になります
  if(ave > 100){
    digitalWrite(5, HIGH);
  }else{
    digitalWrite(5, LOW);
  }
 
  //変数をずらす。
  for(int i=0; i<N-1; i++){
    a[i+1] = a[i];
  }
}
