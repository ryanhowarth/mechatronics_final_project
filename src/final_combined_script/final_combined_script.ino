#include <SPI.h>  
#include <Pixy.h>
#include <Servo.h>


int seconds=0;
int backwards=0;
int forwards=0;
int pointing=0;
int leaving=0;
int LED_red=8;
int LED_yellow=6;
int LED_green=12;
int num_purple = 0;
int num_red = 0;
int num_yellow =0;
unsigned long time_elapse=0;
unsigned long start_time;
//boolean forwards_state=false;
boolean curr_point_state = false;
boolean prev_point_state=false;//not pointing
uint16_t blocks;
Pixy pixy;

// Variables for servo tracking
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
Servo myservo;





// This is the main Pixy object 


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("Starting...\n");
  myservo.attach(9);
  pixy.init();
  start_time=millis();
  pinMode(LED_red, OUTPUT);
  pinMode(LED_yellow, OUTPUT);
  pinMode(LED_green, OUTPUT);
  digitalWrite(LED_red, LOW);
  digitalWrite(LED_yellow, LOW);
  digitalWrite(LED_green, LOW);
}

void loop() {
    //int randAngle;
    int blocks_num;
    static int i = 0;
    int j;
    static int signature;

    blocks = pixy.getBlocks();
    if (blocks)
    {

        i++;
        for(int l =0; l<blocks; l++)
        {
          signature=(pixy.blocks[l].signature);
          if(signature ==1)
          {            
            num_red+=1;
          }
          if(signature ==2)
          {
          num_yellow +=1;
          }
          if(signature ==3) 
          {
          num_purple +=1;
          }
          if (signature==1 || signature==2) {
            servoTrack(pixy.blocks[l].x);
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
    // do this (print) every 50 frames because printing every
    // frame would bog down the Arduino
    if (i%50==0)
    {
      //randAngle = random(0, 180);
      
      if(num_red > 10)//red
      {
        backwards+=1;
        Serial.println("facing backwards");
       }
       if(num_yellow >10)//yellow 
      {
            forwards+=1;
            Serial.println("facing forwards");
      }
      if(num_purple > 10)
      {
            curr_point_state=true;//set
            
      }
      else
      {
        curr_point_state = false;
      }

      if(curr_point_state)//pointing
      {
          if(prev_point_state)//previously pointing
          { Serial.println("continue pointint");}//do nothing
          else//previously not pointing
          {
            Serial.println("start pointing");
              pointing+=1;
          }
          
          
       }
       else//not pointing
       {
          Serial.println("not pointing");
       }
       



         prev_point_state = curr_point_state;
         num_purple = 0;
        num_red = 0;
        num_yellow =0;    
    }
    
  }
    
    time_elapse=millis()-start_time;
     seconds=time_elapse/1000;
     if(time_elapse>=60000)//per 60 sec
     {
          Serial.print("% of time facing forwards = ");
          Serial.println((float)forwards/((float)(forwards+backwards))*100);
          Serial.print("number of times pointing = ");
          Serial.println(pointing);
          Serial.print("number of times leaving = ");
          Serial.println(leftPodium);
          digitalWrite(LED_red, LOW);
          digitalWrite(LED_yellow, LOW);
          digitalWrite(LED_green, LOW);
          if(forwards==0)
          {
                digitalWrite(LED_red, HIGH);
          }
          if(pointing==0)
          {
                digitalWrite(LED_yellow, HIGH);
          }
          if(leaving==0)
          {
                digitalWrite(LED_green, HIGH);
           }
//seconds=0;
          forwards=0;
          backwards=0;
          pointing=0;
          leaving=0;
          start_time=millis();
          num_purple = 0;
          num_red = 0;
          num_yellow = 0;
      }
      //Serial.print("seconds =");
      //Serial.println(seconds);
      
}

void servoTrack(int pixy_x_position){
  int error = X_CENTER-pixy_x_position;
  
  
  if(error<-30){
    servoPos+=3;
    //Serial.println("Get Here top if");
    if (servoPos>SERVO_MAX){ 
      servoPos=SERVO_MAX; 
    }
  }
  else if(error>+30){
    servoPos-=3;
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


