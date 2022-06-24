#include <WiFi.h>
#include <FirebaseESP32.h>

// TEST =================
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "Base64.h"
#include "esp_camera.h"
#include "DHT.h"    
// ================

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

/* 1. Nhập tên và mật khẩu wifi mà ESP32_Cam sẽ kết nối đến*/
#define WIFI_SSID " "
#define WIFI_PASSWORD " "

/* 2. Nhập API Key */
#define API_KEY "AIzaSyDar4RogfH1TQo1tDyItTQt6_LWbHtBOD4"

/* 3. Nhập Real Time Database URL */
#define DATABASE_URL "https://pbl5-arduino-default-rtdb.firebaseio.com" //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app

/* 4.Nhập Email và mật khẩu tương ứng khi đăng kí cơ sở dữ liệu mới trên Firebase */
#define USER_EMAIL "admin@gmail.com" // tao user
#define USER_PASSWORD "123456"

// Khai báo các đối tượng của Firebase Data 
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig configfb;

unsigned long sendDataPrevMillis = 0;
unsigned long PrevMillis = millis();

//5 dòng tiếp theo là khai báo chân module L298N
int IN1 = 12;
int IN2 = 15;
int IN3 = 13;
int IN4 = 14;

//3 dòng tiếp theo khai báo chân của cảm biến nhiệt độ độ ẩm
int DHTPIN = 2;       //Đọc dữ liệu từ DHT11 ở chân 2 trên mạch Arduino
int DHTTYPE = DHT11;  //Khai báo loại cảm biến, có 2 loại là DHT11 và DHT22
DHT dht(DHTPIN, DHTTYPE);

// TEST ============
#define CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// ====================


void setup()
{
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  dht.begin();// Khởi động cảm biến


  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }

  if (WiFi.status() == WL_CONNECTED) {
    char* apssid = "ESP32-CAM";
    char* appassword = "12345678"; 

    WiFi.softAP((WiFi.localIP().toString()+"_"+(String)apssid).c_str(), appassword);            
  }
  else {
    return;
  } 

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    delay(1000);
    ESP.restart();
  }

  sensor_t * s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_CIF);
  
  // =========================================================================

  
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  /* Assign the api key (required) */
  configfb.api_key = API_KEY;

  /* Assign the user sign in credentials */
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the RTDB URL (required) */
  configfb.database_url = DATABASE_URL;

  /* Assign the callback function for the long running token generation task */
  configfb.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&configfb, &auth);

  //Comment or pass false value when WiFi reconnection will control by your code or third party library
  Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);
  long count = 0;
}

void BatQuat()
{
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(100);
}

void TatQuat()
{
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  delay(100);
}
void LacNoi()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  delay(100);
}

void DungNoi()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  delay(100);
}

void XuLiQuat(String chedo,float nhietdo,String fan)
{ 
   const char* chedo1 = chedo.c_str();
   const char* fan1 = fan.c_str();

  if(strcmp(chedo1,"ON") == 0)
  {
     Serial.println("chế độ quạt tự động");
     Serial.println(nhietdo);
     if( nhietdo >= 32)
      {
        BatQuat();
      }
      else if(nhietdo <= 32)
      {
        TatQuat();
      }
   }
  else if(strcmp(chedo1,"OFF") == 0) 
    {
      Serial.println("chế độ quạt thủ công");
      Serial.println(nhietdo);
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

void XuLiNoi(String chedo,String camxuc,String cradle)
{
  const char* chedo1 = chedo.c_str();
  const char* camxuc1 = camxuc.c_str();
  const char* cradle1 = cradle.c_str();
 
  if(strcmp(chedo1,"OFF") == 0) 
  {
    Serial.println("chế độ nôi thủ công");
    if(strcmp(cradle1,"ON") == 0)
    {
      LacNoi();
    }
    else if(strcmp(cradle1,"OFF") == 0) 
    {
      DungNoi();
    }
 }
 else if(strcmp(chedo1,"ON") == 0)
 {
  Serial.println("chế độ nôi tự động");
    if(strcmp(camxuc1,"Khác") == 0)
    {
      Serial.println("em bé không có gì bất thường");
      DungNoi();
    }
    else if(strcmp(camxuc1, "Khóc") == 0)
    {
      Serial.println("em bé đang khóc, lắc nôi để dỗ ");
      LacNoi();
    }
    else if(strcmp(camxuc1, "Ngủ") == 0)
    {
      Serial.println("em bé đang buồn ngủ, ru đời đi nhé");
      LacNoi();
    }
    else
    {
      DungNoi();
    }
  }
 
}

void loop()
{   
  String account = "trquan17"; //tên tài khoản user khi đăng nhập vào web
  if (Firebase.ready() && (millis() - sendDataPrevMillis > 3000 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();
    String str = Photo2Base64();
    String path = "users/" + account + "/info/image_encode";

    // cho biết là đã gửi ảnh thành công lên firebase hay chưa
    Serial.printf("Send image... %s\n", Firebase.setString(fbdo, path, str) ? "success" : fbdo.errorReason().c_str());
  }

  //biến chế độ
  Firebase.getString(fbdo,"users/" + account + "/control/auto");
  String chedo = fbdo.stringData(); 

  //biến cảm xúc
  Firebase.getString(fbdo,"users/" +account + "/info/emoji");
  String camxuc = fbdo.stringData();

  //biến điều khiển bật/tắt nôi 
  Firebase.getString(fbdo,"users/" +account + "/control/status_cradle");
  String cradle = fbdo.stringData();

  //biến điều khiển bật/tắt quạt
  Firebase.getString(fbdo,"users/" + account + "/control/status_fan");
  String fan = fbdo.stringData();


  ////test
  Firebase.getInt(fbdo,"users/" + account + "/info/temp");
  int nhietdo = fbdo.intData();
  ////

//  float doam = dht.readHumidity();    //Đọc độ ẩm
//  float nhietdo = dht.readTemperature(); //Đọc nhiệt độ
//  Firebase.setInt(fbdo,"users/" + account + "/info/temp",nhietdo);// gửi nhiệt độ lên Firebase
//  Firebase.setInt(fbdo,"users/" + account + "/info/hum",doam);// gửi độ ẩm lên Firebase

    
  //dòng tiếp theo tùy theo chế độ và cảm xúc mà cho lắc nôi hay ko 
  XuLiNoi(chedo,camxuc,cradle);
  
  // dòng tiếp theo tùy theo chế độ hoặc nhiệt độ mà cho bật tắt quạt
  XuLiQuat(chedo,nhietdo,fan); 
}

String Photo2Base64() {
    camera_fb_t * fb = NULL;
    fb = esp_camera_fb_get();  
    if(!fb) {
      return "";
    }
  
    String imageFile = "data:image/jpeg;base64,";
    char *input = (char *)fb->buf;
    char output[base64_enc_len(3)];
    for (int i=0;i<fb->len;i++) {
      base64_encode(output, (input++), 3);
      if (i%3==0) imageFile += urlencode(String(output));
    }

    esp_camera_fb_return(fb);
    
    return imageFile;
}

String urlencode(String str)
{
    String encodedString="";
    char c;
    char code0;
    char code1;
    char code2;
    for (int i =0; i < str.length(); i++){
      c=str.charAt(i);
      if (c == ' '){
        encodedString+= '+';
      } else if (isalnum(c)){
        encodedString+=c;
      } else{
        code1=(c & 0xf)+'0';
        if ((c & 0xf) >9){
            code1=(c & 0xf) - 10 + 'A';
        }
        c=(c>>4)&0xf;
        code0=c+'0';
        if (c > 9){
            code0=c - 10 + 'A';
        }
        code2='\0';
        encodedString+='%';
        encodedString+=code0;
        encodedString+=code1;
      }
      yield();
    }
    return encodedString;
}