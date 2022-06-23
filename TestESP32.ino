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
#define WIFI_SSID "T & H"
#define WIFI_PASSWORD "1.2.3.4."

//For the following credentials, see examples/Authentications/SignInAsUser/EmailPassword/EmailPassword.ino

/* 2. Nhập API Key */
#define API_KEY "AIzaSyD9eYYLfgWA2T_7Q8Oye3ws28BOzHdbgjE"

/* 3. Nhập Real Time Database URL */
#define DATABASE_URL "https://test-cb7c4-default-rtdb.firebaseio.com/" //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app

/* 4. Define the user Email and password that alreadey registerd or added in project */
#define USER_EMAIL "19tclcdt1@gmail.com" // tao user
#define USER_PASSWORD "Qwerty@1234"

// Khai báo các đối tượng của Firebase Data 
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig configfb;

unsigned long sendDataPrevMillis = 0;
unsigned long count = 0;
unsigned long PrevMillis = millis();

//5 dòng tiếp theo là khai báo chân module L298N
int IN1 = 12;
int IN2 = 15;
int IN3 = 13;
int IN4 = 2;

//3 dòng tiếp theo khai báo chân của cảm biến nhiệt độ độ ẩm
int DHTPIN = 16;       //Đọc dữ liệu từ DHT11 ở chân 2 trên mạch Arduino
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

void XuLiQuat(int nhietdo,int chedo,int fan)
{ 
   
if( chedo == 0){
   Serial.println("chế độ tự động");
   if( nhietdo >= 32)
    {
      BatQuat();
    }else 
    {
      TatQuat();
    }
  }
  else {
    Serial.println("chế độ thủ công");
    if(fan == 1)
    {
      BatQuat();
    }else 
    {
      TatQuat();
    }
  }
}

void XuLiNoi(String camxuc)
{
  const char* camxuc1 = camxuc.c_str();

 if(strcmp(camxuc1,"happy") == 0)
  {
    Serial.println("em bé đang vui, không lắc nôi");
    DungNoi();
  }
  else if(strcmp(camxuc1, "cry") == 0)
  {
    Serial.println("em bé đang khóc, lắc nôi để dỗ ");
    LacNoi();
  }
  else if(strcmp(camxuc1, "sleepy") == 0)
  {
    Serial.println("em bé đang buồn ngủ, ru đời đi nhé");
    LacNoi();
  }
  else
  {
     DungNoi();
  }
}

void loop()
{   

  if (Firebase.ready() && (millis() - sendDataPrevMillis > 3000 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();
    String str = Photo2Base64();
    String path = "users/thanh/info/image_encode";

    // cho biết là đã gửi ảnh thành công lên firebase hay chưa
    Serial.printf("Send image... %s\n", Firebase.setString(fbdo, path, str) ? "success" : fbdo.errorReason().c_str());
  }
  
  // 3 dòng tiếp theo tùy theo cảm xúc mà cho lắc nôi hay ko 
  Firebase.getString(fbdo,"emotion");
  String camxuc = fbdo.stringData();
  XuLiNoi(camxuc);


  // 7 dòng tiếp theo tùy theo chế độ hoặc nhiệt độ mà cho bật tắt quạt
  int nhietdo = dht.readTemperature(); //Đọc nhiệt độ từ cảm biến
//  Firebase.setString(fbdo,"users/thanh/info/temperature", nhietdo); // gửi nhiệt độ lên Firebase
  Firebase.getInt(fbdo,"chedo");
  int chedo = fbdo.intData();
  Firebase.getInt(fbdo,"fan");
  int fan = fbdo.intData();
  XuLiQuat(nhietdo,chedo,fan); 


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
