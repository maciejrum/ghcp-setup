# Niezależna ocena Incident Desk

Te testy uruchamia oceniający po zamrożeniu patcha. Nie kopiuj tego katalogu ani rozwiązań referencyjnych do `A-standard` lub `B-team`. Otwieraj warianty jako osobne, pojedyncze workspace'y. Obie próby dostają wymagania z [zadania](../task.md), ale bez implementacji testów oceniających. Użyj identycznej wersji tego katalogu dla całej pary; `manifest.json` zawiera jego listę plików i SHA-256.

Oceniający nie importuje kodu aplikacji. Python odpytuje uruchomione HTTP API, a Playwright obsługuje uruchomiony interfejs. Oczekiwane identyfikatory i liczby danych są zapisane niezależnie od implementacji rozwiązania: alpha ma 18 incydentów, po 6 w każdym statusie; beta ma 9, po 3. Kolejność to najwyższy identyfikator jako pierwszy. Nie zmieniaj oczekiwań po obejrzeniu patchy.

## Setup przed pomiarem

Potrzebujesz Pythona 3.11+ oraz wersji Node wymaganej przez [aplikację](../fixture/README.md). API oceniającego używa tylko biblioteki standardowej Pythona. Playwright ma osobny, przypięty pakiet i lockfile; instalacja oceniającego nie zmienia zależności aplikacji.

```sh
cd benchmark/assessor
npm ci
npx playwright install chromium
```

Domyślny wariant używa Chromium pobranego dla przypiętej wersji Playwright. Alternatywnie, jeśli masz zainstalowany Google Chrome, możesz pominąć pobranie Chromium i ustawić `ASSESSOR_BROWSER_CHANNEL=chrome` przy `npm test`. Runner uruchamia nowy, izolowany profil headless; nie korzysta z Twojej zalogowanej sesji. Użyj tego samego kanału i wersji przeglądarki dla A oraz B i zapisz je w notatkach. Lokalna walidacja protokołu odbyła się z Playwright 1.55.1 i systemowym Chrome 154.0.8037.58; pobrane Chromium nie zostało tu zweryfikowane.

Uruchom backend i frontend wyłącznie ocenianego wariantu, według jego `README.md`. Domyślne adresy to `http://127.0.0.1:8000` i `http://127.0.0.1:5173`. Nie uruchamiaj obu wariantów na tych samych portach. Wykonaj poniższe polecenia z repo konfiguracji, poza workspace'em aplikacji:

```sh
python benchmark/assessor/api_acceptance.py --base-url http://127.0.0.1:8000 --json-output /private/tmp/incident-A-api.json
cd benchmark/assessor
FRONTEND_URL=http://127.0.0.1:5173 ASSESSOR_REPORT=/private/tmp/incident-A-ui.json npm test
```

Dla B zmień nazwy raportów. Jeśli używasz innych portów, podaj ich rzeczywiste adresy. W PowerShell ustaw zmienne osobno, np. `$env:FRONTEND_URL = 'http://127.0.0.1:5173'` i `$env:ASSESSOR_REPORT = 'C:\Temp\incident-A-ui.json'`, po czym uruchom `npm test`. Ścieżki raportów należą do oceniającego.

## Zakres oceny

| Kryterium | Zewnętrzne sprawdzenia |
| --- | --- |
| AC1 | Trzy statusy, pusty/nieznany/wielkimi literami status → 422; pominięty status zachowuje odpowiedź |
| AC2 | Ustalona druga strona po filtrze, poprawny `total`, strona poza zakresem, dotychczasowa walidacja paginacji |
| AC3 | Różne wyniki alpha/beta dla każdego statusu, brak/nieznany tenant → 401 |
| AC4 | Wszystkie opcje natywnego selecta, etykieta `Status`, dostęp przez Tab, URL i odświeżenie strony; wybór klawiaturą także ręcznie |
| AC5 | Reset do `page=1`, All usuwa `status`, Next/Previous zachowują filtr i `page_size` |
| AC6 | Loading/error/empty, Retry, aktywny filtr podczas pobierania, spóźniony sukces i spóźniony błąd |
| AC7 | Osobno uruchom testy obu aplikacji oraz build i sprawdź sensowność testów dodanych w patchu |

Testy UI wykorzystują istniejące etykiety `Workspace`, `Next`, `Previous`, `Retry` i komunikaty stanów. Nowa etykieta `Status` i opcje są częścią zadania. Oceniający znajduje widoczne identyfikatory incydentów, nie klasy CSS lub nazwy funkcji. Kontrolowana odpowiedź HTTP w testach wyścigu pozwala wymusić odwrotną kolejność odpowiedzi; oddzielne testy API sprawdzają rzeczywiste filtrowanie i autoryzację.

Kod wyjścia API: `0` — wszystkie sprawdzenia przeszły; `1` — przynajmniej jedno nie przeszło; `2` — nie można połączyć się z API i nie wykonano sprawdzeń. Playwright ma zero automatycznych powtórzeń i jednego workera. Raporty dokumentują sprawdzenia, nie są pomiarem credits ani czasu wykonania zadania przez Copilota. Kilka nieudanych subtestów może wynikać z jednej usterki; nie licz ich jako osobnych defektów jakości.

Sam komplet zielonych testów oceniającego nie kończy oceny. Uruchom `pytest` w backendzie oraz `npm test` i `npm run build` we frontendzie, sprawdź diff względem baseline commita z manifestu i zastosuj wspólną [rubrykę jakości](../quality-rubric.md). Nie przekazuj agentowi błędów oracle w tej samej mierzonej próbie; wznowienie z taką informacją jest nowym eksperymentem.

Obowiązkowe ręczne sprawdzenie AC4 dla obu wariantów: w normalnej przeglądarce przejdź Tab do `Status`, wybierz `Open` klawiszami właściwymi dla systemu i zatwierdź wybór. Potwierdź status w URL, reset strony do 1 i wyłącznie otwarte incydenty. Zapisz PASS/FAIL/NOT_RUN oraz system i przeglądarkę. NOT_RUN nie spełnia warunku akceptacji. Headlessowe testy nie modelują identycznie natywnych menu wyboru wszystkich systemów; ich kontrola Tab nie zastępuje tego sprawdzenia.

## Sprawdzenie samego protokołu

Baseline celowo nie ma filtra. Jego dotychczasowe testy i build powinny przechodzić, ale nowe sprawdzenia filtra muszą nie przejść. Na baseline API powinny nadal przechodzić sprawdzenia pominiętego statusu, walidacji paginacji i kontroli klienta; pozostałe powinny wykazywać realne różnice w danych, `total` lub kodzie HTTP. Brak kontrolki `Status` powinien powodować porażkę nowych testów UI. To kontrola poprawności benchmarku, a nie wynik mierzonej próby A/B.

Sprawdzenie oracle na ewentualnym rozwiązaniu referencyjnym wykonuj poza repo i workspace'ami prób. Nie dostarczaj tego rozwiązania agentom i nie zapisuj go jako wyniku Copilota.
