# ContaPersone
Progetto Conta Accessi:

Il progetto intende contare ingressi-uscite dalla Biblioteca usando un sensore VL53L5CX che misura le distanze
per via ottica ed ha un campo visivo largo circa 62 gradi. Tale campo è diviso in 64 pixel su matrice 8x8

Il progetto iniziale prevedeva il WiFi_Terminal inserito sulla scheda Nucleo-64 STM32F072 
Non sono riuscito a trovare librerie per la lettura del sensore che fossero compatibili con l'STM32
Ho quindi ripiegato su ESP32
Allo stato quindi abbiamo: Scheda WiFi_Terminal connessa via seriale a ESP-WROOM-32
STM32 legge il sensore e trasmette via seriale il set di 64 misure.
WiFI_Terminal, riceve le misure e le rende disponibile via TCP sulla porta 9000

Il programma HeatMap.py gira su PC per visualizzare la mappa delle distanze
