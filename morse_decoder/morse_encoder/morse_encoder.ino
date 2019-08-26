#include <Pushbutton.h>


// Pin layout
#define BUTTON_PIN 35
#define DOT_LED_PIN 32
#define DASH_LED_PIN 33

// Timing data(ms) Tune to the speed of the sender
#define DOT_TIME_MAX 400 // DOT max time (T)


Pushbutton button(BUTTON_PIN, 1, 0);

unsigned long timePressed; // Keep timing data to determine signal
unsigned long timeReleased;
boolean buttonPressed = false;
boolean buttonReleased = true;
unsigned int previousSent;


// decode based on timing
unsigned int decode_press(unsigned int timePressed, unsigned int timeReleased) {
  unsigned int pressDuration = timeReleased - timePressed;
  if (pressDuration <= DOT_TIME_MAX) {
      previousSent = 0;
    return 0;
  } else {
      previousSent = 1;
    return 1;
  }
}

 void decode_release(unsigned int timePressed, unsigned int timeReleased) {
  unsigned int release_duration = timePressed - timeReleased;
  if (release_duration <= DOT_TIME_MAX) {
    return;
  } else if ( release_duration < DOT_TIME_MAX*7) {
      previousSent = 2;
    Serial.println(2);
  }
}

boolean readyForSend(unsigned int value) {
  return previousSent != value;
}


void setup() {
  Serial.begin(9600);
  Serial.println("\n\nInitialized encoder. Ready to encode & send!\n\n");
}

void loop() {


  if (button.isPressed() && !buttonPressed) {
      timePressed = millis();
      buttonPressed = true;
      if (timeReleased > 0) {
        decode_release(timePressed, timeReleased);
      }
    } else if (!button.isPressed() && buttonPressed) {
      timeReleased = millis();
      buttonPressed = false;
      Serial.println(decode_press(timePressed, timeReleased));
    }

    if (readyForSend(3) && timeReleased > timePressed && (millis() - timeReleased) > DOT_TIME_MAX*7) {
      previousSent = 3;
      Serial.println(3);
    }
    delay(20);

  }
