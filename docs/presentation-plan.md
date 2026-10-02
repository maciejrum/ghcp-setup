# Prezentacja po benchmarku: 5–10 minut

Prezentację przygotujemy po otrzymaniu rzeczywistych wyników. Poniższy scenariusz ma wariant około 7 minut i sześć slajdów. [Decyzje projektu](team-design.md) zapisują, co wypracowaliśmy wspólnie i dlaczego.

| Slajd | Czas | Treść i materiał |
| --- | --- | --- |
| 1. Zadanie i cel | 0:40 | Jeden konkretny przykład z Incident Desk. Koszt zaakceptowanej zmiany, czas i jakość jako cele |
| 2. Jak dobraliśmy team | 1:10 | Istniejący setup, propozycja Sol, pytanie o koordynatora, wybór Opusa i podział odpowiedzialności |
| 3. Proces pracy | 1:00 | Jeden czytelny diagram: zakres → Explorer → Implementer i testy → Reviewer → wynik. Deep review tylko przy uzasadnionym problemie |
| 4. Zasady benchmarku | 0:50 | Identyczna baza i prompt, standardowy Agent kontra pełny team, świeże rozmowy, zewnętrzna ocena i trzy pary |
| 5. Wyniki | 1:50 | Zmierzone credits, akceptacja, czas i defekty. Wyniki każdej pary obok zbiorczego porównania. Fragment rzeczywistego śladu lub replay 20–30 s |
| 6. Co wdrażamy dalej | 1:00 | Wniosek wynikający z danych, ograniczenia pilotażu, kolejne zadania lub osobny test Opus/Sol |

W wersji 5-minutowej skrócimy historię i replay. W wersji 10-minutowej pokażemy jeden konkretny defekt lub etap, który wyjaśnia różnicę wyniku. Live coding nie jest potrzebne do tej długości prezentacji.

## Materiały potrzebne od użytkownika

1. Wypełniony [CSV](../benchmark/results.csv) albo [Excel](../outputs/benchmark-tracker.xlsx), również próby FAILED/BLOCKED.
2. Manifest i kolejność każdej pary oraz wersje VS Code/Copilot.
3. Patche A/B i wyniki wspólnych testów oraz przeglądu kodu.
4. Fragmenty śladów z rzeczywistymi modelami, delegacjami i źródłem zużycia credits.
5. Krótka notatka: gdzie potrzebna była pomoc człowieka i co zaskoczyło podczas prób.

## Zasady pokazania wyników

Nie przedstawiamy symulacji jako pomiaru. Nie przypisujemy całej różnicy samej orkiestracji. Koszt obejmuje nieudane próby, a brakujące zużycie pozostaje brakującą daną. Obok średnich pokażemy zakres albo poszczególne próby. Jeśli team przegrał na tym zadaniu, wyjaśnimy obserwowany koszt i następny eksperyment.

Efekt prezentacji budujemy rzeczywistym wynikiem, krótkim śladem współpracy i konkretną decyzją dla zespołu.
