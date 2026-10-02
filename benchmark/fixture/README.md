# Incident Desk

Mała aplikacja do przeglądania incydentów dwóch zespołów. API korzysta ze stałych danych w pamięci; nie wymaga bazy ani kont w usługach zewnętrznych.

Wymagania: Python 3.11–3.14 i Node.js 22.22.2+, 24.15+ albo 26+. Node.js 20 nie jest wspierany przez przypięty zestaw narzędzi.

## API — terminal 1

macOS / Linux, z katalogu aplikacji:

```bash
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Windows PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Dokumentacja API: <http://127.0.0.1:8000/docs>. `GET /api/incidents?page=1&page_size=5` wymaga nagłówka `X-Tenant-ID: alpha` albo `X-Tenant-ID: beta`. Domyślna strona to 1, a rozmiar strony to 5 (zakres 1–50). Incydenty są uporządkowane od najnowszego; `total` dotyczy całego zespołu. Nieznany zespół lub brak nagłówka otrzymuje HTTP 401. Niepoprawna paginacja daje HTTP 422.

W tej lokalnej aplikacji nagłówek wybiera zestaw danych zespołu i pozwala sprawdzić jego izolację. Nie jest produkcyjnym mechanizmem uwierzytelniania użytkowników.

## UI — terminal 2

Z katalogu aplikacji (takie same polecenia na macOS, Linux i Windows):

```bash
cd frontend
npm ci
npm run dev
```

Otwórz <http://127.0.0.1:5173>. Frontend przekazuje `/api` do API na porcie 8000. Można zmieniać zespół i stronę; parametry `page` i `page_size` w URL pozwalają otworzyć konkretny widok. Przy zajętym porcie serwer zakończy się błędem zamiast przejść na inny port.

## Sprawdzenia

W `backend`, macOS / Linux:

```bash
.venv/bin/python -m pytest
```

W `backend`, Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

W `frontend`, wszystkie systemy:

```bash
npm test
npm run build
```

Testy nie potrzebują uruchomionych serwerów. Testy API sprawdzają izolację zespołów, paginację i walidację; testy UI sprawdzają odczyt strony z URL, nagłówek zespołu i nawigację.
