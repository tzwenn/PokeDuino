#include "GameLink.h"
#include <Arduino.h>

/*
  Name ArduinoPin Color
 ---------------------------------------------
  GND  GND        Blue
  SOut 6          Orange   (Red@GB)
  SIn  3          Red      (Orange@GB)
  SClk 2          Green
  
  Note: SOut and SIn are crossed.
        Colors refer to what is connected at arduino end.
*/

namespace GameLink {

static const int timeout_us = 120;

static volatile uint8_t _in;
static volatile uint8_t _out;
static volatile unsigned long _lastReceive = 0;

static ReceivedByteCallback _callback;

enum PIN {
	clk = 2,
	in  = 3,
	out = 6
};

static void externalClockTick()
{
  static volatile int _currentBit = 0;
	
  if (_lastReceive > 0 && microsSinceLastReceive() > timeout_us) {
    _in = 0;
    _currentBit = 0;
  }

  _in <<= 1;
	_in |= (digitalRead(PIN::in) == HIGH);
	
  if (++_currentBit >= 8) {
    _out = _callback(_in);
    _in = 0;
    _currentBit = 0;
  }
  
  _lastReceive = micros();
  while (digitalRead(PIN::clk) != HIGH);
	
  digitalWrite(PIN::out, _out & 0x80 ? HIGH : LOW);
	_out <<= 1;
}

///////////////////////////////////////////////////////////////////////

void setup(ReceivedByteCallback callback)
{
	_in = _out = 0;
	_callback = callback;

	pinMode(PIN::clk, INPUT);
	pinMode(PIN::in,  INPUT);
	pinMode(PIN::out, OUTPUT);

	digitalWrite(PIN::in, LOW);
	attachInterrupt(digitalPinToInterrupt(PIN::clk), externalClockTick, RISING);
}

unsigned long microsSinceLastReceive()
{
  return micros() - _lastReceive;
}

}; // namespace GameLink

