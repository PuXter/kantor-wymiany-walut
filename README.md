# Kantor wymiany walut
Systemy Operacyjne 2 - Projekt 

Politechnika Wrocławska, Wydział Informatyki i Telekomunikacji

Prowadzący -  [Mgr inż. Tomasz Szandała](https://github.com/szandala) 

Autorzy - [Łukasz Czerwiec](https://github.com/PuXter), [Bartosz Szymczak](https://github.com/PewPewBartula)

**Założenia programu**:
- Aplikacja służy do prostej symulacji wymiany walut w oparciu o wątki
- Zostanie wykorzystany prosty serwer http
- Użytkownik po wejściu na stronę i zalogowaniu będzie w stanie podać rodzaje i ilość waluty do przeliczenia
- Jeden wątek będzie odpowiedzialny za pobranie danych o walutach z [Narodowego Banku Polskeigo](https://www.nbp.pl/home.aspx?f=/kursy/kursya.html) i losowe przekształcanie ich
- Drugi wątek będzie odpowiedzialny za obsługę określonej liczby użytkowników strony

