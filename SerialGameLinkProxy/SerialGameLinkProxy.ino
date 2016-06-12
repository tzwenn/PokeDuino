#include "GameLink.h"

const long BAUDRATE = 115200;

uint8_t SerialGameLinkProxy(uint8_t serial_out)
{
  static volatile int serial_in = 0;
  serial_in = Serial.read();
  Serial.write(serial_out);
  return serial_in;
}

void setup()
{
  Serial.begin(BAUDRATE);
  GameLink::setup(SerialGameLinkProxy);
}

void loop()
{
  ;;	
}
