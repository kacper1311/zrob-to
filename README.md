# Zrób to!

## Opis projektu
Zrób to! to aplikacja do zarządzania zadaniami, umożliwiająca użytkownikom dodawanie, edytowanie i usuwanie zadań oraz zarządzanie użytkownikami. Aplikacja wykorzystuje interfejs graficzny oparty na Tkinter i zapisuje dane w pliku JSON.

## Cel projektu
- Stworzenie intuicyjnej aplikacji do zarządzania zadaniami.
- Możliwość przypisywania statusów zadaniom.
- Obsługa wielu użytkowników.
- Przechowywanie danych lokalnie w formacie JSON.

## Zakres projektu
- Interfejs graficzny (GUI) w Tkinter.
- Obsługa listy zadań i użytkowników.
- Możliwość dodawania, edytowania i usuwania zadań oraz użytkowników.
- Przechowywanie danych w pliku JSON.

## Technologie
- Python 3
- Tkinter (GUI)
- JSON (przechowywanie danych)

## Struktura projektu
```
ModernTaskManager/
│── main.py        # Główny plik aplikacji
│── tasks.py       # Logika zarządzania zadaniami
│── users.py       # Logika zarządzania użytkownikami
│── storage.py     # Obsługa zapisu i odczytu JSON
│── data.json      # Plik z danymi
│── README.md      # Dokumentacja
│── test_tasks.py  # Testy jednostkowe dla zadań
│── test_users.py  # Testy jednostkowe dla użytkowników
│── TEST_REPORT.md # Raport z testowania
```

## Uruchomienie aplikacji
   ```bash
   python main.py
   ```

## Funkcjonalności
- **Zarządzanie zadaniami:** dodawanie, edycja, usuwanie, statusy.
- **Zarządzanie użytkownikami:** dodawanie, edycja, usuwanie.
- **Zapis i odczyt danych w JSON.**

## Testowanie
Testy jednostkowe znajdują się w plikach `test_tasks.py` i `test_users.py`.
Aby uruchomić testy, użyj:
```bash
pytest test_tasks.py test_users.py
```

## Autor
- **Imię i nazwisko:** Kacper Jasyk
- **Indeks:** 58953

