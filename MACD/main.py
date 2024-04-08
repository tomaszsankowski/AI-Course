import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def srednia_kroczaca(data,N): # returns [N:] elements
    alpha = 2/(N+1)
    licznik = 0
    mianownik = 0
    for i in range(0,N+1):
        licznik += data[i] * (1-alpha) ** (N-i)
        mianownik += (1-alpha) ** i
    EMA = [(licznik/mianownik)]
    for i in range(N+1,len(data)):
        licznik = 0
        for j in range(0,N+1):
            licznik += data[i-j] * (1-alpha) ** j
        EMA.append(licznik/mianownik)
    return EMA

# main

name = "PKN"
df = pd.read_csv('sp500.csv', usecols=['Data', 'Zamkniecie'])
df['Data'] = pd.to_datetime(df['Data'])
df.set_index('Data', inplace=True)

# Wykres notowań akcji
df.plot(kind='line', y='Zamkniecie', figsize=(10, 6), linewidth=0.75)
plt.title('Wykres ceny jednostkowej ' + name)
plt.xlabel('Data')
plt.ylabel('Cena')
plt.grid(True)
plt.legend()
plt.show()

# obliczanie EMA_12 oraz EMA_26
PRICES = df['Zamkniecie'].values
DATES = df.index[26:]

EMA_12 = srednia_kroczaca(PRICES,12)
del EMA_12[:14]
EMA_26 = srednia_kroczaca(PRICES, 26)

# Wykres EMA_12 i EMA_26
plt.plot(DATES, EMA_26, label="EMA 26", linewidth=0.75)
plt.plot(DATES, EMA_12, label="EMA 12", linewidth=0.75)
plt.xlabel('Czas')
plt.ylabel('Wartość średniej kroczącej')
plt.title('Wykresy średnich kroczących ' + name)
plt.grid(True)
plt.legend()
plt.show()



# Obliczanie MACD oraz SIGNAL
MACD = [EMA_12[i] - EMA_26[i] for i in range(len(EMA_12))]
SIGNAL = srednia_kroczaca(MACD,9)

del MACD[:9]
DATES = DATES[9:]

histogram_MACD = [MACD[i] - SIGNAL[i] for i in range(len(MACD))]

# Znajdź momenty, kiedy MACD przecina sygnał
buy_signals = []
sell_signals = []
for i in range(1, len(MACD)):
    if MACD[i] > SIGNAL[i] and MACD[i-1] <= SIGNAL[i-1]:
        buy_signals.append(DATES[i])
    elif MACD[i] < SIGNAL[i] and MACD[i-1] >= SIGNAL[i-1]:
        sell_signals.append(DATES[i])

# Wykres MACD i SIGNAL
plt.bar(DATES, histogram_MACD, color=['green' if val >= 0 else 'red' for val in histogram_MACD], alpha=1.0, label='Histogram MACD')
plt.plot(DATES, MACD, label="MACD", linewidth=0.75)
plt.plot(DATES, SIGNAL, label="SIGNAL", linewidth=0.75)
plt.xlabel('Czas')
plt.ylabel('Wartość MACD oraz SIGNAL')
plt.title('Wykres wskaźnika MACD oraz SIGNAL dla ' + name)
plt.grid(True)
plt.legend()
plt.show()

# Wykres ceny akcji wraz z punktami kupna/sprzedaży
PRICES = PRICES[35:]

plt.plot(DATES, PRICES, label="Cena", linewidth=0.5)
plt.scatter(buy_signals, [PRICES[DATES.get_loc(date)] for date in buy_signals], color='green', marker='^', label='Buy Signal')
plt.scatter(sell_signals, [PRICES[DATES.get_loc(date)] for date in sell_signals], color='red', marker='v', label='Sell Signal')
plt.xlabel('Czas')
plt.ylabel('Cena')
plt.title('Cena oraz punkty kupna/sprzedaży dla ' + name)
plt.grid(True)
plt.legend()
plt.show()


# Symulujemy inwestowanie początkowo 1000 akcji pasywnie oraz używając wskaźnika MACD
liczba_akcji = 1000
kapital = 0
kapital_start =  1000 * PRICES[0]

transactions = []
for i in range(1, len(MACD)):
    if MACD[i] > SIGNAL[i] and MACD[i-1] <= SIGNAL[i-1]: # kupno
        if (kapital > 0):
            liczba_akcji = kapital / PRICES[i]
            kapital = 0
            transactions.append([DATES[i], 'Buy', liczba_akcji*PRICES[i], 1000 * PRICES[i]])
    elif MACD[i] < SIGNAL[i] and MACD[i-1] >= SIGNAL[i-1]: # sprzedaż
        if (liczba_akcji > 0):
            transactions.append([DATES[i], 'Sell', liczba_akcji*PRICES[i], 1000 * PRICES[i]])
            kapital = PRICES[i] * liczba_akcji
            liczba_akcji = 0

if(liczba_akcji>0):
    kapital = liczba_akcji*PRICES[len(MACD)-1]
    transactions.append([DATES[-1], 'End', liczba_akcji*PRICES[len(MACD)-1], 1000 * PRICES[len(MACD)-1]])

# Wyniki symulacji
print("Obracanie początkowo 1000 akcji w porównaniu do buy and hold [1]")
print("Początkowy kapitał : ", kapital_start)
print("Końcowy zysk/strata : ", round((kapital-kapital_start),2))
print("Zysk (buy and hold) : ", round((1000*PRICES[len(MACD)-1]-kapital_start),2))

# Wykres 1
czas = [transaction[0] for transaction in transactions]
kapital_aktywny = [transaction[2] for transaction in transactions]
kapital_pasywny = [transaction[3] for transaction in transactions]

plt.figure(figsize=(10, 6))
plt.plot(czas, kapital_aktywny, label="Kapitał (inwestowanie aktywne)", color="blue", linewidth=1.0)
plt.plot(czas, kapital_pasywny, label="Kapitał (inwestowanie pasywne)", color="green", linewidth=1.0)
plt.axhline(y=kapital_start, color='red', linestyle='--', label='Startowy kapitał')
plt.xlabel('Czas')
plt.ylabel('Kapitał')
plt.title('Porównanie kapitału inwestycyjnego')
plt.grid(True)
plt.legend()
plt.show()

'''
root = tk.Tk()
root.title("Tabela transakcji")
headings = ["Data", "Sell/Buy", "Kapitał (MACD)", "Kapitał (buy and hold)"]
table = ttk.Treeview(root, columns=headings, show="headings", selectmode="browse")

for header in headings:
    table.heading(header, text=header)

for i, transaction in enumerate(transactions):
    table.insert(parent='', index='end', iid=i, values=(transaction[0].date(), transaction[1], round(transaction[2],2), round(transaction[3],2)))

table.pack(expand=True, fill="both")

root.mainloop()
'''

# Inwestujemy 1000 dolarów tygodniowo pasywnie, lub używając MACD, dokupując lub wstrzymując się od zakupu w zależności od wskazań MACD
akcje_pasywne = 0
akcje_aktywne = 0
kapital_aktywny = 0
transactions = []
for i in range(0, len(MACD)):
    akcje_pasywne += 1000/PRICES[i]
    if MACD[i] >= SIGNAL[i]: # kupno
        akcje_aktywne += (kapital_aktywny+1000)/PRICES[i]
        kapital_aktywny = 0
    else: # wstrzymanie się od kupna
        kapital_aktywny += 1000
    transactions.append([DATES[i], round(akcje_aktywne*PRICES[i] + kapital_aktywny,2), round(akcje_pasywne*PRICES[i],2), 1000*i])

# Wyniki symulacji
print("Inwestowanie 1000 dolarów miesięcznie lub odkładanie dokupowania w zależności co mówi MACD [1]")
print("Dla ", len(MACD), " tygodni inwestowania: ")
print("Przez ten czas zainwestowaliśmy ", 1000*len(MACD), " dolarów.")
print("Kapitał dla inwestowania pasywnego : ", round(akcje_pasywne*PRICES[len(MACD)-1],2), " dolarów.")
print("Kapitał dla inwestowania aktywnego (MACD) : ", round(akcje_aktywne*PRICES[len(MACD)-1] + kapital_aktywny,2), " dolarów.")

# Wykres 2
czas = [transaction[0] for transaction in transactions]
kapital_aktywny = [transaction[1] for transaction in transactions]
kapital_pasywny = [transaction[2] for transaction in transactions]
kapital_zainwestowany = [transaction[3] for transaction in transactions]

plt.figure(figsize=(10, 6))
plt.plot(czas, kapital_aktywny, label="Kapitał (inwestowanie aktywne)", color="blue", linewidth=1.0)
plt.plot(czas, kapital_pasywny, label="Kapitał (inwestowanie pasywne)", color="green", linewidth=1.0)
plt.plot(czas, kapital_zainwestowany, label="Zainwestowane pieniądze", color="red", linestyle='--', linewidth=1.0)
plt.xlabel('Czas')
plt.ylabel('Kapitał')
plt.title('Porównanie kapitału inwestycyjnego')
plt.grid(True)
plt.legend()

plt.show()

# INNA STRATEGIA: aby zakupić, MACD musi się przecinać z Signal z wartością poniżej zera (zero lane) oraz EMA_200 musi być poniżej ceny akcji
# jako, że MACD nadaje się głównie do strategii długoterminowych użyjemy jej tak jak w drugiej symulacji

EMA_200 = srednia_kroczaca(df['Zamkniecie'].values, 200)

PRICES = PRICES[(200-35):]
del MACD[:(200-35)]
DATES = DATES[(200-35):]
del SIGNAL[:(200-35)]

# strategia 1: spekuluemmy 1000 akcji i porównujemy wynik to buy and hold:
liczba_akcji = 1000
kapital = 0
kapital_start = 1000 * PRICES[0]

transactions = []
for i in range(1, len(MACD)):
    sell_buy = 'Hold'
    if ((MACD[i] > SIGNAL[i] and MACD[i-1] <= SIGNAL[i-1])or (MACD[i] < SIGNAL[i] and MACD[i-1] >= SIGNAL[i-1])) and MACD[i]<0 and SIGNAL[i]<0 and PRICES[i]>EMA_200[i]: # kupno (gwarancja up-trend)
        if (kapital > 0):
            liczba_akcji = kapital / PRICES[i]
            kapital = 0
            sell_buy = 'Buy'
    elif ((MACD[i] > SIGNAL[i] and MACD[i-1] <= SIGNAL[i-1])or (MACD[i] < SIGNAL[i] and MACD[i-1] >= SIGNAL[i-1])) and MACD[i]>0 and SIGNAL[i]>0 and PRICES[i]<EMA_200[i]: # sprzedaż (gwarancja down-trend)
        if (liczba_akcji > 0):
            kapital = PRICES[i] * liczba_akcji
            liczba_akcji = 0
            sell_buy = 'Sell'
    transactions.append([DATES[i], sell_buy, max(kapital,liczba_akcji*PRICES[i]), 1000 * PRICES[i]])

if(liczba_akcji>0):
    kapital = liczba_akcji*PRICES[len(MACD)-1]
    transactions.append([DATES[-1], 'End', kapital, liczba_akcji*PRICES[len(MACD)-1]])

# Wyniki symulacji
print("Obracanie początkowo 1000 akcji w porównaniu do buy and hold [2]")
print("Początkowy kapitał : ", kapital_start)
print("Końcowy zysk/strata : ", round((kapital-kapital_start),2))
print("Zysk (buy and hold) : ", round((1000*PRICES[len(MACD)-1]-kapital_start),2))

# Wykres 3
czas = [transaction[0] for transaction in transactions]
kapital_aktywny = [transaction[2] for transaction in transactions]
kapital_pasywny = [transaction[3] for transaction in transactions]

plt.figure(figsize=(10, 6))
plt.plot(czas, kapital_aktywny, label="Kapitał (inwestowanie aktywne)", color="blue", linewidth=1.0)
plt.plot(czas, kapital_pasywny, label="Kapitał (inwestowanie pasywne)", color="green", linewidth=1.0)
plt.axhline(y=kapital_start, color='red', linestyle='--', label='Startowy kapitał')
plt.xlabel('Czas')
plt.ylabel('Kapitał')
plt.title('Porównanie kapitału inwestycyjnego')
plt.grid(True)
plt.legend()

plt.show()

# strategia 2: Inwestujemy 1000 dolarów tygodniowo pasywnie, lub używając MACD, dokupując lub wstrzymując się od zakupu w zależności od wskazań MACD
akcje_pasywne = 0
akcje_aktywne = 0
kapital_aktywny = 0
transactions = []
for i in range(0, len(MACD)):
    akcje_pasywne += 1000/PRICES[i]
    if ((MACD[i] > SIGNAL[i] and MACD[i-1] <= SIGNAL[i-1])or (MACD[i] < SIGNAL[i] and MACD[i-1] >= SIGNAL[i-1])) and MACD[i]<0 and SIGNAL[i]<0 and PRICES[i]>EMA_200[i]: # kupno
        akcje_aktywne += (kapital_aktywny+1000)/PRICES[i]
        kapital_aktywny = 0
    else: # wstrzymanie się od kupna
        kapital_aktywny += 1000
    transactions.append([DATES[i], round(akcje_aktywne*PRICES[i] + kapital_aktywny,2), round(akcje_pasywne*PRICES[i],2), 1000*i])

# Wyniki symulacji
print("Inwestowanie 1000 dolarów miesięcznie lub odkładanie dokupowania w zależności co mówi MACD [2]")
print("Dla ", len(MACD), " tygodni inwestowania: ")
print("Przez ten czas zainwestowaliśmy ", 1000*len(MACD), " dolarów.")
print("Kapitał dla inwestowania pasywnego : ", round(akcje_pasywne*PRICES[len(MACD)-1],2), " dolarów.")
print("Kapitał dla inwestowania aktywnego (MACD) : ", round(akcje_aktywne*PRICES[len(MACD)-1] + kapital_aktywny,2), " dolarów.")

# Wykres 4
czas = [transaction[0] for transaction in transactions]
kapital_aktywny = [transaction[1] for transaction in transactions]
kapital_pasywny = [transaction[2] for transaction in transactions]
kapital_zainwestowany = [transaction[3] for transaction in transactions]

plt.figure(figsize=(10, 6))
plt.plot(czas, kapital_aktywny, label="Kapitał (inwestowanie aktywne)", color="blue", linewidth=1.0)
plt.plot(czas, kapital_pasywny, label="Kapitał (inwestowanie pasywne)", color="green", linewidth=1.0)
plt.plot(czas, kapital_zainwestowany, label="Zainwestowane pieniądze", color="red", linestyle='--', linewidth=1.0)
plt.xlabel('Czas')
plt.ylabel('Kapitał')
plt.title('Porównanie kapitału inwestycyjnego')
plt.grid(True)
plt.legend()

plt.show()