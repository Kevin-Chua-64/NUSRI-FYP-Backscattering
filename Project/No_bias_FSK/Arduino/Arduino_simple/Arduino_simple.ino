#include <TimerOne.h>
#include <MsTimer2.h>

// unsigned long -> 32 bit
// unsigned int  -> 16 bit

// preamble with Hamming code
unsigned long preamble = 0b1111100110101;
unsigned long data = 0b00000000000000010000011010001100; // Addr: 1, temp: 26
int data_length = 32;
int bit_rate = 40;
int f_0 = 70;
int f_1 = 150;


// // low frequency check
// unsigned long data = 0xcccc5555;
// int data_length = 32;
// int bit_rate = 1;
// int f_0 = 5;
// int f_1 = 10;

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
  static int i = 1;
  static boolean j = 1; // 1: preamble, 0: data

  if (j) {
    if (!((preamble>>(13-i)) & 1))
      Timer1.setPeriod(500000/f_0);
    else if ((preamble>>(13-i)) & 1)
      Timer1.setPeriod(500000/f_1);

    if (i == 13) {
      i = 1;
      j = !j;
    } else i++;
  }
  else {
    if (!((data>>(data_length-i)) & 1))
      Timer1.setPeriod(500000/f_0);
    else if ((data>>(data_length-i)) & 1)
      Timer1.setPeriod(500000/f_1);

    if (i == data_length) {
      i = 1;
      j = !j;
    } else i++;
  }
}
