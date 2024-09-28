#include "/home/jonas/SmartGrow/repo/miflora-esp32/lib/control/control.h"


// Define the pumps to cON"trol
const int pump1 = 3;
const int pump2 = 4;
const int pump3 = 2;
const int pump4 = 7;
const int pump5 = 6;
const int pump6 = 5;

void setup() {

  pinMode(pump1, OUTPUT);
  pinMode(pump2, OUTPUT);
  pinMode(pump3, OUTPUT);
  pinMode(pump4, OUTPUT);
  pinMode(pump5, OUTPUT);
  pinMode(pump6, OUTPUT);

  digitalWrite(pump1, LOW);
  digitalWrite(pump2, LOW);
  digitalWrite(pump3, LOW);
  digitalWrite(pump4, LOW);
  digitalWrite(pump5, LOW);
  digitalWrite(pump6, LOW);

  Serial.begin(115200);
}

String receivedCommand = ""; 

void loop() {
  while (Serial.available() > 0) {
    char inChar = Serial.read();   // Read each character

    // Append each character to the receivedCommand string
    if (inChar != '\n') {  // Until a newline is received
      receivedCommand += inChar;
    } else {
      // Handle the received command
      receivedCommand.trim();
      handleCommand(receivedCommand);

      // Clear the command string after processing
      receivedCommand = "";
    }
  }
}

// FunctiON" to handle received commands

void handleCommand(String command) {
      Serial.println(command);

      if(command ==  "CMD_PUMP1_ON"){// Turn pump 2 ON"
        digitalWrite(pump1, HIGH);
        Serial.println("ACK_PUMP1_ON");
      }

      else if(command ==  "CMD_PUMP1_OFF"){ // Turn pump 2 OFF"
        digitalWrite(pump1, LOW);
        Serial.println("ACK_PUMP1_OFF");
      }

      else if(command ==  "CMD_PUMP2_ON"){// Turn pump 3 ON"
        digitalWrite(pump2, HIGH);
        Serial.println("ACK_PUMP2_ON");
      }

      else if(command ==  "CMD_PUMP2_OFF"){ // Turn pump 3 OFF"
        digitalWrite(pump2, LOW);
        Serial.println("ACK_PUMP2_OFF");
      }

      else if(command ==  "CMD_PUMP3_ON"){// Turn pump 4 ON"
        digitalWrite(pump3, HIGH);
        Serial.println("ACK_PUMP3_ON");
      }

      else if(command ==  "CMD_PUMP3_OFF"){ // Turn pump 4 OFF"
        digitalWrite(pump3, LOW);
        Serial.println("ACK_PUMP3_OFF");
      }

      else if(command ==  "CMD_PUMP4_ON"){// Turn pump 5 ON"
        digitalWrite(pump4, HIGH);
        Serial.println("ACK_PUMP4_ON");
      }

      else if(command ==  "CMD_PUMP4_OFF"){ // Turn pump 5 OFF"
        digitalWrite(pump4, LOW);
        Serial.println("ACK_PUMP4_OFF");
      }

      else if(command ==  "CMD_PUMP5_ON"){// Turn pump 6 ON"
        digitalWrite(pump5, HIGH);
        Serial.println("ACK_PUMP5_ON");
      }

      else if(command ==  "CMD_PUMP5_OFF"){ // Turn pump 6 OFF"
        digitalWrite(pump5, LOW);
        Serial.println("ACK_PUMP5_OFF");
      }

      else if(command ==  "CMD_PUMP6_ON"){// Turn pump 7 ON"
        digitalWrite(pump6, HIGH);
        Serial.println("ACK_PUMP6_ON");
      }

      else if(command ==  "CMD_PUMP6_OFF"){ // Turn pump 7 OFF"
        digitalWrite(pump6, LOW);
        Serial.println("ACK_PUMP6_OFF");
      }

      //else
        //Serial.println(-1);
    }

