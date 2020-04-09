# GEO Skripty

Skripty pro usnadnění práce s prostorovými daty. Skripty jsou psané v jazyce
Python v3.

##  xlsx2csv.py

Dekoruje vstupní XLSX soubor o atributy x, y, který se vypočítá transformací
souřadnic existujících atributů Lat/Lon. Výstupní CSV obsahuje všechna data +
další sloupečky se souřadnicemi v S-JTSK x, y [m].

## ruian2byty.py

Stáhne data RUIAN za obec a z vrstvy `StavebniObjekty` vytáhne pouze objekty sloužící
k ubytování a k nim přidá atributy

* Kod
* TypStavebnihoObjektuKod
* ZpusobVyuzitiKod
* PocetBytu
* PocetPodlazi

Výsledek uloží jako soubor CSV

## Závislosti a instalace

`ruian2byty` potřebuje pro svůj běh knihovnu GDAL a její Pythonní knihovnu. 

### Na Linuxu (debian/ubuntu)

`sudo apt install gdal-bin python3-gdal` nebo ekvivalentní příkaz

### Na Windows

Po nainstalování Pythonu stáhnout ze stránek
https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal patřičný soubor `whl` pro
správnou verzi vašeho Pythonu a instalovat pomocí `pip`.

# Kontakt

V případě nutnosti `jachym.cepicky opengeolabs.cz` nebo různě na různých
Slackcích `@jachym`.
