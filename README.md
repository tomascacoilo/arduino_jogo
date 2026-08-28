
Jogo interativo desenvolvido para Arduino que adivinha um número pensado pelo utilizador entre 0 e 63 através de 6 perguntas e respostas (Sim/Não).

Como Funciona:
O jogo utiliza operações bitwise para identificar os bits do número pensado. 
- O utilizador responde se o número está presente na lista apresentada no Monitor Série usando botões.
- A resposta positiva ativa um LED e soma a respetiva potência de 2.
- No final das 6 rondas, o número correto é exibido.

Componentes Utilizados:
- 1x Placa Arduino;
- 6x LEDs (indicadores de bits);
- 2x Pushbuttons (Botão "SIM" e "NÃO");
- Resistores e Jumpers.

Conceitos:
- Operadores bitwise em C++ ;
- Leitura de entradas digitais com INPUT_PULLUP;
- Temporização com millis() para debouncing e comandos por pressão longa.
