#include <thermistor.h>
#define LUZ1 7           //Quarto
#define LUZ2 13          // Closet
#define LUZ3 2           //Banheiro
#define LDR_QUARTO A5
#define LDR A4
THERMISTOR thermistor(LDR, 10000, 3950, 10000);
int sinal, S_LDR_QUARTO, temperature;
void setup() {
  Serial.begin(115200);
    pinMode(LUZ1,OUTPUT);
  pinMode(LUZ2,OUTPUT);
  pinMode(LUZ3,OUTPUT);
  
}

// EDITAR!!!
void loop() {
  S_LDR_QUARTO = analogRead(LDR_QUARTO);
  sinal = Serial.read();
    //Serial.println(S_LDR_QUARTO);

  if (sinal != -1){
  //Serial.println(S_LDR_QUARTO);

  switch (sinal){
    case 49:                                //1
      digitalWrite(LUZ1,!digitalRead(LUZ1));
      break;
    case 51 :                               //3
      digitalWrite(LUZ2,!digitalRead(LUZ2));
      break;
   case 53:                                 //5
      digitalWrite(LUZ3,!digitalRead(LUZ3));
      break;

   case 115:
      if (S_LDR_QUARTO > 600){
        Serial.println("0");
      }else{
        Serial.println("1");
        }
   break;
   case 52:              //4     
    int temperature = thermistor.read();
    Serial.println(temperature);
    break;
  }
  }
}
