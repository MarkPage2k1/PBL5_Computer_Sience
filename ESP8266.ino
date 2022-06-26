#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <DHT.h>
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

unsigned long sendDataPrevMillis = 0;
unsigned long PrevMillis = millis();

//3 dòng tiếp theo khai báo chân của cảm biến nhiệt độ độ ẩm
int DHTPIN = D5;       //Đọc dữ liệu từ DHT11
int DHTTYPE = DHT11;  //Khai báo loại cảm biến, có 2 loại là DHT11 và DHT22
DHT dht(DHTPIN, DHTTYPE);

//khai báo chân dfplayer mini mp3
SoftwareSerial mySoftwareSerial(D1, D2); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

/* 1. Nhập tên và mật khẩu wifi mà ESP32_Cam sẽ kết nối đến*/
#define WIFI_SSID " "
#define WIFI_PASSWORD " "

/* 2. Nhập Real Time Database URL */
#define DATABASE_URL "https://pbl5-arduino-default-rtdb.firebaseio.com"

#define SECRET_KEY "6oFzmOzrZbOSMqOiFm56QddahtwXM7FuzOdsPprC"

FirebaseData fbdo;


void setup() {  
  
  Serial.begin(9600);
  mySoftwareSerial.begin(9600);
   dht.begin();// Khởi động cảm biến

 
   WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
   while (WiFi.status() != WL_CONNECTED)
    {
      Serial.print(".");
      delay(300);
    }
   //Kết nối với Firebase
   Firebase.begin(DATABASE_URL, SECRET_KEY);

  // Connect Dfplayer Mini Mp3
  Serial.println();
  Serial.println(F("DFRobot DFPlayer Mini"));
  Serial.println(F("Initializing DFPlayer module ... Wait!"));
  
  if (!myDFPlayer.begin(mySoftwareSerial))
  {
    Serial.println(F("Not initialized:"));
    Serial.println(F("1. Check the DFPlayer Mini connections"));
    Serial.println(F("2. Insert an SD card"));
    while (true);
  }

  Serial.println();
  Serial.println(F("DFPlayer Mini module initialized!"));

  //Definicoes iniciais
  myDFPlayer.setTimeOut(500); //Timeout serial 500ms
  myDFPlayer.volume(20); //Volume 5
  myDFPlayer.EQ(0); //Equalizacao normal

}

void XuLiMp3(String camxuc)
{
   const char* camxuc1 = camxuc.c_str();
    if(strcmp(camxuc1, "Khóc") == 0)
    {
      myDFPlayer.play(1);
      delay(10000); 
    }
    else if(strcmp(camxuc1, "Ngủ") == 0)
    {
      myDFPlayer.play(2);
      delay(10000);
    }
    else if(strcmp(camxuc1, "Khác") == 0)
    {
      myDFPlayer.stop();
    }  
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

 
  //biến cảm xúc
  Firebase.getString(fbdo,"users/" +account + "/info/emoji");
  String camxuc = fbdo.stringData();
  XuLiMp3(camxuc);
}

  
 
