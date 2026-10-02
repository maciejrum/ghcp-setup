# Incident Desk: zadanie benchmarkowe

Wklej dokładnie poniższy blok w nowej rozmowie w obu wariantach. Nie dołączaj planu rozwiązania, testów oceniających ani wyników drugiego wariantu.

```text
Dodaj filtrowanie incydentów po statusie do istniejącego API i interfejsu Incident Desk.

Kryteria akceptacji:
AC1. GET /api/incidents obsługuje opcjonalny parametr status. Dozwolone wartości to open, in_progress i closed. Obecny, ale pusty lub nieobsługiwany status (także OPEN) zwraca HTTP 422. Pominięcie status zachowuje obecny kontrakt, kolejność danych i zachowanie paginacji.
AC2. Filtrowanie następuje w danych właściwego klienta, przed paginacją. total oznacza liczbę wszystkich dopasowanych incydentów tego klienta. Zachowaj walidację page i page_size oraz odpowiedź na stronę poza zakresem.
AC3. Zachowaj istniejącą kontrolę X-Tenant-ID. Brak nagłówka i nieznany klient nadal zwracają HTTP 401. Żaden filtr ani numer strony nie może ujawniać incydentów innego klienta.
AC4. Interfejs ma dostępny z klawiatury select z etykietą Status oraz opcjami All, Open, In progress, Closed. Wybrany status jest zapisany w parametrze status adresu URL. All usuwa ten parametr. Interfejs i dane odtwarzają wybór po odświeżeniu lub otwarciu adresu, również dla status=closed&page=2.
AC5. Zmiana statusu, również powrót do All, ustawia page=1. Przejście na następną/poprzednią stronę zachowuje wybrany status i dotychczasowy page_size. Zmiana Workspace zachowuje status i ustawia page=1. Interfejs nie może pokazywać incydentów spoza aktywnego filtra.
AC6. Zachowaj widoczne stany loading, error i empty. Starsza odpowiedź lub błąd wcześniejszego żądania nie może nadpisać danych ani stanu nowszego wyboru użytkownika. Filtr pozostaje dostępny podczas pobierania danych.
AC7. Dodaj sensowne testy regresyjne backendu i frontendu. Testy powinny sprawdzać zachowanie, w tym filtr z paginacją oraz szybkie zmiany wyboru. Dotychczasowe testy mają nadal przechodzić. Uruchom backendowe pytest, frontendowe npm test i npm run build z właściwych katalogów.

Zakres: wykorzystaj istniejącą architekturę i zależności. Nie zmieniaj danych początkowych, schematu odpowiedzi, nagłówka klienta, autoryzacji ani konfiguracji agentów. Nie dodawaj bibliotek ani usług zewnętrznych. Nie wykonuj commitów, push ani deploy. Nie wykonuj zmian poza tym zadaniem.

Na końcu podaj zmienione pliki, mapowanie kryteriów na dowody, komendy i wyniki sprawdzeń oraz otwarte problemy. Nie szacuj credits ani czasu — pomiar wykonam osobno.
```

## Warunki zakończenia

Agent kończy pracę jednym raportem. Po nim zamrażamy zmianę i oceniamy ją zewnętrznie. Po obejrzeniu testów oceniających nie przekazujemy ich wyników agentowi w tym samym pomiarze. Próba naprawy z taką informacją jest osobnym eksperymentem.

Do zewnętrznej akceptacji wymagane są: wszystkie testy API i UI oceniającego, ręczne sprawdzenie wyboru statusu klawiaturą z AC4, testy aplikacji, kompilacja frontendu oraz brak poważnych defektów w przeglądzie kodu. Sam komunikat DONE lub APPROVED nie jest zewnętrzną akceptacją.
