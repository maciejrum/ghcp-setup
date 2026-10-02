# Ocena jakości kodu

Jedna rubryka obowiązuje dla A i B. Oceniaj końcowy patch i otaczający kod, po zamrożeniu wyników. Zapisz lokalizację lub przykład uzasadniający każdą ocenę. Ocena jest osądem recenzenta; nie przedstawiamy jej jako obiektywnego testu.

## Akceptacja i defekty

**accepted = YES** wymaga przejścia wszystkich zewnętrznych testów API/UI, ręcznego sprawdzenia wyboru statusu klawiaturą z AC4, testów aplikacji i builda oraz braku poważnych defektów w zewnętrznym review. Niewykonane wymagane sprawdzenie oznacza brak akceptacji; opisz przyczynę i zakres sprawdzeń.

- **Major:** naruszenie kryterium lub regresja wpływająca na poprawność, izolację danych, obsługę błędów albo używalność; podaj reprodukcję i skutek.
- **Minor:** problem utrzymania lub czytelności bez naruszenia kryteriów, np. niepotrzebna duplikacja, zbędny kod albo myląca nazwa.

Liczymy unikalne przyczyny, a nie każdy test padający wskutek tej samej usterki. Przykładowo jedno błędne filtrowanie po paginacji może zepsuć kilka testów, ale nadal jest jednym defektem. Informacja o `APPROVED` od Reviewera teamu nie zastępuje tej oceny.

## Rubryka 0–10

Każdy z pięciu obszarów otrzymuje 0, 1 lub 2 punkty. Równe wagi to jawny wybór tego pilotażu. Nie zmieniaj ich po zobaczeniu wyników.

| Obszar / pole | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Architektura / quality_architecture | Zmiana psuje istniejące granice albo wprowadza sprzeczne źródła stanu | Zachowanie działa, ale pojawia się zbędna duplikacja lub silne sprzężenie | Zmiana wykorzystuje istniejące granice API/UI i ma jedno zrozumiałe źródło stanu |
| Typy i walidacja / quality_types | Brak wymaganej walidacji albo obejście typów maskuje problem | Kontrakt jest zachowany, ale są nieuzasadnione rzutowania lub zbyt szerokie typy | Dane wejściowe i odpowiedzi mają precyzyjne typy, a status jest walidowany na serwerze |
| Błędy i asynchroniczność / quality_errors | Błąd ukryty jako sukces, utracony stan error albo starsza odpowiedź nadpisuje nową | Kryteria spełnione, ale obsługa ma zbędne gałęzie lub niejasną kontrolę cyklu żądania | Obsługa loading/error/empty i kolejności żądań jest spójna i łatwa do prześledzenia |
| Testy patcha / quality_tests | Brak testów nowego zachowania, osłabione stare testy lub testy bez znaczących asercji | Sensowne testy ścieżki podstawowej, ale brak istotnej regresji paginacji lub wyścigu | Testy zachowania obejmują filtr/paginację i szybkie zmiany wyboru oraz nie zależą od szczegółów implementacji |
| Zakres i czytelność / quality_scope | Zmiany niepowiązane z zadaniem albo poważnie utrudnione utrzymanie | Zakres właściwy, ale pozostał zbędny kod lub lokalna nieczytelność | Mały, czytelny patch bez niepowiązanych zmian, zależności i zmian danych początkowych |

Suma `quality_total` powstaje dopiero po wypełnieniu wszystkich pięciu obszarów. Puste pole oznacza brak oceny, a 0 rzeczywistą ocenę. Wysoki wynik jakości nie kompensuje niespełnionych kryteriów akceptacji.

## Notatka recenzenta

```text
Patch / revision:
Komendy i wyniki zewnętrznych sprawdzeń:
Wybór statusu klawiaturą (AC4): PASS/FAIL/NOT_RUN + przeglądarka i obserwacja
Major: lokalizacja, trigger, skutek, reprodukcja
Minor: lokalizacja i uzasadnienie
Architektura: 0/1/2 + dowód
Typy: 0/1/2 + dowód
Błędy: 0/1/2 + dowód
Testy: 0/1/2 + dowód
Zakres: 0/1/2 + dowód
Akceptacja: YES/NO + uzasadnienie
Brakujące sprawdzenia / ograniczenia:
```
