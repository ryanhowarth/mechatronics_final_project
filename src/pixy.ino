#include <SPI.h>  
#include <Pixy.h>

// This is the main Pixy object 
Pixy pixy;

int tree=8;
int gift=9;
int sig;

void setup() {
  // put your setup code here, to run once:
  pinMode(tree,OUTPUT);
  pinMode(gift,OUTPUT);

//  Serial.begin(9600);
//  Serial.print("Starting...\n");

  pixy.init();
}

void loop() {
  // put your main code here, to run repeatedly:
  static int i = 0;
  static int k = 0;
  int j;
  uint16_t blocks;
  char buf[32]; 
  
  // grab blocks!
  blocks = pixy.getBlocks();
  //Serial.print(blocks);
  if(blocks==0)
  {
    k+=1;
    if (k==5000)
    {
      k=0;
      //Serial.print("set low\n");
      digitalWrite(tree, LOW);
      digitalWrite(gift, LOW); 
    }
  }
  else
    k=0;
    
  // If there are detect blocks, print them!
  if (blocks)
  {
    i++;

    // do this (print) every 50 frames because printing every
    // frame would bog down the Arduino
    if (i%50==0)
    {
      //sprintf(buf, "Detected %d:\n", blocks);
      //Serial.print(buf);
      //Serial.print("set high\n");
      for (j=0; j<blocks; j++)
      {
        sig=pixy.blocks[j].signature;
        //Serial.print("sig=");
        //Serial.print(sig);
        //Serial.print('\n');
        if(sig==1)
        {
          //Serial.print("1\n");
          digitalWrite(tree, HIGH);//tree, sig=1
        }
        else if(sig==2)
        {
          //Serial.print("2\n");
          digitalWrite(gift, HIGH);//gift, sig=2  
        }
        break;
        delay(50);
      }
    }
  }
/*
  else
  {
    i++;
    if (i%50==0)
    {
      Serial.print("set low\n");
      digitalWrite(tree, LOW);
      digitalWrite(gift, LOW);  
    }
    //digitalWrite(tree, LOW);
    //digitalWrite(gift, LOW); 
  }
*/  
}
