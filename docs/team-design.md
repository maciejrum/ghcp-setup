# Decyzje dotyczące Engineering Team v4

Stan na 1 października 2026. Dokument zapisuje uzgodniony projekt i hipotezy; nie jest raportem z wyników Copilota.

## Punkt startowy

Repo już zawierało pięć ról, wspólny Task Brief, niezależny review, limit napraw i opcjonalny odczyt Jira. Koordynator używał GPT-5.6 Sol, Explorer GPT-5.6 Luna, Implementer Sonnet 5, Reviewer GPT-5.6 Terra, a Deep Reviewer GPT-5.6 Sol.

Naszym celem jest dopasowanie modeli dostępnych na koncie Business/Enterprise do odpowiedzialności oraz obniżenie kosztu poprawnie zakończonego zadania. Prezentacja ma opierać się na zebranych wynikach.

## 1. Role mają konkretne granice

Koordynator ustala zakres i kryteria oraz deleguje pracę. Explorer czyta kod, jeden Implementer go zmienia, Reviewer ocenia rzeczywisty diff. Deep Reviewer rozstrzyga tylko konkretne poważne pytanie. Walidacja jest etapem pracy, a nie obowiązkowym dodatkowym agentem.

Nie mnożymy ról wraz z liczbą dostępnych modeli. Oszczędność może wynikać z krótkiego kontekstu, mniejszej liczby zbędnych operacji i ograniczonej liczby poprawek.

## 2. Opus 5.5 jako koordynator

Pierwsza propozycja optymalizacji wskazywała GPT-6 Sol. Po dyskusji o znaczeniu interpretacji wymagań i decyzji koordynatora przyjęliśmy Opusa 5.5 jako wariant bazowy. Sol pozostaje kandydatem do osobnego eksperymentu.

Hipoteza: wyższy koszt koordynacji może się zwrócić dzięki mniejszej liczbie błędnych delegacji i poprawek. Nie mamy jeszcze dowodu przewagi jakości Opusa w tym repo.

## 3. Tańszy model dostaje ograniczone zadanie

Explorer używa GPT-6 Luna do scoped research. Sonnet 5 implementuje i waliduje zmianę. GPT-6 Sol prowadzi niezależny review, a Opus 5.5 analizuje uzasadniony trudny problem. Jawny wybór modeli subagentów w Local musi mieścić się w kategorii kosztowej rodzica; aktualna konfiguracja spełnia tę relację statycznie.

Przypisanie modelu w pliku jest konfiguracją. Faktycznie użyty model, dostępność narzędzi i zużycie trzeba potwierdzić w runtime.

## 4. Benchmark ma wspólny punkt startowy i ocenę

Przygotowaliśmy Incident Desk z zamrożonym zadaniem, niezależnymi testami oraz workspace'ami A/B. A to standardowy Agent na Opusie, B to cały team z Opusem jako koordynatorem. Wspólne są aplikacja, wymagania, instrukcje projektu i ocena. Role, skills i modele pomocnicze stanowią pakiet B.

Hipotezy do zbadania:

- Czy team dostarcza więcej zaakceptowanych wyników przy tych samych kryteriach?
- Czy tańsze rozpoznanie i implementacja obniżają credits mimo kosztu delegacji i review?
- Czy team ogranicza pozostałe defekty i interwencje człowieka?
- Jaki narzut czasu i kosztu pojawia się na niewielkim zadaniu?

Wynik przeciwny do hipotezy pozostaje wynikiem benchmarku. Trzy pary tego samego zadania są pilotażem, nie dowodem uniwersalnej przewagi.

## Co jest przygotowane, a co wymaga pomiaru

Przygotowane: konfiguracja, walidator, aplikacja bazowa, zamrożone zadanie, zewnętrzna ocena, instrukcja i tracker. Wyniki zużycia, jakości pracy modeli i czasu z Copilota dostarczy użytkownik. Dopiero później powstanie [prezentacja](presentation-plan.md).

Źródła zasad platformy: [modele i ceny GitHub](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing), [subagenci VS Code](https://code.visualstudio.com/docs/agents/run/subagents), [optymalizacja zużycia](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage).
