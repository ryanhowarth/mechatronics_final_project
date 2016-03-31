#include <SPI.h>
#include <Pixy.h>
#include <Servo.h>


int seconds = 0;
int backwards = 0;
int forwards = 0;
int pointing = 0;

// Define LED pins
#define LED_red 8
#define LED_yellow 6
#define LED_green 12

// Define color signatures
#define redSig 1
#define yellowSig 2
#define purpleSig 3

int num_purple = 0;
int num_red = 0;
int num_yellow = 0;
unsigned long time_elapse = 0;
unsigned long start_time;
//boolean forwards_state=false;
boolean curr_point_state = false;
boolean prev_point_state = false; //not pointing
uint16_t blocks;
Pixy pixy;

// Variables for servo tracking
#define servoPin 9 // Servo library only capable on pins 9 and 10
#define X_CENTER 160
#define SERVO_MAX 160
#define SERVO_MIN 20
int servoPos = 0;
int prev_servoPos = 0;

bool atPodium = false;
int leftPodium = 0;
#define podiumThresh 40 // Greater than this angle means he has left podium
Servo myservo;

int i = 0;
int signature;

// This is the main Pixy object


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("Starting...\n");
  myservo.attach(servoPin);
  pixy.init();
  start_time = millis();

  pinMode(LED_red, OUTPUT);
  pinMode(LED_yellow, OUTPUT);
  pinMode(LED_green, OUTPUT);
  digitalWrite(LED_red, LOW);
  digitalWrite(LED_yellow, LOW);
  digitalWrite(LED_green, LOW);
}

void loop() {

  blocks = pixy.getBlocks();
  if (blocks) {

    i++;
    for (int j = 0; j < blocks; j++) {
      signature = (pixy.blocks[j].signature);
      switch (signature) {
        case redSig:
          num_red++;
          break;
        case yellowSig:
          num_yellow++;;
          break;
        case purpleSig:
          num_purple++;
          break;
      }

      if (signature == redSig || signature == yellowSig) {
        servoTrack(pixy.blocks[j].x);
        prev_servoPos = servoPos;

        if (servoPos > podiumThresh && atPodium) {
          leftPodium++;
          Serial.println("Left podium.");
          Serial.print("Times left: ");
          Serial.println(leftPodium);
          atPodium = false;
        } 
        else if (servoPos <= podiumThresh && !atPodium) {
          atPodium = true;
        }
      }

    }

    if (i % 50 == 0) {

      if (num_red > 10) {
        backwards++;
        Serial.println("facing backwards");
      }
      if (num_yellow > 10) {
        forwards++;
        Serial.println("facing forwards");
      }

      // The following line is a substitute for the following if-else statement
      // TODO: Confirm that it works
      curr_point_state = (num_purple > 10);
      /*if(num_purple > 10)
      {
            curr_point_state=true;//set

      }
      else
      {
        curr_point_state = false;
      }*/

      if (curr_point_state) { //pointing
        if (prev_point_state) { //previously pointing
          Serial.println("continue pointing"); //do nothing
        }
        else { //previously not pointing
          Serial.println("start pointing");
          pointing++;
        }

      }
      else { //not pointing
        Serial.println("not pointing");
      }

      prev_point_state = curr_point_state;
      num_purple = 0;
      num_red = 0;
      num_yellow = 0;
    }

  }

  time_elapse = millis() - start_time;
  seconds = time_elapse / 1000;
  if (time_elapse >= 60000) //per 60 sec
  {
    Serial.print("% of time facing forwards = ");
    Serial.println((float)forwards / ((float)(forwards + backwards)) * 100);
    
    Serial.print("number of times pointing = ");
    Serial.println(pointing);
    
    Serial.print("number of times leaving = ");
    Serial.println(leftPodium);
    
    digitalWrite(LED_red, LOW);
    digitalWrite(LED_yellow, LOW);
    digitalWrite(LED_green, LOW);
    
    if (forwards == 0)
    {
      digitalWrite(LED_red, HIGH);
    }
    if (pointing == 0)
    {
      digitalWrite(LED_yellow, HIGH);
    }
    if (leftPodium == 0)
    {
      digitalWrite(LED_green, HIGH);
    }
    //seconds=0;
    forwards = 0;
    backwards = 0;
    pointing = 0;
    leftPodium = 0;
    start_time = millis();
    num_purple = 0;
    num_red = 0;
    num_yellow = 0;
  }
  //Serial.print("seconds =");
  //Serial.println(seconds);

}

void servoTrack(int pixy_x_position) {
  int error = X_CENTER - pixy_x_position;


  if (error < -30) {
    servoPos += 3;

    if (servoPos > SERVO_MAX)
      servoPos = SERVO_MAX;

  }
  else if (error > +30) {
    servoPos -= 3;

    if (servoPos < SERVO_MIN)
      servoPos = SERVO_MIN;

  }

  // TODO: Confirm that this is working
  if (servoPos != prev_servoPos)
    myservo.write(servoPos);

  delay(15);
}


