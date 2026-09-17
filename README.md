# Kursy walut NBP

Desktopowa aplikacja w Pythonie do pobierania kursów walut z API Narodowego Banku Polskiego. Umożliwia wybór waluty i zakresu dat, przygotowanie danych do wykresu, eksport danych do CSV oraz przeliczanie kwot między PLN i wybraną walutą obcą.

## Funkcje

### Pobieranie danych historycznych

W głównym widoku można:

- wybrać datę początkową i końcową,
- wybrać walutę,
- pobrać kursy kupna i sprzedaży z tabeli C API NBP,
- wyświetlić wykres zmian kursu,
- zapisać wykres jako plik PNG,
- zapisać dane jako plik CSV.

Obsługiwane waluty:

| Kod | Waluta |
| --- | --- |
| CHF | Frank szwajcarski |
| EUR | Euro |
| USD | Dolar amerykański |
| SEK | Korona szwedzka |
| GBP | Funt szterling |
| DKK | Korona duńska |
| UAH | Hrywna ukraińska |

### Przelicznik walut

Drugi widok służy do przeliczania kwot na podstawie aktualnego kursu z API NBP.

- Domyślnie kwota jest przeliczana z PLN na walutę obcą.
- W tym kierunku używany jest kurs sprzedaży banku (`ask`): kwota PLN jest dzielona przez kurs.
- Przycisk `↔` odwraca kierunek przeliczenia.
- Przy przeliczeniu z waluty obcej na PLN używany jest kurs kupna (`bid`): kwota jest mnożona przez kurs.
- Przycisk `Wyczyść` przywraca kwotę `0.00` i wynik `0.00`.
- Niepoprawne, ujemne lub niepełne dane wejściowe są odrzucane bez wysyłania niepotrzebnego żądania.

## Technologie

- Python 3.10 lub nowszy
- Tkinter, interfejs graficzny aplikacji
- `tkcalendar`, kalendarz wyboru dat
- `requests`, komunikacja z API NBP
- `matplotlib`, wykresy i eksport PNG
- `pytest`, testy automatyczne

Aplikacja korzysta z API NBP i nie wymaga klucza API. Do działania potrzebne jest połączenie z Internetem.

## Wymagania systemowe

- Python 3.10+
- Linux, Windows lub macOS
- Tkinter zainstalowany w systemie
- dostęp do Internetu podczas pobierania danych

W systemach Debian/Ubuntu Tkinter można zainstalować poleceniem:

```bash
sudo apt install python3-tk
```

## Instalacja

Sklonuj repozytorium i przejdź do jego katalogu:

```bash
git clone <adres-repozytorium>
cd apka_kursy
```

Utwórz i aktywuj środowisko wirtualne:

```bash
python3 -m venv kursy-env
source kursy-env/bin/activate
```

Na Windows aktywacja środowiska wygląda następująco:

```powershell
kursy-env\Scripts\activate
```

Zainstaluj zależności:

```bash
python -m pip install -r requirements.txt
```

## Uruchomienie

Aplikację uruchamia się z głównego katalogu projektu:

```bash
python -m app.main
```

Po uruchomieniu pojawi się okno `Kursy walut NBP`. Menu pozwala przełączać się między głównym widokiem, przelicznikiem i instrukcją aplikacji.

## Przebieg pracy

1. Wybierz walutę oraz daty w głównym widoku.
2. Użyj jednego z przycisków eksportu albo wyświetl wykres.
3. Przy eksporcie CSV plik zostanie zapisany w katalogu `output_files/`.
4. W przeliczniku wybierz walutę, wpisz kwotę i naciśnij `Przelicz`.
5. Użyj `↔`, aby zmienić kierunek przeliczenia.

Zakres dat jest ograniczony przez interfejs do ostatnich 93 dni, zgodnie z maksymalnym zakresem obsługiwanym przez pojedyncze żądanie tabeli C API NBP. Zakres dat musi mieć datę początkową wcześniejszą lub równą końcowej.

## Pliki wynikowe

Eksport CSV tworzy plik o nazwie:

```text
output_files/kursy_<waluta>_<data-początkowa>-<data-końcowa>.csv
```

Plik zawiera kolumny:

```text
Data,kurs_sprzedazy,kurs_kupna,spread
```

`spread` to różnica między kursem kupna i sprzedaży, zapisana z dokładnością do czterech miejsc po przecinku.

Eksport PNG tworzy plik o nazwie:

```text
output_files/<waluta>_<data-początkowa>-<data-końcowa>.png
```

Katalog `output_files/` jest ignorowany przez Git, aby pliki wynikowe nie trafiały do repozytorium. Funkcja eksportu CSV tworzy go automatycznie. Przed eksportem PNG katalog musi istnieć.

## API NBP

Aplikacja korzysta z następujących endpointów:

```text
https://api.nbp.pl/api/exchangerates/rates/c/<kod>/<data-od>/<data-do>?format=json
https://api.nbp.pl/api/exchangerates/rates/c/<kod>/today?format=json
```

Sesja HTTP ma skonfigurowane ponowienia dla żądań `GET`. Ponowienia dotyczą między innymi statusów `429`, `500`, `502`, `503` i `504`, a pojedyncze żądanie ma limit czasu 15 sekund. Błędy połączenia, timeouty i błędy HTTP są obsługiwane przez moduł API i zwracają `None`.

## Struktura projektu

```text
app/
└── main.py              # Punkt wejścia aplikacji

src/
├── file_handler.py      # CSV, PNG i przygotowanie danych wykresu
├── nbp_api.py           # Sesja HTTP i komunikacja z API NBP
├── user_interface.py    # Okno Tkinter i logika obsługi użytkownika
└── view_data.py         # Przygotowanie zakresu dat i uruchomienie widoku

tests/
├── test_nbp_api.py      # Testy API, plików i przelicznika
└── __init__.py

output_files/            # Lokalne pliki CSV i PNG, ignorowane przez Git
requirements.txt         # Zależności projektu
```

Import modułu `app.main` nie uruchamia aplikacji. GUI startuje wyłącznie po wykonaniu modułu jako programu dzięki blokowi `if __name__ == "__main__"`.

## Testy

Uruchomienie wszystkich testów:

```bash
python -m pytest -q
```

Testy obejmują między innymi:

- poprawne i błędne odpowiedzi API,
- timeouty, błędy połączenia i błędy HTTP,
- konfigurację ponowień HTTP,
- zapis CSV z danymi i z pustą listą kursów,
- przygotowanie osi wykresu,
- przeliczanie w obu kierunkach z użyciem `bid` i `ask`,
- odrzucanie niepoprawnej kwoty,
- odrzucanie odwróconego zakresu dat.

Testy nie wykonują prawdziwych żądań do API. Odpowiedzi HTTP są zastępowane obiektami `Mock`.

## Status projektu

Projekt można uznać za skończony. Być może w przyszłości będę dalej go ulepszać.



