#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <DHT.h>


unsigned long sendDataPrevMillis = 0;
unsigned long PrevMillis = millis();

//5 dòng tiếp theo là khai báo chân module L298N
int IN1 = D0;
int IN2 = D1;
int IN3 = D3;
int IN4 = D4;
int enA = D2;
int enB = D6;

//3 dòng tiếp theo khai báo chân của cảm biến nhiệt độ độ ẩm
int DHTPIN = D5;       //Đọc dữ liệu từ DHT11
int DHTTYPE = DHT11;  //Khai báo loại cảm biến, có 2 loại là DHT11 và DHT22
DHT dht(DHTPIN, DHTTYPE);


/* 1. Nhập tên và mật khẩu wifi mà ESP32_Cam sẽ kết nối đến*/
#define WIFI_SSID " "
#define WIFI_PASSWORD " "

/* 2. Nhập Real Time Database URL */
#define DATABASE_URL "https://pbl5-arduino-default-rtdb.firebaseio.com"

/* 3. Nhập Secret_key */
#define SECRET_KEY "6oFzmOzrZbOSMqOiFm56QddahtwXM7FuzOdsPprC"

FirebaseData fbdo;


void setup() {  
  
  Serial.begin(9600);
  dht.begin();// Khởi động cảm biến
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  
   WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
   while (WiFi.status() != WL_CONNECTED)
    {
      Serial.print(".");
      delay(300);
    }
   //Kết nối với Firebase
   Firebase.begin(DATABASE_URL, SECRET_KEY);
}

void loop() {
  String account = "trquan17"; //tên tài khoản user khi đăng nhập vào web 
  int doam = dht.readHumidity();    //Đọc độ ẩm
  int nhietdo = dht.readTemperature(); //Đọc nhiệt độ
  if (Firebase.ready() && (millis() - sendDataPrevMillis > 3000 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();
    Firebase.setInt(fbdo,"users/" + account + "/info/temp",nhietdo);// gửi nhiệt độ lên Firebase
    Firebase.setInt(fbdo,"users/" + account + "/info/hum",doam);// gửi độ ẩm lên Firebase
  }


  //biến chế độ
  Firebase.getString(fbdo,"users/" + account + "/control/auto");
  String chedo =  fbdo.stringData();

  //biến cảm xúc
  Firebase.getString(fbdo,"users/" +account + "/info/emoji");
  String camxuc =  fbdo.stringData();

  //biến điều khiển bật/tắt nôi 
  Firebase.getString(fbdo,"users/" +account + "/control/status_cradle");
  String cradle =  fbdo.stringData();

  //biến điều khiển bật/tắt quạt
  Firebase.getString(fbdo,"users/" + account + "/control/status_fan");
  String fan =  fbdo.stringData();

     
////  điều chỉnh tốc độ lắc nôi
//   int  giatri = analogRead(A0);
//   int tocdo = map(giatri,0,1024,0,255);
//   Serial.print("Speed: ");
//   Serial.println(tocdo);

    //dòng tiếp theo tùy theo chế độ và cảm xúc mà cho lắc nôi hay ko 
  XuLiNoi(chedo,camxuc,cradle,220);
  
  // dòng tiếp theo tùy theo chế độ hoặc nhiệt độ mà cho bật tắt quạt
  XuLiQuat(chedo,nhietdo,fan);
  
}
void LacNoi(int tocdo)
{
  Serial.print("băm xung: ");
  Serial.println(tocdo);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(enA, tocdo);
}

void DungNoi()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}
void BatQuat()
{
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(enB, 250);
}

void TatQuat()
{
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
void XuLiQuat(String chedo,float nhietdo,String fan)
{ 
   const char* chedo1 = chedo.c_str();
   const char* fan1 = fan.c_str();

  if(strcmp(chedo1,"ON") == 0)
  {
//     Serial.println("chế độ quạt tự động");
     if( nhietdo > 33)
      { 
        BatQuat();
      }
      else if(nhietdo <= 33)
      {
        TatQuat();
      }
   }
  else if(strcmp(chedo1,"OFF") == 0) 
    {
//      Serial.println("chế độ quạt thủ công");
      if(strcmp(fan1,"ON") == 0)
      {
        BatQuat();
      }
      else if(strcmp(fan1,"OFF") == 0) 
      {
        TatQuat();
      }
    }
}

void XuLiNoi(String chedo,String camxuc,String cradle,int tocdo)
{
  const char* chedo1 = chedo.c_str();
  const char* camxuc1 = camxuc.c_str();
  const char* cradle1 = cradle.c_str();
 
  if(strcmp(chedo1,"OFF") == 0) 
  {
//    Serial.println("chế độ nôi thủ công");
    if(strcmp(cradle1,"ON") == 0)
    {
//      Serial.println("Lắc nôi");
      LacNoi(tocdo);
    }
    else if(strcmp(cradle1,"OFF") == 0) 
    {
//       Serial.println("Dừng nôi");
      DungNoi();
    }
 }
 else if(strcmp(chedo1,"ON") == 0)
 {
//  Serial.println("chế độ nôi tự động");
    if(strcmp(camxuc1,"Khác") == 0)
    {
      Serial.println("em bé không có gì bất thường");
      DungNoi();
    }
    else if(strcmp(camxuc1, "Khóc") == 0)
    {
      Serial.println("em bé đang khóc, lắc nôi để dỗ ");
      LacNoi(tocdo);
    }
    else if(strcmp(camxuc1, "Ngủ") == 0)
    {
      Serial.println("em bé đang buồn ngủ, ru đời đi nhé");
      LacNoi(tocdo);
    }
    else
    {
      DungNoi();
    }
  }
}
