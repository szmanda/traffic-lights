// This code depends on ArduinoJson library
// Installation: https://docs.arduino.cc/software/ide-v1/tutorials/installing-libraries
// Documentation: https://arduinojson.org/v6/how-to/do-serial-communication-between-two-boards/
#include <ArduinoJson.h>
#include <string>

bool DEBUG = true;
String lanes[] = {
  "in-road-north-1",
  "in-road-south-1",
  "out-road-north-1",
  "out-road-south-1",
  "in-sidewalk-west-1",
  "in-sidewalk-east-1"
};


// method sends a message via serial port (commandName = "add"|"remove"|"set")
void serialCommand(String commandName, String laneName, int count, int timeOffset);

// if available, method reads JSON from serial port
// example json: {"in-road-north-1":{"light":"red", "waiting-count":5}, "in-road-south-1":{"light":"yellow", "waiting-count":2}}
void serialState();

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1000); // set timeout to 1 second
}
 
void loop() {
  // SEND
  serialCommand("add", "in-road-north-1", 2, 0);
  serialCommand("remove", "in-road-north-1", 1, 0);
  serialCommand("set", "in-road-north-1", 5, 0);

  // RECEIVE
  serialState();
  
  // WAIT
  delay(5000);
}

// ==== Handling serial port messages ==== //

// method sends a message via serial port
void serialCommand(String commandName, String laneName, int count, int timeOffset) {
  // Create the JSON document
  StaticJsonDocument<200> doc;
  doc[laneName]["count"] = count;
  doc[laneName]["time-offset"] = timeOffset;

  // Send the message type and JSON document over the serial port
  Serial.println(commandName);
  serializeJson(doc, Serial);
  Serial.println();
}

// if available, method reads JSON from serial port
void serialState(){
  if (!Serial.available()) return NULL;
  delay(100); // make sure the message is fully received
  
  // Allocate the JSON document
  // This one must be bigger than the sender's because it must store the strings
  StaticJsonDocument<900> doc;
  // Read the JSON document from the serial port
  DeserializationError err = deserializeJson(doc, Serial);
  if (err != DeserializationError::Ok) {
    if (!DEBUG) {
      while (Serial.available() > 0) Serial.read(); // Flush all bytes in the serial port buffer
      return NULL;
    }
    // if in debug, print the error
    Serial.print("deserializeJson() has thrown an error: ");
    Serial.println(err.c_str());
    Serial.print("Remaining in buffer: ");
    while (Serial.available() > 0) Serial.print((char)Serial.read());
    return NULL;
  }

  // Reading the values
  // (we must use as<T>() to resolve the ambiguity)
  if (DEBUG) Serial.println("Succesfully received JSON");
  for (String lane : lanes) {
    if (DEBUG) {
      Serial.println(lane);
      Serial.print("\t light:");
      Serial.print(doc[lane]["light"].as<String>());
      Serial.print("\n\t waiting-count:");
      Serial.print(doc[lane]["waiting-count"].as<int>());
      Serial.println();
    }
  }
}
