# Jak zgłaszać uwagi do slajdów

## Najwygodniej: tryb recenzji w przeglądarce

1. Otwórz prezentację z dopiskiem `?review=1`, np.:
   `slides/01-architektura-i-wymagania.html?review=1`.
2. Przejdź do komentowanego slajdu.
3. Jeśli uwaga dotyczy fragmentu tekstu, zaznacz go myszą.
4. Kliknij **💬 Dodaj uwagę** albo naciśnij `C`.
5. Wpisz komentarz. Jest zapisywany lokalnie w tej przeglądarce.
6. Po zakończeniu kliknij:
   - **Kopiuj** — aby wkleić wszystkie uwagi bezpośrednio do rozmowy;
   - **Pobierz** — aby otrzymać pliki Markdown i JSON.
7. Po przekazaniu uwag możesz użyć **Wyczyść**; przycisk usuwa wszystkie lokalne uwagi
   dopiero po potwierdzeniu.

Każda uwaga zawiera nazwę prezentacji, stabilny identyfikator slajdu, numer aktualnego
fragmentu animacji, zaznaczony cytat i treść komentarza. Dzięki temu zmiany można
jednoznacznie odnieść do źródłowego pliku QMD.

## Format ręczny

Jeśli wolisz pisać uwagi w zwykłym pliku lub wiadomości, wystarczy taki zapis:

```text
04-mqtt-i-kontrakt-danych#qos-sekwencja
Cytat: „QoS 2 — dokładnie raz”
Uwaga: dodać przykład, kiedy koszt QoS 2 jest uzasadniony.
```

Ważny jest identyfikator widoczny po `#` w adresie slajdu. Komentarz do całego slajdu
nie wymaga cytatu.

## Powiększanie grafik

Każdą grafikę i diagram Mermaid można kliknąć. Otworzy się na całym ekranie; ponowne
kliknięcie albo `Esc` zamyka powiększenie.
