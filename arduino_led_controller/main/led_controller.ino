
void led_on()
{
  
  FastLED.show();
  delay(30); 
}

void column(int start_led, int end_led, int colour)
{
  for (int i = start_led; i < end_led; i++)
  {
    leds[i] = colour;
   
  } 
  led_on();
}


