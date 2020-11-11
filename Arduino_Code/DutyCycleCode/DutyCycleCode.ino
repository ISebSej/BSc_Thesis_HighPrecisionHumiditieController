/*  rcTiming.ino -- JW, 30 November 2015 -- 
 * Uses pin-change interrupts on A0-A4 to time RC pulses
 *
 * Ref: http://arduino.stackexchange.com/questions/18183/read-rc-receiver-channels-using-interrupt-instead-of-pulsein
 *
 */
#include <Streaming.h>
#include <SPI.h>
static   byte rcOld;        // Prev. states of inputs
volatile unsigned long rcRises[4]; // times of prev. rising edges
volatile unsigned long rcTimes[4]; // recent pulse lengths
volatile unsigned long rcPulse[4]; // recent pulse lengths
volatile unsigned int  rcChange=0; // Change-counter
unsigned long int stoptime = 5000;
unsigned long int switchtime = 8000;
bool SCLl = false;
int LOAD_PIN = 7;
float RH, Te, Pr;

// Be sure to call setup_rcTiming() from setup()
void setup_rcTiming() {
  rcOld = 0;
  pinMode(A0, INPUT);  // pin 14, A0, PC0, for pin-change interrupt
  pinMode(A1, INPUT);  // pin 15, A1, PC1, for pin-change interrupt
  PCMSK1 |= 0x01;       // One-bit mask for one channels
  PCIFR  |= 0x02;       // clear pin-change interrupts if any
  PCICR  |= 0x02;       // enable pin-change interrupts
}
// Define the service routine for PCI vector 1
ISR(PCINT1_vect) {
  byte rcNew = PINC & 15;   // Get low 1 bits, A0
  byte changes = rcNew^rcOld;   // Notice changed bits
  byte channel = 0;
  unsigned long now = micros(); // micros() is ok in int routine
  while (changes) {
    if ((changes & 1)) {  // Did current channel change?
      if ((rcNew & (1<<channel))) { // Check rising edge
        rcTimes[channel] = now-rcRises[channel];    
      } else {              // Is falling edge
        rcPulse[channel] = now - rcRises[channel];
        rcRises[channel] = now; // Is Falling edge
      }
    }
    changes >>= 1;      // shift out the done bit
    ++channel;
    ++rcChange;
  }
  rcOld = rcNew;        // Save new state
}


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
   char outstr[4];
   uint8_t digit = 0x04;
   uint8_t segment;
   int ind;
   if (number < 10.0){
   dtostrf(number,4,2,outstr);
   ind = 0;
   }
   else{
   dtostrf(number,4,1,outstr);
   ind = 1;
   }
   
   for(int i; outstr[i]; i++){

    if (outstr[i] == '0'){
      segment = 0x00;
      digit--;
    }    
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
    }

    if (ind == i){
        segment += 0xA0;
      }
    maxTransfer(digit, segment);
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

  writeText(0.00);
  //setup serial
  Serial.begin(115200);
  Serial.println("Starting RC Timing Test");
  setup_rcTiming();

}


void loop() {
  
  unsigned long rcT; // copy of recent pulse lengths
  unsigned long rcR; // copy of recent pulse lengths
  unsigned long rcP; // copy of recent pulse lengths
  unsigned int rcN, rawPres;
  float duty;
  if (rcChange) {

    // Data is subject to races if interrupted, so off interrupts
    cli();          // Disable interrupts
    rcN = rcChange;
    rcChange = 0;       // Zero the change counter
    rcT = rcTimes[0];
    rcR = rcRises[0];
    rcP = rcPulse[0];
    duty = (((float)rcP - (float)rcT)) /  (float)rcP;
    RH  = -6.0 + 125.0 * duty;
    Te  = -46.85 + 175.72 * duty;
    sei();          // reenable interrupts

    rawPres = analogRead(A1);
    Pr = rawPres * 10.0 / 1024.0;
    
    //Serial << " " << Te   << " C"  << " "  << rcT
    //   << " " << rcR << " " << duty << " " << Pr << endl;
    /*if (millis() > switchtime){
      SCLl = !SCLl;
      if(SCLl){
        digitalWrite(8, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(2, LOW);
        Serial << "SWITCH"<< endl;

      }else{
        digitalWrite(8, LOW);
        digitalWrite(4, LOW);
        digitalWrite(2, HIGH);
        Serial << "switch" << endl;
      }
      switchtime += 15000;
      stoptime += 1000;
      }*/
      
      }
     cli();     
    if(millis() > stoptime){
      if (SCLl){
       
        Serial << " " << stoptime << " " << duty * 100<< " RH " << RH << " " << millis()<< endl;
        writeText(RH);
      }
      else{
        digitalWrite(8, LOW);
        Serial << " " << stoptime << " " << duty * 100<< " TE " << Te << " " << millis()<< endl;
        writeText(Te);
        }
        stoptime = millis() + 1000;
    
    }
     sei();           // reenable interrupts
}
