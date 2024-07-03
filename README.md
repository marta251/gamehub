# GameHub
A collection of games you can play from your terminal



Il progetto consiste nello sviluppo di un'applicazione da riga di comando che permetterà di giocare a una serie di giochi classici. In particolare l'interfaccia grafica sarà gestita direttamente nel terminale per mezzo della libreria curses di Python (https://docs.python.org/3/howto/curses.html).
Segue l'elenco dei giochi che siamo intenzionati ad implementare:
- Scacchi
- Dama
- Conway's Game of Life
- Snake
- Wordle
In ogni caso l'applicazione sarà strutturata in modo da permettere una facile estensione con nuovi giochi nel futuro. 

Ogni gioco avrà il proprio set di opzioni: 
- Scacchi: sarà possibile selezionare modalità single-player (giocare da solo contro un'IA) o multiplayer (giocare in due dallo stesso terminale) 
- Dama: sarà possibile selezionare modalità single-player o multiplayer
- Conway's Game of Life: modalità manuale (viene eseguita un'epoca ogni volta che viene ricevuto un input da parte dell'utente) o modalità automatica (periodicamente viene eseguita un'iterazione, in tal caso è anche possibile definire l'intervallo di tempo desiderato)
- Snake: velocità di gioco 

L'idea per gestire l'IA, necessaria per la modalità single-player degli scacchi, è quella di utilizzare la API ReST di Stockfish oppure l'applicazione di Stockfish stessa. In particolare, l'intenzione è quella di realizzare due immagini utilizzando Docker: la prima sarà più leggera e necessiterà di essere connessi ad internet per giocare a scacchi, in quanto utilizzerà l'API ReST per calcolare le mosse dell'IA, mentre la seconda conterrà al proprio interno Stockfish, sarà dunque più pesante ma non necessiterà di essere connessi ad internet.


Esempi di utilizzo: 

gamehub scacchi --mode multiplayer

gamehub game-of-life --mode automatic -t 0.2

gamehub snake --speed fast
