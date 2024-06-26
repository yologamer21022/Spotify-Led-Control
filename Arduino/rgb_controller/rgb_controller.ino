#include <string.h>

int red = 9;                      // Pin number for the red LED
int green = 10;                   // Pin number for the green LED
int blue = 11;                    // Pin number for the blue LED
float alt = 1;                  // Altitude value for LED intensity adjustment 2.3
const char delimiter[] = "|";     // Delimiter used to separate values in the serial input

static String values[10] = {        // Array to store color values
  "[255, 255, 255]",               // Default value for the rest colors
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  "",
  ""
}; //Default Values


void setup() {
  pinMode(red, OUTPUT);                                  // Set LED pins as output
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);

  Serial.begin(9600);                                   // Initialize serial communication
}

float lerp(float start, float end, float t) {              // Perform linear interpolation between start and end values
  return start + t * (end - start);
}

void parseData(String data, unsigned long transition) {
  static int r, g, b;                                          // Static variables to store current RGB values
  
  // Remove the square brackets from the string
  data = data.substring(1, data.length() - 1);

  // Tokenize the string based on commas
  int value[3];  // Assuming there are three values
  int count = 0;
  char* ptr = strtok(const_cast<char*>(data.c_str()), ",");
  while (ptr != nullptr && count < 3) {
    value[count] = atoi(ptr);                         // Convert parsed value to integer
    ptr = strtok(nullptr, ",");
    count++;
  }

  int oldR = r;
  int oldG = g;                       // Store previous values
  int oldB = b;

  r = value[0];
  g = value[1];                // Update values
  b = value[2];

  float redIncrement, greenIncrement, blueIncrement;

  redIncrement = static_cast<float>(r - oldR) / static_cast<float>(transition);
  greenIncrement = static_cast<float>(g - oldG) / static_cast<float>(transition);               // Calculate increment per step
  blueIncrement = static_cast<float>(b - oldB) / static_cast<float>(transition);


  unsigned long startTime = millis();
  unsigned long elapsedTime = 0;

  int currentR = oldR;
  int currentG = oldG;
  int currentB = oldB;

  while (elapsedTime <= transition) {
    elapsedTime = millis() - startTime;

    float t = static_cast<float>(elapsedTime) / transition;
    currentR = static_cast<int>(lerp(oldR, r, t));
    currentG = static_cast<int>(lerp(oldG, g, t));            // Interpolate current values
    currentB = static_cast<int>(lerp(oldB, b, t));
    analogWrite(red, static_cast<int>(currentR / alt));
    analogWrite(green, static_cast<int>(currentG / alt));
    analogWrite(blue, static_cast<int>(currentB / alt));

  }
}

void runColorChange(const String* values, int counting, unsigned long duration, unsigned long transition) {
  static unsigned long startTime = 0;
  static int currentIndex = 0;          // Current index of the color in the values array

  if (millis() - startTime >= duration) {
    parseData(values[currentIndex], transition);          // Parse and transition to the next colo
    currentIndex++;
    if (currentIndex >= counting) {
      currentIndex = 0;  // Reset to the beginning
    }
    startTime = millis();
  }
}

void loop() {
  static int count = 0;      // Number of valid color values

  if (Serial.available() > 0) {
    String data = Serial.readString();
    char* token = strtok(const_cast<char*>(data.c_str()), delimiter);
    count = 0;
    while (token != nullptr && count < 5) {
      values[count] = token;            // Store received color values
      token = strtok(nullptr, delimiter);
      count++;        // Count the number of valid color values
    }
  }
  
  int validCount = 0;
  for (int i = 0; i < count; i++) {
    if (values[i] != "") {
      validCount++;
    }
  }

  unsigned long duration = 5000;  // Delay duration between color changes in milliseconds
  unsigned long transition = 5000; // Transition time

  runColorChange(values, validCount, duration, transition);           // Run the color change process
}
