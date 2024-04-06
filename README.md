# Trading Bot em BTC

```mermaid
flowchart LR
    Trading_Bot -- tem --> Candle_Chart
    Candle_Chart -- guarda --> Candle
    Trading_Bot -- tem --> Balance
    Balance -- tem --> USD
    Balance -- tem --> BTC
    Balance -- tem --> LimitUSD
    Balance -- tem --> LimitBTC
    Balance -- tem --> Default
    Trading_Bot --> Decider
    Balance --> History
    History -- guarda --> Entry
    Entry -- tem --> Datetime
    Entry -- tem --> Valor
    Decider -- cria --> Decision
    Balance -- recebe --> Decision
    Trading_Bot -- comunica com -->API_Caller
    REST_API -- interroga --> Trading_Bot
```

O api_caller deverá obter informações acerca de candles passadas ou do valor atual da moeda.

A candle deverá armazenar essas informações, e, no caso da
captura de uma vela, deverá oferecer uma função feed() capaz de ir recebendo os valores da moeda e indo atualizando a estrutura.

A candle_chart deverá ir armazenando as candles e fornecer e calcular os indicadores quando necessário. Deverá também oferecer todos os indicadores sobre o formato de uma matriz.

> !NOTE: ÉS UM GÉNIO, A MATRIZ VAI DAR PARA DAR PLUG NA REDE NEURAL!!!!!!

O history deverá armazenar os histórico de 'jogadas do bot' (entry). Um entry regista uma transação (vender ou comprar), a data e hora em que foi feita e o valor da moeda no momento.

A balance deverá guardar o estado financeiro do bot, assim como os limites de gasto e o valor de aposta padrão.

A decision deverá ser a decisão tomada e o multiplier.

```mermaid
classDiagram
    Trading_Bot -- Candle_Chart : tem
    Candle_Chart o-- Candle : tem
    Trading_Bot -- Balance : tem
    Trading_Bot -- Decider : tem
    Trading_Bot -- History : tem
    class Candle {
        -__top : float
        -__bottom : float
        -__entry : float
        -__exit : float
        -__samples : int
        -__stamp : datetime
        +__init__(top : float, stamp: datetime = None) : None
        +feed(value : float) : None
    }
    class Candle_Chart {
        -__candles : list
        +get__indicator__() : float
    }

```