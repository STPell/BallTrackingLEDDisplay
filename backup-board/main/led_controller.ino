void all_off()
{
  for (int i = 0; i < 144; i++)
  {
    leds[i] = BLACK;
    FastLED.show();
    delay(30);
  }
}

void led_on()
{
  
  FastLED.show();
  delay(30); 
}

void column(int num1, int num2, int colour)
{
  int start_num, end_num;
  if (num1 > num2)
  {
    end_num = num1;
    start_num = num2;
  } else
  {
    end_num = num2;
    start_num = num1;
  }
  //debug("in column");
  for (int i = start_num; i <= end_num; i++)
  {
    leds[i] = CRGB::Red;
   
  } 
  FastLED.show();
}

void test()
{
  if (data[0] == -1)
  {
    FastLED.clear();
    FastLED.show();
  }
  else
  {
    leds[(int)data[0]] = CRGB::Red;
    FastLED.show();
  }
}
