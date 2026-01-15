#include <BleGamepad.h>
#include <FastLED.h>
#define JOY_X_PIN 1;
#define JOY_Y_PIN 0;
#define JOY_BTN_PIN 2;
#define BTN_UP_PIN 4;
#define BTN_DN_PIN 3;
#define BATTERY_PIN 7;
#define LED_PIN 10;
CRGB leds[20];

const int CENTER_VALUE = 2048;
const int DEADZONE = 150; 

BleGamepad bleGamepad("Controller_1", "Lenz", 100); //This is just the code for controller 1, but this is the only difference.

unsigned long buttonPressedTime = 0;
unsigned long lastConnectionTime = 0;
unsigned long lastBatteryReportTime = 0;
const unsigned long SLEEP_TIMEOUT = 300000; 
const unsigned long OFF_PRESS_TIME = 5000;
const unsigned long BATTERY_INTERVAL = 20000;

struct BatteryStep { float voltage; int percentage; };
const BatteryStep batteryTable[] = {
  {4.15, 100}, {4.05, 90}, {3.97, 80}, {3.90, 70}, {3.84, 60},
  {3.79, 50},  {3.75, 40}, {3.71, 30}, {3.66, 20}, {3.60, 10},
  {3.40, 5},   {3.20, 0}
}; //I took this table from the web.

const int tableSize = sizeof(batteryTable) / sizeof(BatteryStep);

int getBatteryPercentage() {
  long sum = 0;
  for(int i=0; i<20; i++) sum += analogRead(BATTERY_PIN);
  float avgRaw = sum / 20.0;
  float voltage = (avgRaw / 4095.0) * 6.6;

  if (voltage >= batteryTable[0].voltage) return 100;
  if (voltage <= batteryTable[tableSize - 1].voltage) return 0;
  
  for (int i = 0; i < tableSize - 1; i++) {
    if (voltage <= batteryTable[i].voltage && voltage > batteryTable[i+1].voltage) {
      float diff = batteryTable[i].voltage - batteryTable[i+1].voltage;
      float weight = (voltage - batteryTable[i+1].voltage) / diff;
      return batteryTable[i+1].percentage + (weight * (batteryTable[i].percentage - batteryTable[i+1].percentage));
    }
  }
  return 0;
}

int32_t processAxis(int rawValue) {
  int delta = rawValue - CENTER_VALUE;
  if (abs(delta) < DEADZONE) return 0;
  if (delta > 0) return map(rawValue, CENTER_VALUE + DEADZONE, 4095, 0, 32767);
  else return map(rawValue, 0, CENTER_VALUE - DEADZONE, -32767, 0);
}

// the following parts are the animations for my LEDs. I had to use a template and edit it.
void showBatteryLevel() {
  int pct = getBatteryPercentage();
  int numLedsToLight = pct / 5;
  CRGB color = (pct > 20) ? CRGB::Green : CRGB::Red;
  FastLED.clear();
  for(int i = 0; i < numLedsToLight; i++) leds[i] = color;
  for(int b = 0; b <= 100; b += 2) { FastLED.setBrightness(b); FastLED.show(); delay(10); }
  delay(1000); 
  for(int b = 100; b >= 0; b -= 2) { FastLED.setBrightness(b); FastLED.show(); delay(10); }
  FastLED.clear(); FastLED.show(); FastLED.setBrightness(50); 
}

void showSearchAnimation() {
  static uint8_t hue = 0; 
  for(int i = 0; i < 20; i++) {
    leds[i] = CHSV(hue, 255, 200);
    FastLED.show();
    delay(30);
    leds[i] = CRGB::Black;
    if(bleGamepad.isConnected()) return; 
  }
  hue += 40; 
}

// I made a function for this because it is used in two cases and the animation only in one case.
void goToSleep() {
  FastLED.clear(); FastLED.show();
  esp_deep_sleep_enable_gpio_wakeup(1 << JOY_BTN_PIN, ESP_GPIO_WAKEUP_LOW_LEVEL);
  esp_deep_sleep_start();
}

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, 20);
  showBatteryLevel();
  pinMode(JOY_BTN_PIN, INPUT_PULLUP);
  pinMode(BTN_UP_PIN, INPUT_PULLUP);
  pinMode(BTN_DN_PIN, INPUT_PULLUP);
  bleGamepad.begin();
  lastConnectionTime = millis();
}

void loop() {
  bool joyBtn = !digitalRead(JOY_BTN_PIN);

  if (joyBtn) {
    if (buttonPressedTime == 0) buttonPressedTime = millis();
    if (millis() - buttonPressedTime >= OFF_PRESS_TIME) {
      for(int i = 20 - 1; i >= 0; i--) {
    int distanceFromMiddle = abs(i - (20 / 2));
    int brightness = map(distanceFromMiddle, 0, 20/2, 255, 20);
    
    leds[i] = CRGB::Red;
    FastLED.setBrightness(brightness);
    FastLED.show();
    delay(50);
    leds[i] = CRGB::Black;
    FastLED.show();
  }
  FastLED.setBrightness(50);

      goToSleep();
    }
  } else {
    buttonPressedTime = 0;
  }

  if (bleGamepad.isConnected()) {
    lastConnectionTime = millis();
    bleGamepad.setLeftThumb(processAxis(analogRead(JOY_X_PIN)), processAxis(analogRead(JOY_Y_PIN)));

    if (joyBtn) bleGamepad.press(BUTTON_1); else bleGamepad.release(BUTTON_1);
    if (!digitalRead(BTN_UP_PIN)) bleGamepad.press(BUTTON_2); else bleGamepad.release(BUTTON_2);
    if (!digitalRead(BTN_DN_PIN)) bleGamepad.press(BUTTON_3); else bleGamepad.release(BUTTON_3);

    if (millis() - lastBatteryReportTime >= BATTERY_INTERVAL) {
      bleGamepad.setBatteryLevel(getBatteryPercentage());
      lastBatteryReportTime = millis();
    }
    bleGamepad.sendReport();
  } else {
    showSearchAnimation();
    if (millis() - lastConnectionTime >= SLEEP_TIMEOUT) goToSleep();
  }
  delay(10);
}