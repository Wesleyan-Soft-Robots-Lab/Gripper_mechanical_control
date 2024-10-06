/*
Name: Katelyn Rosethorn
Date Created: 7/23/2024
Last Updated: 8/6/2024

Description:
  Reads from a single capacitor using the FDC1004 chip over I2C ports.
*/

#include <Wire.h>
#include <Protocentral_FDC1004.h>
#include <List.hpp>

FDC1004 FDC;
uint8_t hardware_offset = 9; // offset (in pF) = hardware_offset * 3.125 (14)
uint16_t scalar = 460; // scalar for converting chip output to Farads
int MAX_WINDOW = 10; // max window size for the rolling window stability. Set to 1 to disable.

// define the Sensor struct to include a name, channel, window list, sum, and resulting capacitance and offset
typedef struct Sensor {
  char* name = "";
  uint8_t channel = 0;
  List<int32_t> window;
  int32_t window_sum = 0;
  int32_t capacitance;
  int16_t software_offset = 0; // in femtoFarads (1000 fF = 1 pF)
};

// initialize the 1 capacitor
const int number_of_sensors = 1;
Sensor Sensors[number_of_sensors];
void Sensor_Init() {
  Sensors[0].name = "1A";
  Sensors[0].channel = 0;
}

//idrk
#define UPPER_BOUND  0X4000                 // max readout capacitance
#define LOWER_BOUND  (-1 * UPPER_BOUND)   

bool is_calibrated = false;


// Returns a measurement from the given channel
void update_measurement() {         
  for (int i=0;i<number_of_sensors;i++) {
    FDC.configureMeasurementSingle(Sensors[i].channel, Sensors[i].channel,hardware_offset);
    FDC.triggerSingleMeasurement(Sensors[i].channel, FDC1004_100HZ);
    delay(20);
    uint16_t value[2];
    if (!FDC.readMeasurement(Sensors[i].channel, value)) {
      // add the current measurement to the window and compute the new average
      int16_t msb = value[0];
      int32_t cur = ((int32_t)scalar)*((int32_t)msb);
      cur /= 1000;
      cur += Sensors[i].software_offset;
      Sensors[i].window.add(cur);
      Sensors[i].window_sum += cur;
      if (is_calibrated) {
        Sensors[i].window_sum -= Sensors[i].window[0];
        Sensors[i].window.removeFirst();
        Sensors[i].capacitance = Sensors[i].window_sum / MAX_WINDOW;
      }
    }
  }
}

void calibrate() {
  for(int i=0;i<MAX_WINDOW;i++) {
    update_measurement();
  }
  is_calibrated = true;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  calibrate();
}

void debug() {
  // long t = millis();
  // String debug_text = String(t) + '|';
  String debug_text;
  for(int i=0;i<number_of_sensors;i++) {
    debug_text = (Sensors[i].capacitance + Sensors[i].software_offset);
  }
  Serial.println(debug_text);
}

void ZeroScale() {


  for(int i=0;i<number_of_sensors;i++) {
    while(abs(Sensors[i].capacitance) > 2000) {
      if (Sensors[i].capacitance > 2000) hardware_offset++;
      else if (Sensors[i].capacitance < -2000) hardware_offset--;
      calibrate();
    }
  }
  
}

void loop() {
  update_measurement();
  debug();
  if (analogRead(A0) > 200) {
    ZeroScale();
  }
}

