// C++ code
//
int buttonPin_SIM=3;
int buttonPin_NAO=4;
int ledPin_0=6;
int ledPin_1=7;
int ledPin_2=8;
int ledPin_3=9;
int ledPin_4=10;
int ledPin_5=11;
int numpensado;
int bit;
int mascara;
int n;


// Variáveis de Estado do Jogo
      // Valor da potência de 2 na ronda atual (32, 16, 8, 4, 2, 1).
void setup()
{
  Serial.begin(9600);
  pinMode(ledPin_0, OUTPUT);
  pinMode(ledPin_1, OUTPUT);
  pinMode(ledPin_2, OUTPUT);
  pinMode(ledPin_3, OUTPUT);
  pinMode(ledPin_4, OUTPUT);
  pinMode(ledPin_5, OUTPUT);
  pinMode(buttonPin_SIM,INPUT_PULLUP);
  pinMode(buttonPin_NAO,INPUT_PULLUP);
  
  // Garantir que todos os LEDs estão desligados no início
  digitalWrite(ledPin_5, LOW);
  digitalWrite(ledPin_4, LOW);
  digitalWrite(ledPin_3, LOW);
  digitalWrite(ledPin_2, LOW);
  digitalWrite(ledPin_1, LOW);
  digitalWrite(ledPin_0, LOW);
  
  int lastButtonState_SIM = LOW; 
  int lastButtonState_NAO = LOW;
}

void loop()
{
 int numpensado=0;    
 Serial.println("Pense num valor de 0 a 63");
  for (bit=5;bit>=0;bit--){   
    //escolher a potência de dois
    mascara= 1 << bit;
    
    
    Serial.println("O numero este nesta sequencia?");
    //imprimir os numeros com essa potencia
    for (n=0;n<64;n++){
      if ((n & mascara)!= 0){
        Serial.print(n);
        Serial.print (" ");
      }
    }
    Serial.println();
    
    // Ler a resposta do utilizador
    int sim = !digitalRead(buttonPin_SIM);
    int nao = !digitalRead(buttonPin_NAO);
    
    while (!sim && !nao){
      sim = !digitalRead(buttonPin_SIM);
      nao = !digitalRead(buttonPin_NAO);
     
    }
    int cronometro=millis();
    //diz qual o botao é que está pressionado
    int botaoPressionado=0;
    if (sim){
      botaoPressionado=buttonPin_SIM;
    }
    else {
      botaoPressionado=buttonPin_NAO;
    }
    // enquanto estiver a ser pressionado
    while (sim || nao){
      sim = !digitalRead(buttonPin_SIM);
      nao = !digitalRead(buttonPin_NAO);
      //quando for pressionado por mais de 2s
      if (millis() - cronometro > 2000){
        varrerLeds();
        return;
     }
    }
      
     
   
      
    delay(100);
    if (botaoPressionado == buttonPin_SIM){
      digitalWrite(6+bit, HIGH);
      numpensado+=mascara;
    }
   
      
  }
  Serial.println(numpensado);
  delay(5000);
  varrerLeds();
}

//reset
void varrerLeds(){
  int delayDuracao=100;
  
  for(int led=11; led >=6;led--){
    digitalWrite(led,LOW);
  }
  
  for(int led=6; led <=11;led++){
    digitalWrite(led,HIGH);
    delay(delayDuracao);
    digitalWrite(led,LOW);
  }
  
  for(int led=11; led >=6;led--){
    digitalWrite(led,HIGH);
    delay(delayDuracao);
    digitalWrite(led,LOW);
  }
  
}
        
   
    
    
      
      
      
  
    
  


