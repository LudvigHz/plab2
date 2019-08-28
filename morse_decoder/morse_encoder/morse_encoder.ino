#include <Pushbutton.h>


// Pin layout
#define BUTTON_PIN 13
#define DOT_LED_PIN 5
#define DASH_LED_PIN 6

// Timing data(ms) Tune to the speed of the sender
#define DOT_TIME_MAX 400 // DOT max time (T)

#define ENABLE_LED true // Enable LED debugging


Pushbutton button(BUTTON_PIN, 1, 0);

unsigned long timePressed; // Keep timing data to determine signal
unsigned long timeReleased;
boolean buttonPressed = false; // Keep track of the button state
unsigned int previousSent; // Just to not send word end several times


// encode button press based on the timing data
unsigned int encode_press(unsigned int timePressed, unsigned int timeReleased) {
  unsigned int pressDuration = timeReleased - timePressed;
  if (pressDuration <= DOT_TIME_MAX) {
    previousSent = 0;
    if (ENABLE_LED) {
      digitalWrite(DOT_LED_PIN, HIGH);
    }
    return 0;
  } else {
    previousSent = 1;
    if (ENABLE_LED) {
      digitalWrite(DASH_LED_PIN, HIGH);
    }
    return 1;
  }
}

// encode the release time based on timing
 void encode_release(unsigned int timePressed, unsigned int timeReleased) {
  unsigned int release_duration = timePressed - timeReleased;
  if (release_duration <= DOT_TIME_MAX) {
    return;
  } else if ( release_duration < DOT_TIME_MAX*7) {
    previousSent = 2;
    Serial.println(2);
  }
}

// Helper function that returns true if the previous value sent was <value>
boolean readyForSend(unsigned int value) {
  return previousSent != value;
}



void setup() {
  pinMode(DOT_LED_PIN, OUTPUT);
  pinMode(DASH_LED_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("\n\nInitialized encoder. Ready to encode & send!\n\n");
}

void loop() {

  if (button.isPressed() && !buttonPressed) {
    // If the button is being pressed, and previous state was released,
    // check the release time, and send the appropriate signal
    timePressed = millis();
    buttonPressed = true; // Update the button state
    if (ENABLE_LED) {
      digitalWrite(DOT_LED_PIN, LOW);
      digitalWrite(DASH_LED_PIN, LOW);
    }
    if (timeReleased > 0) {
      // Simply dont send a signal first time button is pressed
      encode_release(timePressed, timeReleased);
    }
  } else if (!button.isPressed() && buttonPressed) {
    // If button is released and previous state was pressed,
    // send
    timeReleased = millis();
    buttonPressed = false; //Update state
    Serial.println(encode_press(timePressed, timeReleased));
  }

  if (readyForSend(3) && timeReleased > timePressed && (millis() - timeReleased) > DOT_TIME_MAX*7) {
    // Send word end signal if the release time is sufficient enough
    previousSent = 3;
    Serial.println(3);
    if (ENABLE_LED) {
      digitalWrite(DOT_LED_PIN, LOW);
      digitalWrite(DASH_LED_PIN, LOW);
    }
  }

  // Easier than debounce handling and works well...
  delay(20);
}
