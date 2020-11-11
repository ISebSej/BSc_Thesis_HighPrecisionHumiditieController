#include <SPI.h>
//https://gist.github.com/nrdobie/8193350
// What pin on the Arduino connects to the LOAD/CS pin on the MAX7219/MAX7221
int LOAD_PIN = 7;

const int pinSDA = A0;
const int pinSIG = A1;
const int pinSCL = 8;

bool seriall   = true;
bool SCLselect = true;
int rawSIG;
int rawSCL;

bool dot;




void maxTransfer(uint8_t address, uint8_t value) {

  // Ensure LOAD/CS is LOW
  digitalWrite(LOAD_PIN, LOW);

  // Send the register address
  SPI.transfer(address);

  // Send the value
  SPI.transfer(value);

  // Tell chip to load in data
  digitalWrite(LOAD_PIN, HIGH);
}


void writeText(float number){
   dot = false;
   char outstr[4];
   uint8_t digit = 0x03;
   uint8_t segment;
   if (number < 10.0){
   dtostrf(number,4,2,outstr);
   }
   else{
   dtostrf(number,4,1,outstr);
   }
   
   for(int i; outstr[i]; i++){

     Serial.println(outstr[i]);
    
    if (outstr[i] == '1'){
      segment = 0x01;
      digit--;
    }
    if (outstr[i] == '2'){
      segment = 0x02;
      digit--;
    }
    if (outstr[i] == '3'){
      segment = 0x03;
      digit--;
    }
    if (outstr[i] == '4'){
      segment = 0x04;
      digit--;
    }
    if (outstr[i] == '5'){
      segment = 0x05;
      digit--;
    }
    if (outstr[i] == '6'){
      segment = 0x06;
      digit--;
    }
    if (outstr[i] == '7'){
      segment = 0x07;
      digit--;
    }
    if (outstr[i] == '8'){
      segment = 0x08;
      digit--;
    }
    if (outstr[i] == '9'){
      segment = 0x09;
      digit--;
    }
    if (outstr[i] == '.'){     
    dot = true;  
    }
    if (dot){
      segment = segment +  0x00;
      }
    maxTransfer(digit, segment);
     Serial.print(segment);
     Serial.println(digit);
   }
}




void setup() {

  // Set load pin to output
  pinMode(LOAD_PIN, OUTPUT);

  // Reverse the SPI transfer to send the MSB first  
  SPI.setBitOrder(MSBFIRST);
  
  // Start SPI
  SPI.begin();
  // Run test
  // All LED segments should light up
  maxTransfer(0x0F, 0x01);
  delay(1000);
  maxTransfer(0x0F, 0x00);
  // Enable mode B
  maxTransfer(0x09, 0xFF);
  // Use lowest intensity
  maxTransfer(0x0A, 0x05);
  // Only scan one digit
  maxTransfer(0x0B, 0x02);
  // Turn on chip
  maxTransfer(0x0C, 0x01);
  //SCL pin preset
  pinMode(pinSCL, OUTPUT); 
  pinMode(2, OUTPUT); 
  
  if(seriall){
  Serial.begin(9600);
  Serial.println("Start");
  writeText(12.4);
  }
}




void loop() {
  // put your main code here, to run repeatedly:
  // Read Sensors
  
   // Loop through each code
  if(SCLselect){
    digitalWrite(pinSCL, HIGH);
    digitalWrite(2, HIGH);
     Serial.print("HI ");
  }else{
    digitalWrite(pinSCL, LOW);
    digitalWrite(2, LOW);
     Serial.print("LO ");
  }
  /*for (uint8_t i = 0; i < 0x10; ++i)
  { 
    maxTransfer(0x01, i);
    maxTransfer(0x02, i);
    delay(300);
  }*/
    rawSIG = analogRead(pinSIG);
    rawSCL = analogRead(pinSDA);
    if(seriall){
      // Send to terminal
      Serial.print("A1 = ");
      float voltage = rawSIG * (5.0 / 1023.0);
      Serial.print(voltage);
      Serial.print(" A0 = ");
      voltage = rawSCL * (5.0 / 1023.0);
      Serial.println(voltage);
      }
  SCLselect = !SCLselect;
  delay(5000);
  }

  //https://arduino.stackexchange.com/questions/18183/read-rc-receiver-channels-using-interrupt-instead-of-pulsein/18221#18221
  
