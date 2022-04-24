# Kantor wymiany walut
Systemy Operacyjne 2 - Projekt 

Politechnika Wrocławska, Wydział Informatyki i Telekomunikacji

Prowadzący -  [Mgr inż. Tomasz Szandała](https://github.com/szandala) 

Autorzy - [Łukasz Czerwiec](https://github.com/PuXter), [Bartosz Szymczak](https://github.com/PewPewBartula)

**Założenia programu**:
- Aplikacja służy do prostej symulacji wymiany walut w oparciu o wątki
- Zostaną wykorzystane proste aplikacje serwera i klienta, komunikujące się ze sobą za pomocą socketów
- Klient będzie w stanie podać rodzaj i ilość waluty do przeliczenia
- Jeden wątek będzie odpowiedzialny za pobranie danych o walutach z [Narodowego Banku Polskeigo](https://www.nbp.pl/home.aspx?f=/kursy/kursya.html) i losowe przekształcanie ich 
- Drugi wątek będzie odpowiedzialny za obsługę określonej liczby klientów

