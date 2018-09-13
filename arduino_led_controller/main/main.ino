#include <FastLED.h>

int mode_select = 0;
float data[4];
int led_array[12][12];

int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

#define buttonPin 10
#define COLUMNS 12
#define BLUE 0x0000FF
#define BLACK 0x000000
#define RED 0xFF0000
#define DATA_PIN 3
#define NUM_LEDS 144

#define BUFFER_SZ 30

CRGB leds[NUM_LEDS];

void set_led_array()
{
  int counter = 0;
  
  for (int i = 0; i < 12; i++)
  {
    for (int j = 0; j < 12; j++)
    {
      if (i % 2 == 0)
      {
        led_array[j][i] = counter;
        counter++;
      } else {
        led_array[abs(j-12)][i] = counter;
        counter++;
      }
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  set_led_array();
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
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

void follow_mode(int colour)
{
  int x_sum = 0;
  int y_sum = 0;
  int x_mean = 0;
  int y_mean = 0;
  

  for (int i = 0; i < 5; i++)
  {
    
    x_sum += data[0];
    
    y_sum += data[1];
  }

  x_mean = x_sum/5;
  y_mean = y_sum/5;

  Serial.println(x_mean);
  Serial.println(y_mean);
  Serial.println();
  
  leds[led_array[y_mean][x_mean]] = CRGB::Red;
  
  FastLED.show();
 FastLED.clear();
}

void asteroid_mode()
{
  
  if (data[0] == 0)
  {
    data[0] = 1;
  }
  if ((int)data[0] == 11)
  {
    data[0] = 10;
  }

  if ((int)data[3] < -50 and (int)data[3] > -130 and (int)data[2] > 3)
  {
    leds[(led_array[10][(int)data[0]])] = RED;
  }
  
  leds[(led_array[11][(int)data[0]])] = BLUE;
  leds[(led_array[11][(int)data[0] + 1])] = BLUE;
  leds[(led_array[11][(int)data[0] - 1])] = BLUE;
  leds[(led_array[10][(int)data[0]])] = BLUE;
  FastLED.show();
  FastLED.clear();
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
void parse(char *buffer)
{
    char *s = strtok(buffer, ",");
      data[0] = atof(s);
    
    s = strtok(NULL, ",");
    
      data[1] = atof(s);

    s = strtok(NULL, ",");
    data[2] = atof(s);

    s = strtok(NULL, ",");
    data[3] = atof(s);
    
}


void get_serial() 
{
 static char buffer[BUFFER_SZ];
  static size_t lg = 0;
  while (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {        // carriage return
          buffer[lg] = '\0';  // terminate the string
          parse(buffer);
          lg = 0;             // get ready for next message
      }
      else if (lg < BUFFER_SZ - 1) {
          buffer[lg++] = c;
      }
  }
}


void loop() {
  //Serial.println(mode_select);
  Serial.println(data[0]);
  //Serial.println(data[2]);
  //Serial.println(data[3]);
  get_serial();
  debounce_button();
 // test();
 if (data[0] != -1)
 {
    switch (mode_select)
    {
      case (0):
        piano_mode_1(BLUE);
        break;
      case (1):
        asteroid_mode();
        break;
      case (2):
        follow_mode(BLUE);
        break;
      case(3):
        all_off();
        break;
    }
 } else {
  FastLED.clear();
  FastLED.show();
 }
}
