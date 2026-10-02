# Benchmark Incident Desk

Porównujemy **A: standardowy Agent / Opus 5.5** i **B: Orchestrator / Opus 5.5 z naszym teamem**. Zadanie to dodanie filtra statusu do małej aplikacji FastAPI + React + TypeScript. Kryteria obejmują API, paginację, izolację danych klientów, URL i kolejność odpowiedzi asynchronicznych.

To porównanie całych pakietów pracy. Model główny jest wspólny, ale B ma własne role, modele pomocnicze, kontrakty i skills. Wynik nie wyodrębnia samego wpływu orkiestracji. Standardowy Agent może używać swoich wbudowanych subagentów; zapisujemy ich faktyczne użycie.

## 1. Przygotuj parę workspace'ów

Wymagane: Python 3.11+, Node zgodny z [aplikacją](fixture/README.md), npm, Git i VS Code z Copilot Business/Enterprise. Używamy harnessu **Local**. Modele muszą być dostępne zgodnie z polityką organizacji.

Z katalogu głównego tego repo:

```sh
python scripts/prepare_benchmark.py --destination ../ghcp-benchmark-pair-01 --init-git
```

Na macOS/Linux użyj `python3`, jeśli `python` nie wskazuje Pythona 3. Na Windows użyj `py` lub właściwej ścieżki do Pythona.

Powstaną nowe katalogi `A-standard`, `B-team` oraz `manifest.json`. Istniejący cel nie zostanie nadpisany. Flaga `--init-git` tworzy lokalny commit bazowy **wyłącznie w tych nowych workspace'ach**, aby dało się porównać późniejszy diff. Nie dotyka historii tego repo i niczego nie publikuje.

Manifest zapisuje stan źródeł, hashe plików i losową kolejność AB/BA. Zachowaj go poza workspace'ami. Dla kolejnych par użyj nowych ścieżek, np. `../ghcp-benchmark-pair-02` i `../ghcp-benchmark-pair-03`. Nigdy nie przygotowuj drugiej próby z rozwiązania pierwszej.

Otwieraj A i B jako **osobne okna z pojedynczym folderem**. Nie otwieraj katalogu nadrzędnego ani tego repo jako multi-root workspace. Dzięki temu agent nie otrzyma rozwiązania drugiego wariantu ani zewnętrznych testów oceniających.

## 2. Sprawdź środowisko przed pomiarem

W obu workspace'ach wykonaj setup i bazowe sprawdzenia opisane w ich README. Pobierz zależności i uruchom aplikację przed startem stopera. Używaj identycznych wersji, lockfile, portów i usług. A i B uruchamiaj kolejno, nie równocześnie na tych samych portach.

Zapisz wersję VS Code, rozszerzenia Copilot, harness, modele, reasoning/context i ustawienia zatwierdzania. W A wybierz standardowego **Agent** i **Claude Opus 5.5**. W B wybierz **Orchestrator**. Potwierdź efektywny model główny i routing pomocników na podstawie diagnostyki, nie samego YAML.

W obu wariantach są te same wspólne instrukcje projektu, instrukcje ścieżek oraz ustawienia zatwierdzania. Definicje teamu i jego skills są dostępne tylko w B. Nie dodawaj dodatkowego MCP ani osobistych skills do jednego wariantu. Jeśli instrukcje użytkownika/organizacji pozostają aktywne, zapisz je i zachowaj takie same w obu.

Preflight modelu i narzędzi wykonaj w osobnej rozmowie. Jego koszt nie należy do właściwej próby. Jeśli nie da się wywołać skonfigurowanych modeli, popraw środowisko przed startem; nie podstawiaj po cichu innego modelu.

## 3. Wykonaj zadanie

1. Zacznij od wariantu wskazanego w `manifest.json`. Zamknij inne płatne sesje na swoim koncie.
2. Otwórz nową rozmowę. Usuń niepotrzebne otwarte pliki i załączniki. Nie przekazuj historii ani ustaleń poprzedniej próby.
3. Zapisz źródło pomiaru credits i odczyt początkowy, jeśli używasz licznika zużycia przypisanego do siebie. **Nie używaj zmiany wspólnej puli Business/Enterprise jako kosztu tej sesji.**
4. Uruchom stoper w chwili wysłania identycznego [promptu zadania](task.md).
5. Zatwierdzaj równoważne bezpieczne operacje według tych samych zasad. Licz zatwierdzenia osobno od podpowiedzi, ręcznych edycji i innych interwencji.
6. Nie podpowiadaj sposobu rozwiązania. Jeśli agent zada pytanie, odpowiedz wyłącznie na podstawie zamrożonego zadania i zapisz pytanie oraz odpowiedź.
7. Zatrzymaj czas pracy agenta po jego końcowym raporcie albo ustalonym wcześniej limicie. Zapisz `agent_minutes`, diff i diagnostykę sesji.
8. Oceń wynik według następnej sekcji. Zapisz także `verified_minutes`: czas od pierwszego promptu do zakończenia zewnętrznych testów i review.
9. Odczytaj przypisane zużycie po uwzględnieniu opóźnienia raportowania. Zapisz źródło i okres pomiaru. Jeśli nie można przypisać kosztu, zostaw credits puste i opisz brak danych.

Przed pierwszą próbą ustal i zapisz ten sam limit czasu dla obu wariantów, np. **30 minut pracy agenta**. Nie zmieniaj go po zobaczeniu wyniku A. Instrukcje teamu o liczbie poprawek są miękką polityką modeli; obserwuj faktyczne wykonanie. Limitu CLI nie traktujemy jako limitu tego eksperymentu w VS Code Local.

## 4. Oceń zamrożony wynik

[Oceniający](assessor/README.md) działa poza workspace'ami A/B, przeciwko ich uruchomionej aplikacji. Jego setup i pobranie przeglądarki zrób przed pomiarem. Testy zostały przygotowane dla ustalonego zadania, a nie wygenerowane z patcha agenta.

Po raporcie agenta:

- zachowaj patch, wersje plików i eksport śladu;
- uruchom bazowe testy aplikacji, jej nowe testy i build;
- uruchom zewnętrzne sprawdzenia API i przeglądarki z instrukcji oceniającego;
- sprawdź wybór filtra samą klawiaturą w normalnej przeglądarce według instrukcji oceniającego i zapisz wynik w notes;
- wykonaj ten sam przegląd kodu według [rubryki jakości](quality-rubric.md) dla A i B;
- zapisz akceptację, defekty, czas i koszt, również dla prób nieudanych lub zablokowanych.

Review teamu jest częścią jego workflow. Wspólny zewnętrzny review stanowi ocenę benchmarku. Jeśli możesz, oceniaj patche pod neutralnymi identyfikatorami bez informacji o wariancie.

## 5. Zapisz pomiary

Użyj [CSV](results.csv) albo [trackera Excel](../outputs/benchmark-tracker.xlsx). Wybierz **jeden** jako źródło danych, aby nie powstały rozbieżne wyniki. Sześć wierszy oznacza trzy pary A/B, nie sześć wykonanych prób. Wszystkie pomiary są początkowo puste.

Najważniejsze pola:

| Pole | Co zapisujesz |
| --- | --- |
| pair, variant, execution_order | Numer pary, A/B, kolejność z manifestu |
| baseline_ref | Ścieżka/identyfikator manifestu i bazowy commit |
| resolved_models | Modele rzeczywiście widoczne w śladzie |
| status | NOT_RUN, DONE, FAILED lub BLOCKED; DONE oznacza zakończenie workflow, nie automatyczną akceptację |
| credits_used, credit_evidence | Rzeczywiste zużycie całej próby i jego źródło |
| agent_minutes, verified_minutes | Czas do raportu i czas do zewnętrznej weryfikacji |
| human_interventions, approval_prompts | Pomoc człowieka i zwykłe zatwierdzenia narzędzi, liczone osobno |
| repair_rounds | Zaobserwowane rundy poprawek; jeśli niewidoczne, pozostaw puste |
| api_tests, ui_tests | PASS/FAIL/NOT_RUN/PARTIAL plus wyniki i komendy w notes/evidence |
| remaining_major_defects, remaining_minor_defects | Unikalne defekty po zewnętrznym przeglądzie; zero tylko po faktycznej ocenie |
| accepted | YES/NO po wspólnej ocenie, puste przed oceną |
| quality_* | Pięć ocen 0–2 i ich suma według rubryki |
| trace_ref, notes | Ślad, patch, wynik ręcznego sprawdzenia klawiatury, blokery, brakujące dane i odstępstwa od procedury |

Nie sumuj zużycia rodzica obejmującego subagentów z ich kosztami drugi raz. `credits_after - credits_before` jest poprawne tylko dla tego samego, narastającego licznika **zużycia** z czystym przypisaniem. Licznik pozostałego budżetu ma odwrotny kierunek. Liczba wywołań narzędzi i oszacowanie modelu nie są pomiarem credits. Szczegóły: [obserwowalność](../docs/observability.md).

## 6. Co będzie można stwierdzić

Pierwsza para sprawdza procedurę i daje przykład. **Trzy pary są małym pilotażem**: pokażą zmienność tego samego zadania, ale nie dowiodą przewagi na wszystkich projektach. Zmieniaj kolejność A/B zgodnie z manifestami i zapisuj możliwy wpływ cache oraz uczenia się osoby obsługującej.

Porównamy akceptację, pozostałe defekty, czas, interwencje i credits. Koszt zaakceptowanego zadania to suma kosztów **wszystkich prób, także nieudanych**, podzielona przez liczbę zaakceptowanych wyników. Przy zerowej liczbie zaakceptowanych wyników ten iloraz jest nieokreślony. Brak kosztu choć jednej próby oznacza niepełne porównanie kosztów.

Testowo zielony wynik i ocena jakości kodu mierzą różne rzeczy. Pokazujemy je osobno. Zachowaj również wyniki, w których standardowy Agent wygrał.

## Materiały do późniejszej prezentacji

Przekaż wypełniony CSV lub XLSX, manifesty, patche A/B, wyniki zewnętrznych sprawdzeń oraz kilka kluczowych fragmentów śladów. Usuń prywatne dane przed udostępnieniem. Na tej podstawie przygotujemy prezentację na **5–10 minut** według [scenariusza](../docs/presentation-plan.md).
