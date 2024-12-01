# RCE Demonštračný nástroj

Tento program umožňuje demonštráciu učenia RCE (restricted coulomb energy) neurónových sietí. Umožňuje vizualizáciu každého kroku učenia siete, vytvorenie dátovej sady, editáciu existujúcej testovacej sady.

## Inštalácia

Inštalácia kľúčových programov a balíčkov na systéme linux (pred spustením prejdite do koreňového adresára projektu)

```
bash build.sh
```

#### Manuálny postup

- Aktualizujte a nainštalujte python3 python3-pip python3-venv
- Vytvorte virtuálne prostredie do ktorého stiahnete balíčky podľa requirements.txt

```
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
# Create virtual environment
python3 -m venv my-rce-venv
# pip install -r requirements.txt into virtual env
my-venv/bin/pip install -r requirements.txt
```

## Spustenie

Spustenie na systéme linux

```
bash run.sh
```

#### Manuálny postup

- Zmeňte prostredie na to, ktoré ste vytvorili pri inštalácii
- Spustite main.py

```
source my-rce-venv/bin/activate
python3 main.py
```

## Menu

V hlavnom menu si môžete vybrať medzi trénovaním RCE siete a vytváraním dátovej sady pre trénovanie.

## Trénovanie RCE siete

1. <b>Load Data</b> - výber súboru pre načítanie vstupných dát (Trénovanie siete sa vykoná automaticky po načítaní dátovej sady)
2. <b><<<,<<,<,>,>>,>>></b> - posúvanie sa na začiatok/koniec trénovania, cez jednotlivé iterácie, cez jednotlivé kroky
3. <b>R max</b> - slúži na úpravu maximálnej aktivačnej hodnoty pre skrytú vrstvu neurónov,
4. <b>Show</b> - results zobrazí v novom okne informácie o natrénovanej sieti (finálnej)
5. <b>Help</b> - zobrazí popis ovládania
6. <b>Back</b> - vráti do Menu

## Vytváranie dátovej sady

1. <b>Add Point</b> - pridá vektor s dvoma súradnicami (X, Y) a triedou - Class (ktorá značí farbu akou bude daný bod vykreslený)
2. <b>Remove Point</b> - odstráni vektor podľa súradníc (X, Y) na triede vektoru nezáleží
3. <b>Save Dataset</b> - uloží trénovacie dáta
4. <b>Load Dataset</b> - načíta trénovacie dáta, ktoré následne môžeme upravovať a uložiť
5. <b>Back</b> - vráti do menu

## Štruktúra Repozitára

- **root**
  - **data**
    - **input_data.py**: Modul na spracovanie vstupných dát. Umožňuje pridanie, odstránenie vektorov.
    - **my_exceptions.py**: Definície vlastných výnimiek.
    - **point.py**: Vstupný vektor.
    - **json_serializer**: Zaobaľuje logiku pre vytváranie json formátu výstupných trénovacích dát.
  - **gui**
    - **main_menu.py**: Menu pre výber medzi vytváraním datasetu alebo trénovaním.
    - **main_window.py**: Vytvorí hlavné okno, v ktorom sa menia obrazovky (menu, train, create).
    - **mpl_canvas.py**: Vytvorenie Matplotlib canvasu pre zobrazenie grafov.
    - **styles.py**: Štýly pre tlačidlá a ďalšie GUI komponenty.
    - **train_network_screen.py**: Hlavná obrazovka na tréning siete.
    - **create_dataset_screen.py**: Hlavná obrazovka pre vytváranie vstupného datasetu.
  - **rce**
    - **rce_trainer.py**: Hlavná logika tréningu RCE siete. Ukladá priebežné výsledky trénovania.
    - **rce_network.py**: RCE sieť, umožňuje pridávanie nových neurónov. Obsahuje vrstvu hidden a ouput neuronov, flagy o modifikácii siete, hit, maximálnu veľkosť polomeru aktivačnej funkcie neurónov, index trénovacej sady a index skrytého neuronu. Umožňuje detailny výpis všetkých podstatných informácii.
    - **hidden_neuron.py**: Skrytý neuron RCE siete.
    - **output_neuron.py**: Výstupný neuron RCE siete.
  - **main.py**: Hlavný skript na spustenie aplikácie.
  - **rce_text.py**: Vedľajší skript na tréning siete a výpis výstupov trénovania na konzolu.
  - **requirements.txt**: Zoznam potrebných Python knižníc.
  - **.gitignore**
  - **README.md**

## Autor

Martin Pribylina, xpriby19
