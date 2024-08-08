#include <TimerOne.h>
#include <MsTimer2.h>

// unsigned long -> 32 bit
// unsigned int  -> 16 bit

// PRBS7
// period: 127
int init_state = 0b1000000;
int bit_rate = 40;
int f_0 = 70;
int f_1 = 150;


void setup() {
  // Serial.begin(9600);
  // Serial.print(data);

  pinMode(9, OUTPUT);
  digitalWrite(9,LOW);

  Timer1.initialize(500000/f_0); // initialize timer1, and set a us level period
  Timer1.attachInterrupt(flip); // attaches ISR as a timer overflow interrupt

  MsTimer2::set(1000/bit_rate, bit_switch); // ms level period
  MsTimer2::start();
}

void loop() {

}

void flip() {
  static boolean output = 0;
  digitalWrite(9, output);
  output = !output;
}

void bit_switch() {
  static int states = init_state;

  boolean output = states & 1;
  // PRBS7 = x^7 + x^6 + 1
  boolean first_bit = (states ^ (states >> 1)) & 1;
  // update state
  states = (states >> 1) | (first_bit << 6);

  if (!output)
    Timer1.setPeriod(500000/f_0);
  else if (output)
    Timer1.setPeriod(500000/f_1);


  // if (states == init_state;) { // only transmit once
  //   Timer1.stop();
  //   MsTimer2::stop();
  //   digitalWrite(9,LOW);
  // }
}
