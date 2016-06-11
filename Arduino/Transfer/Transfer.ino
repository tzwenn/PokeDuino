#include "GameLink.h"

#include <EEPROM.h>

#include "pokemon.h"
#include "output.h"

volatile int counter = 0;
volatile connection_state_t connection_state = NOT_CONNECTED;
volatile trade_centre_state_t trade_centre_state = INIT;

int trade_pokemon = -1;

uint8_t PokemonCommunication(uint8_t in) {
  uint8_t send = 0x00;

  switch(connection_state) {
    case NOT_CONNECTED:
      if(in == PKMN_MASTER)
        send = PKMN_SLAVE;
      else if(in == PKMN_BLANK)
        send = PKMN_BLANK;
      else if(in == PKMN_CONNECTED) {
        send = PKMN_CONNECTED;
        connection_state = CONNECTED;
      }
      break;
  
    case CONNECTED:
      if(in == PKMN_CONNECTED)
        send = PKMN_CONNECTED;
      else if(in == PKMN_TRADE_CENTRE)
        connection_state = TRADE_CENTRE;
      else if(in == PKMN_COLOSSEUM)
        connection_state = COLOSSEUM;
      else if(in == PKMN_BREAK_LINK || in == PKMN_MASTER) {
        connection_state = NOT_CONNECTED;
        send = PKMN_BREAK_LINK;
      } else {
        send = in;
      }
      break;
  
    case TRADE_CENTRE:
      if(trade_centre_state == INIT && in == 0x00) {
        trade_centre_state = READY_TO_GO;
        send = 0x00;
      } else if(trade_centre_state == READY_TO_GO && in == 0xFD) {
        trade_centre_state = SEEN_FIRST_WAIT;
        send = 0xFD;
      } else if(trade_centre_state == SEEN_FIRST_WAIT && in != 0xFD) {
                          // random data of slave is ignored.
        send = in;
        trade_centre_state = SENDING_RANDOM_DATA;
      } else if(trade_centre_state == SENDING_RANDOM_DATA && in == 0xFD) {
        trade_centre_state = WAITING_TO_SEND_DATA;
        send = 0xFD;
      } else if(trade_centre_state == WAITING_TO_SEND_DATA && in != 0xFD) {
        counter = 0;
        // send first byte
        send = pgm_read_byte(&(DATA_BLOCK[counter]));
        INPUT_BLOCK[counter] = in;
        trade_centre_state = SENDING_DATA;
        counter++;
      } else if(trade_centre_state == SENDING_DATA) {
        // if EEPROM is not initialised, please use the pgm data only.
        /*if (counter == 12) {
          send = EEPROM.read(0); // pokemon species
        } else if(counter >= 19 && counter < 19+44) {
          send = EEPROM.read(counter-19); // pokemon data
        } else if(counter >= 283 && counter < 283+11) {
          send = EEPROM.read((counter-283)+44); // trainer name
        } else if(counter >= 349 && counter < 349+11) {
          send = EEPROM.read((counter-349)+44+11); // nickname
        } else {*/
          send = pgm_read_byte(&(DATA_BLOCK[counter]));
        //}
        INPUT_BLOCK[counter] = in;
        counter++;
        if(counter == PLAYER_LENGTH) {
          trade_centre_state = SENDING_PATCH_DATA;
        }
      } else if(trade_centre_state == SENDING_PATCH_DATA && in == 0xFD) {
        counter = 0;
        send = 0xFD;
      } else if(trade_centre_state == SENDING_PATCH_DATA && in != 0xFD) {
        send = in;
        counter++;
        if(counter == 197) {
          trade_centre_state = TRADE_PENDING;
        }
      } else if(trade_centre_state == TRADE_PENDING && (in & 0x60) == 0x60) {
        if (in == 0x6f) {
          trade_centre_state = READY_TO_GO;
          send = 0x6f;
        } else {
          send = 0x60; // first pokemon
          trade_pokemon = in - 0x60;
        }
      } else if(trade_centre_state == TRADE_PENDING && in == 0x00) {
        send = 0;
        trade_centre_state = TRADE_CONFIRMATION;
      } else if(trade_centre_state == TRADE_CONFIRMATION && (in & 0x60) == 0x60) {
        send = in;
        if (in  == 0x61) {
          trade_pokemon = -1;
          trade_centre_state = TRADE_PENDING;
        } else {
          trade_centre_state = DONE;
        }
      } else if(trade_centre_state == DONE && in == 0x00) {
        send = 0;
        trade_centre_state = INIT;
      } else {
        send = in;
      }
      break;
  
    default:
      send = in;
      break;
  }

  return send;
}


void setup()
{
  Serial.begin(115200);
  Serial.write("Restarted!\n");
  GameLink::setup(PokemonCommunication);
}

void loop()
{
  ;;	
}
