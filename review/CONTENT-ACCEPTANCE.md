# Obowiązkowe kryterium odbioru: poprawki w treści, nie errata

Doprecyzowanie Marka podczas przebudowy: „Super ze dajesz sprostowania do materialow wykladowych, ale licze, ze skoro je przebudowujesz to wprowadzisz poprawki zauwazonych bledow i niedomowien.”

Siedem nowych prezentacji ma zawierać poprawną, zrozumiałą treść już w docelowych slajdach. Nie wystarczy raport wskazujący błędy ani dopisek ostrzegawczy pozostawiający niepoprawne stwierdzenie obok.

Warunki odbioru dla wykonawcy i koordynatora:
- Każdy rozpoznany błąd należy poprawić we właściwym QMD, tabeli, podpisie ilustracji, przykładzie kodu i powtórzeniach tego twierdzenia. Następnie ponownie wyrenderować i sprawdzić HTML.
- Niedomówienia uzupełniać o warunki stosowalności, jednostki, ograniczenia i potrzebny kontekst. Gdy materiał staje się za długi, podzielić slajd zamiast używać drobnej czcionki.
- Podawać zweryfikowaną wersję faktu, nie kopiować błędu oryginału dla zachowania wierności. Dotyczy też błędów w dokumentacji producentów: rozstrzygać przez schemat/datasheet, a nie prezentować błędny pin jako poprawny.
- Szczególnie sprawdzić: Stamp-C3U vs C3, GPIO a USB/VIN, prądy graniczne a robocze, ADC/Wi-Fi zależnie od SoC, QoS a przetwarzanie biznesowe, retained a historia, retry/idempotencja, autoryzacja Sheets, CE vs PE, OTA/rollback i podpisy.
- Usunąć lub zastąpić niesprawne ilustracje i zbędne logotypy, poprawić błędy JS, nie zostawiać ich jedynie w sekcji „znane problemy”.
- Nie fabrykować rozstrzygnięcia: autentycznie nierozstrzygnięty szczegół oznaczyć jako niepewny albo pominąć z instrukcji wykonawczej. Takie resztkowe przypadki jawnie raportować.
- Rejestr korekt ma być dodatkiem dla Marka: źródło -> błędna/niepełna teza -> poprawna wersja -> dowód -> docelowy slajd. Nie zastępuje poprawionych slajdów i nie musi zaśmiecać publicznej prezentacji.

Koordynator nie uzna przebudowy za ukończoną przed sprawdzeniem tego kryterium w źródłach i wyrenderowanych prezentacjach. Bez zmian zakresu: lokalne repo, bez push/commit i bez podmiany Moodle.
