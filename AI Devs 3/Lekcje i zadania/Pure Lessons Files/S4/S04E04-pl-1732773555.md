![](https://cloud.overment.com/S04E04-1732717129.png)

W poprzedniej lekcji skupiliśmy się na źródłach wiedzy dla LLM w postaci plików oraz treści stron www. Wspomniałem także, że źródłem informacji mogą być zewnętrzne usługi, posiadające API. Poza tym, możemy wykorzystać ten fakt nie tylko w celu wczytywania informacji, ale także **podejmowania działań**.

Dlatego w tej lekcji stworzymy kolejny zestaw narzędzi, który umożliwi połączenie modelu ze światem zewnętrznym. Na przykładach zobaczymy, jak istotna jest spójność formatu wymiany danych i jak można ułatwić budowanie narzędzi na własne potrzeby, korzystając z rozwiązań no-code.

Omawiane przykłady znajdują się w katalogu `tools`, a wśród nich są: 

- **Google Maps:** Umożliwia precyzyjne określanie wskazówek dojazdu oraz wczytywanie informacji na temat miejsc.
- **Spotify:** Pozwala na przeszukiwanie bazy utworów, albumów i playlist, a także odtwarzanie muzyki na dostępnym urządzeniu.
- **Resend**: Pozwala na przesyłanie wiadomości e-mail z pomocą platformy [resend](https://resend.com)
- **Speak:** (tylko macOS) pozwala na odtworzenie komunikatu głosowego z pomocą polecenia `say`

Dodatkowo w kodzie znajdują się także klasy dla SMS API, Google Calendar oraz YouTube (ze względu na zmianę polityki prywatności Google, ta klasa działa wyłącznie na komputerze lokalnym).

> WAŻNE: W związku z koniecznością posiadania kont i kluczy API dla wymienionych wyżej usług, potraktuj ich uruchomienie jako opcjonalne. W tej lekcji chodzi nam przede wszystkim o **schematy i praktyki tworzenia narzędzi**, a nie konkretne implementacje, które przedstawiam.
## Uprawnienia i dostępność

W lekcji S00E03 — API oraz w praktycznie każdym z przykładów, pojawiał się wątek uprawnień, które nadajemy modelowi oraz agentom AI. Do tej pory jednak niemal zawsze poruszaliśmy się po przykładach **odczytywania** danych.

Tym razem przejdziemy do narzędzi, w przypadku których ewentualna pomyłka może przełożyć się na rezultat niemożliwy do odwrócenia (np. wysłanie maila) lub generujące niepotrzebne trudności. Dlatego, podobnie jak w przykładzie `websearch` będzie nam zależało na programistycznych ograniczeniach, dzięki którym ewentualne pomyłki w odpowiedziach zostaną przechwycone, lub po prostu **nie będzie na nie miejsca**.

Patrząc na przykłady narzędzi, przez które będziemy przechodzić, zastanów się nad zestawem technologicznym z którego korzystasz lub który wykorzystuje Twoja firma. Sprawdź czy rozwiązania z którymi pracujesz oferują dostęp do API oraz jakie metody i formaty odpowiedzi są dostępne. Następnie zadaj sobie pytanie: **w jaki sposób możesz je wykorzystać w celu ułatwienia, optymalizacji bądź automatyzacji wybranych procesów**.

Weź także przede wszystkim pod uwagę fakt, niedeterministycznej natury modeli. W sytuacji gdy będziesz potrzebować 100% precyzji, zastosowanie modeli nie będzie dobrym pomysłem. Może się jednak okazać, że niedeterministyczne odpowiedzi mogą stanowić wartość. 

Ostatecznie **zawsze dbaj o ograniczanie uprawnień modelu do wyłącznie tych koniecznych**. Gdy nie będzie to możliwe, a pomoc LLM nadal będzie potrzebna, uwzględnij etap weryfikacji przez człowieka.

## Interfejs

Pomimo tego, że w przypadku narzędzi takich jak Google Maps nie mówimy o przetwarzaniu dokumentów, to i tak jako dane wejściowe/wyjściowe będziemy stosować struktury dokumentów (treść + metadane). Dzięki temu zachowamy spójność pomiędzy narzędziami i przykładowo: 

- Narzędzie Google Maps będzie mogło przetwarzać listę lokalizacji wczytanych z wybranych stron www czy plików PDF, albo nagrań audio
- Narzędzie Google Calendar będzie mogło otrzymać listę wiadomości e-mail na podstawie których utworzy spotkania w kalendarzu
- Narzędzie Resend będzie mogło otrzymać raporty, na podstawie których prześle prywatny newsletter lub wiadomości do wybranych osób (np. zespołu)

No i takie konfiguracje mogą uwzględniać także zaangażowanie kilku narzędzi pomiędzy którymi będziemy przekazywać dane. 

Dane w postaci dokumentów będziemy zwracać zarówno w przypadku powodzenia, jak i wystąpienia błędu. Dzięki temu agent otrzyma informację nie tylko o tym, że zadanie się nie powiodło, ale także o szczegółach błędu, co zwykle doprowadzi do jego automatycznego rozwiązania. 

![](https://cloud.overment.com/2024-10-21/aidevs3_messages-9f5ae274-5.png)

Struktura dokumentów nie musi być dokładnie taka, jak w moich przykładach. Liczy się jedynie zachowanie spójności oraz na tyle dużej elastyczności, aby ten sam format był zachowany dla każdego z narzędzi. 
## Narzędzia no-code

Dla usług takich jak Google Calendar, Google Maps czy Spotify, potrzebujemy autoryzacji z pomocą OAuth 2.0. Skorzystanie z niej zwykle wymaga wczytania się w dokumentację oraz publikacji endpointów odpowiedzialnych za przekierowanie do strony logowania oraz odebrania tokenów potrzebnych do dalszych zapytań.

Programistyczne połączenie z narzędziami zazwyczaj przynosi korzyści, ale czasami czas potrzebny na ich wdrożenie nie jest uzasadniony. Na przykład, jeśli tworzymy agenta do obsługi skrzynki e-mail w celu wykonania prostych operacji, takich jak tworzenie szkicu wiadomości, budowanie całej integracji od podstaw nie ma sensu.

W takich sytuacjach warto skorzystać z platform no-code, takich jak [make.com](https://www.make.com/). W przypadku Make, możemy utworzyć scenariusz rozpoczynający się i kończący modułem Webhook. W rezultacie automatyzacja ta, zostanie uruchomiona w chwili, gdy prześlemy zapytanie HTTP na adres wygenerowany w module "Custom Webhook". W odpowiedzi otrzymamy wszystko to, co zostanie uwzględnione w module Webhook Response. 

![](https://cloud.overment.com/2024-10-21/aidevs3_make_webhooks-60d51b75-1.png)

Praca z Make wykracza poza zakres naszego szkolenia, więc odsyłam do materiałów na stronie [Make Academy](https://academy.make.com/collections). Natomiast dodam do tego kilka głównych wskazówek:

- Webhook musi być zabezpieczony przed przypadkowym wywołaniem. W ustawieniach zaawansowanych modułu możemy aktywować opcję przechwytywania nagłówków HTTP w celu odczytania z nich nagłówka Authorization. Szczegóły na ten temat, można znaleźć [tutaj](https://community.make.com/t/incoming-webhook-authentication/15219/8)
- Moduł **webhook response** umożliwia ręczne wpisanie treści obiektu JSON, ale nie jest to zalecane ze względu na obsługę znaków specjalnych. Zamiast tego, zawsze powinniśmy korzystać z modułu Create JSON, który pozwala zdefiniować strukturę obiektu, na podstawie której wygenerowany zostanie JSON String. Przykład zastosowania, widoczny jest poniżej. 

![](https://cloud.overment.com/2024-10-21/aidevs3_json_response-c8518477-f.png)

Ze względu na rozwój LLM coraz rzadziej polecam rozwiązania no-code, ponieważ utworzenie połączenia z API, w tym także obsługi procesu OAuth 2.0, jest coraz prostsze. Po prostu musimy upewnić się, że do wiadomości systemowej modelu wkleimy treść dokumentacji i/lub przykłady pochodzące z SDK, a model bez większych problemów zaimplementuje nam całą logikę. 

Przy narzędziach no-code warto jednak zostać albo w wymienionej wyżej sytuacji (własne rozwiązania, na które nie mamy zbyt dużo czasu) albo: 

- gdy zależy nam na połączeniu ze sobą wielu usług
- gdy zależy nam na możliwości łatwego edytowania logiki, bez otwierania kodu
- gdy zależy nam na zaangażowaniu osób, które nie potrafią programować / posługiwać się generowanym kodem
- gdy potrzebujemy jednorazowego rozwiązania lub jesteśmy na etapie prototypu
- gdy chcemy uniknąć utrzymania integracji, np. w wyniku zmieniającego się API

Ogólnie rzecz biorąc, **coraz większe możliwości LLM w generowaniu kodu sprawiają, że korzyści z szybkiej implementacji logiki przy użyciu no-code są mniejsze**. Natomiast wartość narzędzi no-code nadal jest obecna, ale zmienia się ich rola. 
## Google Maps

Google Maps dostępne jest poprzez utworzenie aplikacji na [Google Cloud](https://console.developers.google.com/) lub poprzez natywną integrację w make.com (jednak tutaj i tak potrzebujemy identyfikatorów wygenerowanych w Google Cloud). Dostępne akcje obejmują między innymi: **wczytywanie informacji na temat miejsc**, oraz **określanie wskazówek dojazdu do miejsca docelowego.**

Dla określenia informacji na temat trasy, użytkownik zwykle będzie dostarczał niepełne dane, takie jak: "jak długo zajmie mi droga do Warszawy?" lub "ile potrzebuję na dojazd do domu?". 

Dla takich zapytań, API Google Maps nie będzie dla nas zbyt pomocne. Ale jeśli w kontekście pojawią się dokumenty zawierające informacje o tym **gdzie obecnie znajduje się użytkownik** oraz **gdzie jest "dom"**, to odnalezienie trasy będzie możliwe. 

![](https://cloud.overment.com/2024-10-21/aidevs3_map-190a5c0e-0.png)

W lekcji S01E02 — Kontekst pokazywałem podobny przykład, w którym agent 'uruchamiał ulubioną muzykę' bez podania wykonawcy. 

![](https://cloud.overment.com/2024-09-10/aidevs3_music-df9dde4c-b.png)

Zatem dla każdego z narzędzi musimy przemyśleć zapytania oraz scenariusze, które będziemy chcieli obsłużyć. Natomiast nie powinniśmy tutaj myśleć o **konkretnych przypadkach**, ale **ogólnych zasadach**.

Przykładowo w kodzie aplikacji nie mam żadnej wzmianki o tym, że agent ma 'dowiedzieć się, jaka jest ulubiona muzyka użytkownika'. W zamian, agent zadaje sobie serię pytań, aby lepiej zrozumieć **intencję użytkownika**. Chodzi więc o spekulacyjne zadawanie pytań ([Speculative RAG](https://arxiv.org/pdf/2407.08223)) i próbę doprecyzowania nieścisłości oraz odnalezienia brakujących informacji. 

Bardzo pomocny w takich sytuacjach jest także sam LLM, który także na podstawie kilku przykładów, jest w stanie nam pomóc w **generalizacji** oraz **określeniu schematów**. Poniżej znajduje się fragment mojej konwersacji (zawiera literówki) w której po opisie problemu proszę o uchwycenie szerokiej perspektywy, a nie konkretnej sytuacji. 

![](https://cloud.overment.com/2024-10-21/aidevs3_generalization-12af67b9-5.png)

Lekcja z tego narzędzia jest więc następująca: 

- System musi dążyć do odkrycia / zdobycia brakujących informacji, korzystając z pamięci długoterminowej i/lub zewnętrznych usług
- Rozwiązywanie problemów powinno opierać się na **schematach**, **zasadach** i **regułach**, a nie na pojedynczych przypadkach, których będzie zbyt wiele, aby je wszystkie zaadresować
## Wysyłanie wiadomości

Wysyłanie maili, wiadomości prywatnych czy SMS, których treść tworzy LLM jest często wymieniane jako potrzeba biznesowa w kontekście procesów sprzedażowych i marketingowych. Niemal nigdy nie będzie to dobry pomysł (choć takie procesy działają na dużej skali i zwykle określane są jako 'opłacalne'). Pozostawiając bez komentarza aspekty etyczne takich rozwiązań, możliwość kontaktowania się poprzez różne kanały jest przydatna.

Wiemy, że część zadań wykonywanych przez agenta będzie asynchroniczna i nierzadko będzie zajmować kilkanaście minut lub kilka godzin. Wśród nich będą także akcje uruchamiane w odpowiedzi na zdarzenie czy ustaloną porę. 

Warto więc rozważyć połączenie się z usługami takimi jak: 

- [Resend](https://resend.com) lub dowolna alternatywa umożliwiająca przesyłanie maili transakcyjnych
- [SMSAPI](https://www.smsapi.pl/) lub alternatywa (np. Twilio) umożliwiająca przesyłanie SMS
- [Slack](https://slack.com/) lub inny komunikator posiadający API

Jednak usługi te, **nie powinny być wykorzystywane do przesyłania masowych wiadomości**. Co więcej **lista kontaktów powinna być ograniczona** lub wprost ustawiona na tylko jeden adres — nasz.

Poza limitami, największym wyzwaniem jest sprawienie, by LLM był w stanie wygenerować treść, która faktycznie będzie dla nas wartościowa. Niestety zwykle taka nie jest, co widać na poniższym przykładzie wiadomości w odpowiedzi na prośbę o "listę filmów w których grał Keanu Reeves".

![](https://cloud.overment.com/2024-10-21/aidevs3_writing-ac4911c4-f.png)

Jednak po dopasowaniu promptu do naszych potrzeb i osobistych preferencji, otrzymujemy rezultat który skrajnie różni się od poprzedniego. Sam ton wypowiedzi, zwięzłość oraz przede wszystkim **wypełnienie polecenia w pełni** charakteryzują wiadomości pisane przez człowieka. Natomiast przede wszystkim — taki komunikat niesie realną wartość. 
 
![](https://cloud.overment.com/2024-10-21/aidevs3_email-ace28171-a.png)

W przypadku `tools/ResendService`, mamy tylko jeden prompt odpowiedzialny za napisanie treści wiadomości. Natomiast na przykładzie `web`, wiemy, że możemy rozwinąć logikę o serię promptów tworzących rozbudowaną wiadomość. W razie potrzeby, możemy uwzględnić w niej również użycie szablonu HTML, aby przygotować pełnoprawny newsletter.

Wniosek z tego narzędzia jest następujący:

- Przesyłanie wiadomości z pomocą komunikatorów oraz maila, powinno być możliwe, ale bardzo ograniczone. Sytuacja w której LLM decyduje się na wysłanie prywatnej korespondencji na przypadkowy adres e-mail, jest bardzo możliwa
- Sposób formatowania i zapisu treści powinien być dopasowany z pomocą promptów oraz przykładów, które możliwie ograniczą domyślne zachowanie modelu związane z generowaniem bardzo ogólnych treści
- W związku z tym, że nie będziemy mieć możliwości wprowadzania poprawek w treści wiadomości, musimy poświęcić więcej czasu na dopasowanie promptu

Poniższy prompt kształtowałem z pomocą LLM, korzystając przy tym z meta-promptu z lekcji S00E02 — Prompt Engineering. Stworzenie takiej instrukcji nie jest jednak automatyczne i wymaga kilku iteracji w których wspólnie z modelem kształtujemy kolejne zachowania. 

![](https://cloud.overment.com/2024-10-21/aidevs3_writing_prompt-67fe2db5-9.png)

Podobnie jak w przypadku innych narzędzi, w odpowiedzi przesyłamy dokument z treścią wiadomości oraz statusem akcji lub informacją o jej niepowodzeniu. 

![](https://cloud.overment.com/2024-10-21/aidevs3_confirmation-44bf569e-9.png)

Akcje związane z komunikacją powinny uwzględniać także zasady posługiwania się nimi. Przykładowo rozbudowane komunikaty powinny być przekierowane na e-mail, a pilne wiadomości wymagające natychmiastowej reakcji, powinny trafić na SMS. 
## Rozrywka

Nie wszystkie integracje będą opierać się o ustandaryzowane interfejsy i gotowe do użycia API. Niekiedy na własne potrzeby będziemy musieli znaleźć 'kreatywne' rozwiązanie pozornie nierozwiązywalnego lub trudnego do rozwiązania problemu.

Jedną z takich integracji może być powiadomienie w postaci komunikatu głosowego uruchamianego na naszym komputerze. Jednym z rozwiązań, jest wykorzystanie skryptu bash i polecenia `say` (macOS) lub narzędzi umożliwiających odtwarzanie plików audio (np. `afplay`). Takie polecenie powinno być dostępne zdalnie (np. przez [ngrok](https://ngrok.com/)). 

W związku z tym, że ta akcja dostępna jest wyłącznie w systemie macOS, nie będziemy poświęcać jej dużo czasu. Poza tym, jej implementacja jest bardzo prosta i sprowadza się do uruchomienia jednego polecenia. 

![](https://cloud.overment.com/2024-10-21/aidevs3_voice-85052875-b.png)

Od dłuższego czasu korzystam z powiadomień głosowych, które świetnie sprawdzają się jako przypomnienia oraz do informowania o zakończonych zadaniach.

Drugim przykładem akcji, którą wykorzystuję dla rozrywki, jest integracja ze Spotify. W poprzednich edycjach AI_devs korzystałem w tym celu ze scenariusza automatyzacji Make. Natomiast teraz dzięki logice wygenerowanej przez LLM, nawiązałem połączenie bezpośrednio z API.

Dzięki temu taki scenariusz:

![](https://cloud.overment.com/2024-10-21/aidevs_spotify-9f92b23b-5.png)

Został zastąpiony jedną klasą `tools/SpotifyService`, a odnalezienie i uruchomienie utworu sprowadza się do wywołania funkcji `await assistantService.playMusic('Title, artist');`. Jest to także potwierdzenie tego, co pisałem wyżej na temat narzędzi no-code oraz zmiany ich roli w obliczu coraz lepszych modeli językowych. 

> Ważne: Aby uruchomić narzędzie Spotify, musisz utworzyć aplikację na [developer.spotify.com](https://developer.spotify.com/dashboard) i wypełnić klucze w pliku .env. Następnie, po uruchomieniu aplikacji, przejdź na adres /spotify/auth (nasz localhost musi być dostępny w Internecie, a endpoint /spotify/callback dodany w panelu aplikacji developerskiej Spotify). To spowoduje, że tokeny zostaną dopisane do pliku .env (nie jest to praktyka zalecana na produkcji, ale w tym przypadku nie mamy bazy danych, więc musimy z tego skorzystać), a Spotify będzie dostępne po ponownym uruchomieniu serwera.

Sam przykład integracji ze Spotify również zawiera kilka ciekawych sugestii, ale opiera się o podobne schematy, co przykład z Google Maps. 

Konkretnie zapytania użytkownika mogą być bardzo ogólne i odnosić się do rzeczy takich jak:

- Play the track that was playing when Memphis saw Eleanor for the first time in Gone in 60 Seconds.

Czyli chodzi o odwołanie do konkretnej sceny z filmu "60 Sekund". Pomimo braku tytułu utworu, model korzystając ze swojej bazowej wiedzy, poprawnie go identyfikuje.

![](https://cloud.overment.com/2024-10-21/aidevs3_60seconds-1746bca9-a.png)

Baza Spotify nie jest kompletna, a czasem zawiera kilka wariantów tego samego kawałka. Dlatego w akcji `playMusic` widocznej poniżej nie tylko korzystam z wyszukiwarki (`this.searchMusic`), ale także korzystam z promptu `spotifyPlayPrompt`, którego zadaniem jest podjęcie **decyzji** o tym, który rekord z wyników wyszukiwania uruchomić. 

![](https://cloud.overment.com/2024-10-21/aidevs3_spotify-21d80041-0.png)

Wyniki wyszukiwania Spotify zawierają wiele szczegółowych informacji, które z perspektywy naszej integracji można pominąć. Dlatego używam funkcji pomocniczej `formatMusicSearchResults`, aby wybrać tylko te właściwości, które są istotne. Jest to podyktowane także ograniczaniem 'szumu' i dążeniem do utrzymania uwagi modelu na zadaniu. 

![](https://cloud.overment.com/2024-10-21/aidevs3_formatting-5afa34b4-1.png)

Wnioski:

- Tworzenie narzędzi dla agenta może także nawiązywać do naszego hobby czy zainteresowań. Nawet jeśli ich użyteczność będzie podważalna, to i tak budując je, zdobywamy doświadczenie przydatne w innych sytuacjach
- Kreatywne rozwiązywanie problemów, szczególnie w przypadku gdy budujemy coś na potrzeby własne bądź wewnątrzfirmowe jest bardzo wskazane. Nie wszystkie aplikacje i usługi posiadają oficjalne API i czasem musimy poszukać alternatywnych ścieżek
- Po raz kolejny przekonaliśmy się, że zbudowanie warstwy pośredniej pomiędzy LLM, a naszą aplikacją, jest wskazane. Pozwala to nam na utrzymanie kontroli pomiędzy formatem wymiany danych oraz transformacją zapytań
## Dobre praktyki

Zbierając w całość dobre praktyki na temat budowania narzędzi dla modelu: 

- **Jeden prompt = jeden problem**: rozbudowane zadania powinny być podzielone na mniejsze kroki, a model w danej chwili musi otrzymywać minimum informacji
- **Generalizacja problemu**: problemy mają swoją przyczynę, którą należy odkryć i zaadresować. Jeśli prompt nie działa w sytuacji X, nie próbuj jej rozwiązać, lecz znaleźć jej powód lub schemat według którego działa model
- **Pomoc ze strony modelu**: w planowaniu, pisaniu kodu, pisaniu promptów, generowaniu zestawów danych testowych, debugowaniu — **zawsze pracuj wspólnie z modelem**
- **Seria akcji:** narzędzia powinny być projektowane tak, aby możliwe było wykonanie wielu zapytań jednocześnie. W ten sposób model będzie miał możliwość zebrania wszystkich potrzebnych informacji za jednym razem, co przekłada się pozytywnie na ogólną efektywność. 
- **Wspólny interfejs**: wartość łączenia modelu z narzędziami nie polega tylko na ich bezpośrednim połączeniu, ale na możliwości podłączenia wielu narzędzi, po które model sięga wtedy, gdy jest to konieczne.
- **Komplet informacji**: narzędzia zawsze muszą zwracać komplet informacji na temat pozyskanych danych lub błędów, które miały miejsce. W sytuacji gdy dane nie będą kompletne i poprawnie oznaczone, agent nie będzie potrafił się nimi posługiwać.
- **Ograniczenia:** odciążanie modelu z podejmowania decyzji powinno być priorytetem nie tylko ze względu na stabilność systemu, ale także jego wydajność
- **Ułatwienia:** tam gdzie to możliwe, warto stosować ułatwienia albo w postaci narzędzi no-code, albo gotowych rozwiązań, które pozwolą nam się skupić na innych obszarach systemu
- **Obserwowanie:** wszystkie kroki związane z posługiwaniem się narzędziami, powinny być logowane i/lub zapisywane w bazie danych. Dostęp do tych informacji powinien mieć zarówno człowiek, jak i sam system (choć to zależy od jego przeznaczenia). Zgromadzone dane z czasem będą także użyteczne na potrzeby budowania zestawów danych testowych oraz dalszego kształtowania promptów. 
## Podsumowanie

Integrowanie LLM z otaczającymi nas usługami i urządzeniami poprzez budowanie narzędzi w taki sposób, aby model mógł się nimi swobodnie posługiwać, stanowi kolejny fundamentalny element agentów AI. 

Jeśli masz zabrać ze sobą z tej lekcji tylko jedną rzecz, to spójrz na przykłady implementacji narzędzi z katalogu `tools`. Następnie wybierz **jedno narzędzie, usługę bądź urządzenie** z Twojego otoczenia i sprawdź jak wygląda dostępność przez API. Wybierz takie, które oferuje możliwość integracji i zaplanuj akcje, które mogą być przydatne dla LLM.

Zastanów się też jak agent wyposażony w takie narzędzie, mógłby wnosić wartość Tobie, lub jak mógłby wspierać procesy wewnątrzfirmowe. Uwzględnij także możliwość połączenia z innymi narzędziami i podziel się swoimi przemyśleniami w komentarzu.