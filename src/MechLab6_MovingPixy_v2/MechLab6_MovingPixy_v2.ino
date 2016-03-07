//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//
// This sketch is a good place to start if you're just getting started with 
// Pixy and Arduino.  This program simply prints the detected object blocks 
// (including color codes) through the serial console.  It uses the Arduino's 
// ICSP port.  For more information go here:
//
// http://cmucam.org/projects/cmucam5/wiki/Hooking_up_Pixy_to_a_Microcontroller_(like_an_Arduino)
//
// It prints the detected blocks once per second because printing all of the 
// blocks for all 50 frames per second would overwhelm the Arduino's serial port.
//

int X_CENTER=160;
int X_MAX=319;
int X_MIN=0;
int SERVO_MAX=160;
int SERVO_MIN=20;
int servoPos=0;
int prev_servoPos=0;

bool atPodium;
int leftPodium;
int podiumThresh=40;

#include <SPI.h>  
#include <Pixy.h>
#include <Servo.h>

Servo myservo;

// This is the main Pixy object 
Pixy pixy;

void setup()
{
  Serial.begin(9600);
  Serial.print("Starting...\n");
  myservo.attach(9);
  pixy.init();
}

void loop()
{ 
  // grab blocks!
  uint16_t blocks = pixy.getBlocks();
  // If there are detect blocks, print them!
  if (blocks)
  {
    servoTrack(pixy.blocks[0].x);
    if(servoPos > podiumThresh && atPodium) {
      leftPodium++;
      Serial.println("Left podium.");
      Serial.print("Times left: ");
      Serial.println(leftPodium);
      atPodium = false; 
    } else if (servoPos <= podiumThresh && !atPodium) {
      atPodium = true;
    }
    prev_servoPos=servoPos;
  }  
}

void servoTrack(int pixy_x_position){
  int error = X_CENTER-pixy_x_position;
  
  
  if(error<-30){
    servoPos+=5;
    //Serial.println("Get Here top if");
    if (servoPos>SERVO_MAX){ 
      servoPos=SERVO_MAX; 
    }
  }
  else if(error>+30){
    servoPos-=5;
    //Serial.println("Get Here bottom if");
    if (servoPos<SERVO_MIN){
    servoPos=SERVO_MIN;
    }
  }
  myservo.write(servoPos);
  //Serial.print("Servo Command: ");
  //Serial.println(servoPos);
  /*if(servoPos!=prev_servoPos){
    Serial.print("Servo Command: ");
    Serial.println(servoPos);
    // 
  }*/
  delay(15);
}

