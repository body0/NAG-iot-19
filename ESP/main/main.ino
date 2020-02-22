#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

#define deepSleepTime 60e6 // 1m

const char *ssid = "pudil.cz";  //ENTER YOUR WIFI SETTINGS
const char *password = "staromak104";


const char *host = "192.168.1.198";
const char *route = "/espPld";
const int httpsPort = 4000;  //HTTPS= 443 and HTTP = 80
 
const char fingerprint[] PROGMEM = "06 38 72 65 EE 6A EC AC 8E F0 B7 1F E9 A5 43 CF 0F 1F F9 18";

void setup() {
    delay(500);
    Serial.begin(115200);
    Serial.println("");
    Serial.println("Init");
    WiFi.mode(WIFI_OFF);        //Prevents reconnection issue (taking too long to connect)
    delay(1000);
    WiFi.mode(WIFI_STA);
    
    WiFi.begin(ssid, password);
    Serial.print("Connecting");
    // Wait for connection
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("Connected!!!!");


    WiFiClientSecure httpsClient;    //Declare object of class WiFiClient

    Serial.printf("Using fingerprint '%s'\n", fingerprint);
    httpsClient.setFingerprint(fingerprint);
    httpsClient.setTimeout(15000); // 15 Seconds
    delay(1000);
    
    Serial.print("HTTPS Connecting");
    int r=0; //retry counter
    while((!httpsClient.connect(host, httpsPort)) && (r < 30)){
        delay(100);
        Serial.print(".");
        r++;
    }
    if(r==30) { // can not connect to server
        digitalWrite(LED_BUILTIN, HIGH);
        delay(500);
        digitalWrite(LED_BUILTIN, LOW); 
        delay(500);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(500);
        digitalWrite(LED_BUILTIN, LOW); 
        delay(500);
        // ESP.deepSleep(deepSleepTime);
    }
    else {
        Serial.println("Connected to web");
    }

    int temp = 10;
    int pres = 10;
    int hum = 10;
    int light = 10;
    int batteryState = 10;
    String body = String("{\"temp\":") + light + ", \"pres\":" + pres + ", \"hum\":" + hum + ", \"light\":" + light + ", \"batteryState\":" + batteryState + " }";
    Serial.println(String("POST ") + route + " HTTP/1.1\r\n" +
                "Host: " + host + "\r\n" +
                "Content-Type: application/json\r\n" +              
                "Connection: close\r\n" +
                "Content-Length: " + body.length() + "\r\n" +
                "\r\n" +
                body + "\r\n");

    httpsClient.print(String("POST ") + route + " HTTP/1.1\r\n" +
                "Host: " + host + "\r\n" +
                "Content-Type: application/json\r\n" +              
                "Connection: close\r\n" +
                "Content-Length: " + body.length() + "\r\n" +
                "\r\n" +
                body + "\r\n");

    Serial.println("request sent");
    // ESP.deepSleep(deepSleepTime);
                    
   /*  while (httpsClient.connected()) {
        String line = httpsClient.readStringUntil('\n');
        if (line == "\r") {
        Serial.println("headers received");
        break;
        }
    }

    Serial.println("reply was:");
    Serial.println("==========");
    String line;
    while(httpsClient.available()){        
        line = httpsClient.readStringUntil('\n');  //Read Line by Line
        Serial.println(line); //Print response
    }
    Serial.println("==========");
    Serial.println("closing connection"); */
    
}

void loop() {
  
}
