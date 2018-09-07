#include <FastLED.h>

int button_state = 0;
float data[4];
int led_array[12][12];


#define button_mode 10
#define COLUMNS 12
#define BLUE 0x0000FF
#define BLACK 0x000000
#define DATA_PIN 3
#define NUM_LEDS 144

CRGB leds[NUM_LEDS];

void set_led_array()
{
  int counter = 0;
  
  for (int i = 0; i < 12; i++)
  {
    for (int j = 0; j < 12; j++)
    {
      led_array[j][i] = counter;
      counter++;
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  set_led_array();
  Serial.begin(9600);
  pinMode(button_mode, INPUT);
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  while (!Serial) {
    ; //wait for serial to connect properly
  }
}

void debug(char* message)
{
  Serial.print(message);
  Serial.print("\n\r");
}

void get_mode() {
  //debug("in button mode select");
  if (button_mode == 1)
  {
    if (button_state < 3) {
      button_state += 1;
    } else if (button_state == 3) {
      button_state = 0;
    }
  }
}

void piano_mode_1(int colour)
{
  //debug("in piano");
  //Serial.println(led_array[0][data[0]]);
  //Serial.println(led_array[11][data[0]]);
  
  column(led_array[0][(int)data[0]], led_array[11][(int)data[0]], colour);
  //delay(30);
  FastLED.clear();
}

void hue_mode()
{
  
}

void snake_mode(int colour)
{
  //led_on(led_array[data[1]][data[0]], colour);
}

/*
void connect4_mode()
{
  int start_state = 0;
  int gameover = 0;
  int change_x = 0;
  
  while (start_state == 0)
  {
    number_four(GREEN);
    if (data[0] == 5)
    {
      start_state = 1;
      FastLED.clear();
    }
  }

  while(!gameover)
  {
    led_on(data[0] * 12, PINK);
  }
}

*/


void serial_poll1() 
{
 // debug("in serial event");
  int i = 0;

  while (i < 4)
  {
    if (Serial.available()){
      data[i] = Serial.parseFloat();
      i++;
    }
    
  }
  debug("complete");
}

//void test()
//{
//  debug("in test");
//  if ((int)data[0] == 8)
//  {
//    debug("turning on");
//    leds[0] = BLUE;
//    FastLED.show();
//    delay(30);
//  } else {
//    debug("off");
//    off();
//  }
//}

void off()
{
  for (int i = 0; i < 144; i++)
  {
    leds[i] = BLACK;
    FastLED.show();
    delay(30);
  }
}

void loop() {
  // put your main code here, to run repeatedly: 
//  Serial.println(data[0]);
//Serial.println(data[1]);
//Serial.println(data[2]);
//Serial.println(data[3]);
//// get_mode();
//  serial_poll1();
//  leds[0] = BLUE;
//  FastLED.show();
//  test();
  int i = 0;
  if (Serial.available()) {
    i = Serial.parseInt();
    Serial.println(i);
    leds[i] = BLUE;
    FastLED.show();
  }
  /*
 
  switch (button_state)
  {
    case (0):
      piano_mode_1(BLUE);
      break;
    case (1):
      hue_mode();
      break;
    case (2):
      snake_mode(BLUE);
      break;
  }
  */

  //column(0, 4, BLUE);
}
