# ftx-bot

*** WORK IN PROGRESS ***

IL programma consiste in un BOT che fa trading su un EXCHANGE seguendo una certa logica e su vari ASSET.
Ogni mattina fa il check della candela e decide se comprare o vendere o non fare nulla. Se fa un'operazione manda una NOTIFICA su telegram.
Ogni operazione la salva su un DB relazionale.
Il bot non gira sempre ma solo in un certo momento dalla giornata quando viene lanciato

Protegonisti:
EXCHANGE-Connector
BOT
WALLET
BRAIN
ORDINE
NOTIFICA
DBMANAGER
DASHBOARD
PARAMETERS

FLOW:
-il bot sceglie che EXCHANGE usare e usa le api per collegarvisi e scarica il WALLET di quel exchange
-calcola l' heikin ashi e decide se comprare o meno
-se compra crea un ordine di acquisto e genera la notifica (la notifica invia a telegram e al db)


IMPLEMNTAZIONE:
- implementare tutte le classi vuote
 


Cose secondarie:
dashboard
dbmanager
brain

COMANDI UTILI:
poetry add nome_pacchetto --lock -D