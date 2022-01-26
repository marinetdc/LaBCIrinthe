#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

/*

Ce script permet d'allumer et éteindre chaque led en fonction du 
boutton qui est appuuyé. Chaque led s'allume durant 3 secondes 
et clignotent à des fréquences différentes. 

*/




// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        6 // On Trinket or Gemma, suggest changing this to 1
unsigned long previousMillis = 0;
const long interval =50;
int state = 0;

#define PIN2       9
unsigned long previousMillis2 = 0;
const long interval2 = 72;
int state2 = 0;

#define PIN3       11
unsigned long previousMillis3 = 0;
const long interval3 = 62;
int state3 = 0;

#define PIN4       3
unsigned long previousMillis4 = 0;
const long interval4 = 55;
int state4 = 0;


// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 7 // Popular NeoPixel ring size
#define NUMPIXELS2 7
#define NUMPIXELS3 7
#define NUMPIXELS4 7
// PIN 1


Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels2(NUMPIXELS4, PIN2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels3(NUMPIXELS4, PIN3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels4(NUMPIXELS4, PIN4, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

// Def des Bouttons 

const int buttonPin1 = 4;
const int buttonPin2 = 5;
const int buttonPin3 = 7;
const int buttonPin4 = 8;

void setup() {
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  Serial.begin(9600);
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels2.begin();
  pixels3.begin();
  pixels4.begin();

  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  pinMode(buttonPin4, INPUT_PULLUP);
}

void loop() {
  // pixels.clear(); // Set all pixel colors to 'off'

  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);

  if (buttonState1 == LOW) {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      state = !state;

      if (state == 0) {
        for (int i = 0; i < NUMPIXELS; i++) {
          pixels.setPixelColor(i, pixels.Color(0, 250, 0));
          pixels.show();
        }
      } else {
        for (int i = 0; i < NUMPIXELS; i++) {
          pixels.setPixelColor(i, pixels.Color(0, 0, 0));
          pixels.show();

        }
      }
    }
    delay(3)
    for (int i = 0; i < NUMPIXELS; i++) {
          pixels.setPixelColor(i, pixels.Color(0, 0, 0));
          pixels.show();
        }
  }

  if (buttonState2 == LOW) {
    unsigned long currentMillis2 = millis();
    if (currentMillis2 - previousMillis2 >= interval2) {
      previousMillis2 = currentMillis2;
      state2 = !state2;

      if (state2 == 0) {
        for (int i = 0; i < NUMPIXELS2; i++) {
          pixels2.setPixelColor(i, pixels2.Color(0, 250, 0));
          pixels2.show();
        }
      } else {
        for (int i = 0; i < NUMPIXELS2; i++) {
          pixels2.setPixelColor(i, pixels2.Color(0, 0, 0));
          pixels2.show();

        }
      }
    }
    delay(3)
    for (int i = 0; i < NUMPIXELS; i++) {
          pixels2.setPixelColor(i, pixels.Color(0, 0, 0));
          pixels2.show();
        }
  }

  if (buttonState3 == LOW) {
    unsigned long currentMillis3 = millis();
    if (currentMillis3 - previousMillis3 >= interval3) {
      previousMillis3 = currentMillis3;
      state3 = !state3;

      if (state3 == 0) {
        for (int i = 0; i < NUMPIXELS3; i++) {
          pixels3.setPixelColor(i, pixels3.Color(0, 250, 0));
          pixels3.show();
        }
      } else {
        for (int i = 0; i < NUMPIXELS3; i++) {
          pixels3.setPixelColor(i, pixels3.Color(0, 0, 0));
          pixels3.show();

        }
      }
    }
    delay(3)
    for (int i = 0; i < NUMPIXELS; i++) {
          pixels3.setPixelColor(i, pixels.Color(0, 0, 0));
          pixels3.show();
        }
  }

  if (buttonState4 == LOW) {
    unsigned long currentMillis4 = millis();
    if (currentMillis4 - previousMillis4 >= interval4) {
      previousMillis4 = currentMillis4;
      state4 = !state4;

      if (state4 == 0) {
        for (int i = 0; i < NUMPIXELS4; i++) {
          pixels4.setPixelColor(i, pixels4.Color(0, 250, 0));
          pixels4.show();
        }
      } else {
        for (int i = 0; i < NUMPIXELS4; i++) {
          pixels4.setPixelColor(i, pixels4.Color(0, 0, 0));
          pixels4.show();

        }
      }
    }
    delay(3)
    for (int i = 0; i < NUMPIXELS; i++) {
          pixels4.setPixelColor(i, pixels.Color(0, 0, 0));
          pixels4.show();
        }
  }
}
