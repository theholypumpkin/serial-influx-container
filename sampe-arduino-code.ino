#include <ArduinoJson.h>
#include <ArduinoJson.hpp>

void setup() {
  Serial.begin(115200);
  while(!Serial);
}

void loop() {
  // Create a new document on every loop because it's the proper way to use the library
  StaticJsonDocument<88> json;
  json["measurement"].set("indoor air quality");
  json["tags"]["location"].set("living room");
  json["tags"]["uuid"].set(65535);
  json["tags"]["name"].set("name");
  json["fields"]["eCO2"].set(random(350,500));
  json["fields"]["TVOC"].set(random(0,3000));
  json["fields"]["temperature"].set(random(20,30));
  json["fields"]["humidity"].set(random(0,100));
  json["fields"]["dust"].set(random(0,10));

  serializeJson(json,Serial);
  Serial.println();
  Serial.flush();
  delay(10000);
}
