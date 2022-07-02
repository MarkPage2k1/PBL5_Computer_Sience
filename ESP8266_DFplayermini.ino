#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

//khai báo chân dfplayer mini mp3
SoftwareSerial mySoftwareSerial(D3, D4); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

/* 1. Nhập tên và mật khẩu wifi mà ESP32_Cam sẽ kết nối đến*/
#define WIFI_SSID "PBL5"
#define WIFI_PASSWORD "PBL5PBL5"

/* 2. Nhập Real Time Database URL */
#define DATABASE_URL "https://pbl5-arduino-default-rtdb.firebaseio.com"

#define SECRET_KEY "6oFzmOzrZbOSMqOiFm56QddahtwXM7FuzOdsPprC"

FirebaseData fbdo;

void setup() {
    Serial.begin(9600);
    mySoftwareSerial.begin(9600);

    
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
   while (WiFi.status() != WL_CONNECTED)
    {
      Serial.print(".");
      delay(300);
    }
   
   //Kết nối với Firebase
   Firebase.begin(DATABASE_URL, SECRET_KEY);

  // Kết nối Dfplayer Mini Mp3
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

  //Khởi tạo các chỉ số âm lượng, EQ của dfplayermini
  myDFPlayer.setTimeOut(500); //Timeout serial 
  myDFPlayer.volume(20); //Volume 
  myDFPlayer.EQ(0); //Equalizacao normal
}

void loop() {
  String account = "trquan17"; //tên tài khoản user khi đăng nhập vào web 

  //biến cảm xúc
  Firebase.getString(fbdo,"users/" +account + "/info/emoji");
  String camxuc = fbdo.stringData();
  XuLiMp3(camxuc);
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
