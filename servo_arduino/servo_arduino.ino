#include <Servo.h>

Servo pan_servo;
Servo tilt_servo;

String str;

int pan_angle;
int tilt_angle;

int min_pulse = 544; //Default: 544, SG90: 500
int max_pulse = 2400; // Default: 2400, SG90: 2500

void setup() {
  // put your setup code here, to run once:
   Serial.begin(115200);
   pan_servo.attach(9, min_pulse, max_pulse);
   tilt_servo.attach(10, min_pulse, max_pulse);
   Serial.println(pan_servo.read());
   Serial.println(tilt_servo.read());

}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()==0){
  }
  
  str = Serial.readStringUntil('!');
  str.trim();
  if(str!=""){
    if(str.endsWith("x")){
      pan_angle = str.toInt();
      pan_servo.write(pan_angle);
      //Serial.println(pan_servo.readMicroseconds());
      }
      if(str.endsWith("y")){
      tilt_angle = str.toInt();
      tilt_servo.write(tilt_angle);
      //Serial.println(tilt_servo.readMicroseconds());
      }
  }
  

}
