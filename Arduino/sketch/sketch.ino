// This code depends on ArduinoJson library
// Installation: https://docs.arduino.cc/software/ide-v1/tutorials/installing-libraries
// Documentation: https://arduinojson.org/v6/how-to/do-serial-communication-between-two-boards/
#include <ArduinoJson.h>
#include <string>

bool DEBUG = false;
String lanes[] = {
  "in_road_n_0",
  "in_road_s_0",
  "out_road_n_0",
  "out_road_s_0",
  "in_sidewalk_w_0",
  "in_sidewalk_e_0"
};

int CAR1 = 0, // id from lanes[]
    CAR1_RED = 12,
    CAR1_YELLOW = 11,
    CAR1_GREEN = 10,
    CAR1_IN = 9,
    CAR1_OUT = 8;

int SIDEWALK1 = 4,
    SIDEWALK1_RED = 7,
    SIDEWALK1_GREEN = 6,
    SIDEWALK1_ANALOG_IN = A0;

bool inputBuffer[13] = { 0 }; // stores last value of digitalRead()

// method sends a message via serial port (commandName = "add"|"remove"|"set")
void serialCommand(String commandName, String laneName, int count, int timeOffset);

// if available, method reads JSON from serial port
// example json: {"in_road_n_0":{"light":"red", "waiting-count":5}, "in_road_s_0":{"light":"yellow", "waiting-count":2}}
void serialState();

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1000); // set timeout to 1 second
  pinMode(CAR1_RED, OUTPUT);
  pinMode(CAR1_YELLOW, OUTPUT);
  pinMode(CAR1_GREEN, OUTPUT);
  pinMode(CAR1_IN, INPUT_PULLUP);
  pinMode(CAR1_OUT, INPUT_PULLUP);
  pinMode(SIDEWALK1_RED, OUTPUT);
  pinMode(SIDEWALK1_GREEN, OUTPUT);
  pinMode(SIDEWALK1_ANALOG_IN, INPUT);
}

int prev_pedestrian_count = 0;
int loop_counter = 0;
void loop() {
  // SEND (testing)
//  serialCommand("add", "in_road_n_0", 2, 0);
//  serialCommand("remove", "in_road_n_0", 1, 0);
//  serialCommand("set", "in_road_n_0", 5, 0);

  // READ SENSORS
  if (isPressed(CAR1_IN)) // Adding a new car with -10sec offset
    serialCommand("add", "in_road_n_0", 1, -10);
  if (isPressed(CAR1_OUT)) // Removing a car from the waitlist
    serialCommand("remove", "in_road_n_0", 1, 0);
  if (loop_counter % 20 == 0) {
    int weight = analogRead(SIDEWALK1_ANALOG_IN); // 0..1023 (lets say kg)
    int avg_weight = 80; // average weight of a person
    int pedestrian_count = weight / avg_weight;
    if (pedestrian_count != prev_pedestrian_count) {
      serialCommand("set", "in_sidewalk_w_0", pedestrian_count, 0);
      prev_pedestrian_count = pedestrian_count;
    }
  }

  // RECEIVE
  serialState();
  
  // WAIT
  delay(100);
  loop_counter++;
}

// ==== Handling digital input ==== //
// Activates only once per button press
bool isPressed(int PIN) {
  if (digitalRead(PIN) == LOW) {
    if (!inputBuffer[PIN]){
      inputBuffer[PIN] = true;
      return true;
    }
    return false;
  }
  inputBuffer[PIN] = false;
  return false;
}

// ==== Handling lights ==== //
// example: setLights('g', 10, 11, 12) - set a green light using given pins
void setLights(char light, int RED, int YELLOW, int GREEN) {
  digitalWrite(RED, LOW);
  digitalWrite(YELLOW, LOW);
  digitalWrite(GREEN, LOW);
  switch (light) {
    case 'r': digitalWrite(RED, HIGH); break;
    case 'y': digitalWrite(YELLOW, HIGH); break;
    case 'g': digitalWrite(GREEN, HIGH); break;
  }
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
    char light = doc[lane]["light"].as<String>()[0];
    if (lane == lanes[CAR1])
      setLights(light, CAR1_RED, CAR1_YELLOW, CAR1_GREEN);
    if (lane == lanes[SIDEWALK1])
      setLights(light, SIDEWALK1_RED, SIDEWALK1_RED, SIDEWALK1_GREEN);
    
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
