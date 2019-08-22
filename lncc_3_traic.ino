#include <OneWire.h>
#include <DallasTemperature.h>
#include <Servo.h>

#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
Servo portinholaMotor;

const int coolerPin = 3;
const int triacPin = 9;
const int portinholaPin = 8;
//teste

bool flag = false;
String serialBuffer = "0";
int triacValue = 0;
int coolerValue = 0;
int portinholaValue = 0;


//SETUP
void setup() {
  pinMode(triacPin, OUTPUT);
  pinMode(coolerPin, OUTPUT);
  pinMode(portinholaPin, OUTPUT);
  portinholaMotor.attach(portinholaPin);
  pwm25kHzBegin();
  Serial.begin(9600);
  sensors.begin();
}


//MAIN
void loop() {
  
  sensors.requestTemperatures();
  Serial.println(sensors.getTempCByIndex(0));
  int encodedInt = receiver();
  processActuators(encodedInt);
}
//END MAIN


int receiver()
{ 
  //if (Serial.available()) {
  //  serialBuffer = "0";
  //  while (Serial.available())  {
  //    if (Serial.available() > 0) {
  //      flag = true; char c = Serial.read(); serialBuffer += c;
  //    }
  //  }
  //}
  serialBuffer = "010020030"
  int encoded = serialBuffer.toInt();
  return encoded;
}

void processActuators(int encodedInt){
  decodeData(encodedInt);
  actuatorsActivator();
}

void actuatorsActivator() {
    analogWrite(triacPin, triacValue);
    velocidadeDoCooler(coolerValue);// 25%= 19, 50%=39, 75%=59. 100%=79
    portinholaMotor.write(portinholaValue); 
}

void decodeData(int encodedInt){
  triacValue = (encodedInt / 1000000);
  coolerValue = ((encodedInt - (triacValue * 1000000) ) / 1000);
  portinholaValue = (encodedInt - ( (triacValue * 1000000) + (coolerValue * 1000) )   );
}

void pwm25kHzBegin() {
  TCCR2A = 0; TCCR2B = 0; TIMSK2 = 0; TIFR2 = 0;                                
  TCCR2A |= (1 << COM2B1) | (1 << WGM21) | (1 << WGM20);  
  TCCR2B |= (1 << WGM22) | (1 << CS21);     
  OCR2A = 79;                               
  OCR2B = 0;
}
 
void velocidadeDoCooler(byte ocrb) {
  OCR2B = ocrb;                             // PWM Width (duty)
}
