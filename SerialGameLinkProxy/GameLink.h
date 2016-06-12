#pragma once

#include <stdint.h>

namespace GameLink {

	typedef uint8_t(*ReceivedByteCallback)(uint8_t data);

	void setup(ReceivedByteCallback callback);
	unsigned long microsSinceLastReceive();

}
