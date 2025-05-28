#include <Arduino.h>
#include "Arduino_LED_Matrix.h"
#include "animation.h"

ArduinoLEDMatrix matrix;
void setup() {
    matrix.loadSequence(animation);
    matrix.begin();
    matrix.play(true);
}

void loop() {
}