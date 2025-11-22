![](https://cloud.overment.com/s05e05-1730924179.png)

## Słowem wstępu

Każdy, kto uczestniczył w poprzednich edycjach AI_devs lub obserwuje mnie na X, Instagramie czy Linkedinie, wie, że "Alice", która pojawia się w treściach lekcji, ma również swoją drugą wersję, dostępną wyłącznie dla mnie. Wynika to z faktu, że poziom personalizacji tego projektu jest tak duży, że trudno było mi go udostępnić...

...do dziś.

Dotychczasowa podróż w AI_devs doprowadziła nas do miejsca w którym dość zrozumiałe stały się kluczowe aspekty związane z tworzeniem narzędzi, pracą z danymi, różnymi formatami plików czy rozwijania logiki agentów. Teraz dobrze byłoby na to spojrzeć zarówno z szerokiej perspektywy nieco większego projektu, ale też detali.

Istotną zmienną jest tutaj także fakt, że dzięki współpracy z Cursor, nawet jeśli pracujesz w innej technologii lub na co dzień skupiasz się na innych obszarach niż aplikacje backendowe, to i tak będziesz w stanie szczegółowo zapoznać się z moim kodem. Możliwość tą potwierdziły ostatnie tygodnie oraz osoby pracujące w Pythonie, .NET czy po prostu w obszarze front-endu lub innych specjalizacji.

Zatem w ostatniej lekcji AI_devs 3 skupimy się na omówieniu systemu, który **łączy wszystkie dotychczasowe koncepcje** i który w założeniu powinien pomóc Ci "połączyć kropki" lub przynajmniej pokazać, jak możesz stosować wiedzę z AI_devs 3 w praktyce. 
## AI_devs 3

Lekcje AI_devs 3 przeprowadziły nas przez **wszystko, co aktualnie wiemy na temat modeli**, technik **interakcji z nimi poprzez API**, **budowie interfejsów użytkownika**, **strukturyzowania i przetwarzania treści** oraz **budowaniu narzędzi** z myślą o dużych modelach językowych.

Każdy z przykładów miał formę "modułu" (jest to przenośnia, bo nie spełniają one definicji modułu), który zwykle skupiał się **tylko na jednym zadaniu**. Dzięki temu stopniowo zauważyliśmy, że możemy łączyć je ze sobą w praktycznie dowolnej kolejności. Natomiast w ostatnich lekcjach dowiedzieliśmy się także w jaki sposób możemy je rozbudować i sprawić, by pełniły rolę agentów współpracujących między sobą. 

Powiedziałem jednak, że do budowy zespołu agentów, warto dobrze opanować zbudowanie przynajmniej jednego z nich. 

"Alice" w mojej prywatnej wersji to projekt, który rozwijam od grudnia 2022. Sama jego forma stanowi kontynuację mojej koncepcji zespołu 'avatarów', którą rozpocząłem kilka lat wcześniej, gdy do dyspozycji miałem tylko kod oraz narzędzia no-code.

Przez cały ten czas Alice rozwijała się. Możliwości modeli językowych wzrastały, a nowe narzędzia pojawiały się regularnie. Moje doświadczenie również się powiększało. Uznałem więc, że AI_devs 3 to doskonała okazja, by nie tylko stworzyć kolejną wersję, ale także udostępnić kod projektu — "Alice AGI".

> "AGI" oczywiście należy traktować z przymrużeniem oka i nie brać tego dosłownie, aczkolwiek obecne możliwości projektu to całkiem dobra namiastka tego, jak może wyglądać nasza codzienność za jakiś czas.

![](https://cloud.overment.com/2024-12-03/aidevs3_agi-3c33ec7b-a.png)

## Zanim zaczniemy

Projekt "Alice AGI" udostępniam na swoim githubie, ale nie mam w planach rozwijania go w formie Open Source czy też publikowania aktualizacji z zachowaniem wstecznej kompatybilności. Ten projekt nadal będzie mieć zatem prywatny charakter. Co prawda sekcja "Issues" może posłużyć wymianie pomysłów czy sugestii, ale nic poza tym.

Naturalnie w projekcie występuje jeszcze sporo mniejszych i większych błędów, aczkolwiek z głównych funkcjonalności nowej wersji korzystam z powodzeniem od około 4 tygodni.

Nadrzędnym celem tego projektu na potrzeby tej lekcji, jest **przedstawienie tego, w jaki sposób wszystkie omówione koncepcje AI_devs 3 można połączyć w całość**. 

Jest to więc kopalnia wiedzy (przynajmniej według mnie) zarówno na temat tego, o czym mówiłem w lekcjach, ale także tego, o czym powiedzieć nie miałem okazji. 
## Koszty i czas reakcji 

Z jakiegoś powodu podczas rozmowy z drugą osobą na czacie, oczekiwanie kilku lub kilkunastu minut na odpowiedź jest dla nas w pełni akceptowalne. Jednak zupełnie inne oczekiwanie mamy wobec aplikacji i modeli językowych.

Dobrze więc wiedzieć, że w przypadku Alice AGI w obecnej formie, czas odpowiedzi rzadko spada poniżej jednej minuty. Wyjątkiem są zapytania klasyfikowane jako 'fast track', które nie wymagają zaangażowania logiki agenta.

![](https://cloud.overment.com/2024-12-03/aidevs3_latency-78ed28ba-b.png)

Podobnie jest także z kosztami, bo aktualnie sięgają one $0.3 za jedno zapytanie. Oczywiście jest tutaj ogromny potencjał na optymalizację i przejście na modele Claude 3.5 Haiku bądź GPT-4o-mini, co także zmniejszyłoby czas reakcji w przypadku części zadań.

![](https://cloud.overment.com/2024-12-03/aidevs3_costs-1bfbc1f7-6.png)

Warto więc już na wstępie mieć na uwadze fakt, że złożoność systemu przekłada się na zdecydowanie wyższy czas reakcji oraz stosunkowo wysokie koszty. Może się zatem okazać, że korzystanie z takiego rozwiązania będzie dla Ciebie nieopłacalne, albo że **warto zbudować taki, który będzie w dużej mierze opierać się o modele open source.** 

No bo nikt nie powiedział, że każdy agent musi być zbudowany dokładnie w taki sposób, a wszystkie moje założenia są poprawne. 
## Główna koncepcja

Koncepcja Alice AGI jest prosta i **polega na dążeniu do możliwie swobodnej rozmowy z aplikacją, która posiada wiedzę na mój temat oraz jest w stanie posługiwać się narzędziami z którymi pracuję.** Poniżej widać przykład takiej rozmowy, w wyniku której do mojej listy zadań został dodany nowy wpis.

![](https://cloud.overment.com/2024-12-04/aidevs3_chat-5ae58c40-0.png)

W przyszłości mogę wrócić do tego tematu i może mieć to miejsce **w nowej konwersacji**. Historia wcześniejszych wiadomości nie ma tutaj znaczenia, ponieważ potrzebne informacje są wczytane zarówno z mojej listy zadań w Linear, jak i pamięci długoterminowej modelu. Poniżej widzimy, że faktycznie Alice mówi o zakupie prezentów oraz przywołuje zainteresowania Kate. 

![](https://cloud.overment.com/2024-12-04/aidevs3_gifts-d84c21af-7.png)

Powyższe pytanie uruchomiło widoczną poniżej logikę w której widzimy nawiązanie połączenia z listą zadań oraz wczytanie informacji z pamięci długoterminowej. To, co widzimy poniżej, to oczywiście [Langfuse](https://langfuse.com/), który omawialiśmy w pierwszych tygodniach AI_devs.

![](https://cloud.overment.com/2024-12-04/aidevs3_report-cf026e82-0.png)

Rozmowa oczywiście może być kontynuowana i poniżej widzimy odpowiedź wygenerowaną na podstawie wyszukiwania w Internecie, ponieważ domyślnie model nie posiada informacji na temat produktu "Arc Ultra".

![](https://cloud.overment.com/2024-12-04/aidevs3_ideas-96f7f822-0.png)

Nie zawsze jednak może być to w pełni swobodna rozmowa, ponieważ wiemy, że model nie jest w stanie domyślić się wszystkiego. Poza tym, jesteśmy ograniczeni dostępnymi narzędziami, czy w ogóle możliwością interakcji z nimi z poziomu kodu — obie te rzeczy omawialiśmy w lekcjach AI_devs 3.

W tej chwili może pojawiać się pytanie: **dlaczego obsługiwać te narzędzia z pomocą czatu, a nie samodzielnie?**

Przede wszystkim, jedno nie wyklucza drugiego. Natomiast możliwość przywołania informacji z kilku źródeł lub dodanie kilku wpisów za pomocą jednej wiadomości jest często prostsze niż przełączanie się między narzędziami. Po drugie, możliwość przesłania wiadomości jest dostępna także z poziomu automatyzacji czy zewnętrznych usług, o czym również wspominałem w lekcjach. Co więcej, we wpisie "[Jak pracuję z LLM?](https://bravecourses.circle.so/c/dyskusje-ai3/jak-pracuje-z-ai-material-bonusowy?login_token=WjXMQxUS24pwtFwCdZ84ejK5eKNrBk2tLX7c#comment_wrapper_51468273)" mówiłem także o tym, że dokładnie te same możliwości są dla mnie dostępne na Slacku, w zegarku, czy w samochodzie.

![](https://cloud.overment.com/2024-12-04/aidevs3_interfaces-84314d33-9.png)

Zobaczmy więc, jak to wszystko działa.
## Zestaw narzędzi

Pomimo wzrastającej popularności frameworków, które już dziś pojawiają się w ogłoszeniach o pracę firm takich jak Amazon, Cloudflare czy Apple, zdecydowałem się na pracę z [Vercel AI SDK](https://sdk.vercel.ai) w celu połączenia z modelami OpenAI oraz Anthropic. Natomiast poniższy zrzut ekranu wskazuje na możliwy wzrost znaczenia frameworków w przyszłości. Warto zatem monitorować ich rozwój, testować nowe wersje, a po zakończeniu AI_devs rozważyć zapoznanie się z LangGraph, który według opinii niektórych z Was zasługuje na uwagę.

![](https://cloud.overment.com/2024-12-04/aidevs3_crew-0d211d9a-9.png)

Pomimo tego, że jest to "jedynie" SDK, to i tak zdążyłem już spotkać ograniczenia wymagające pominięcia jej przy obsłudze audio. Natomiast i tak projekt jest bardzo solidnie prowadzony i jak dotąd postrzegam wybór AI SDK jako właściwy. Jednocześnie zaimplementowanie reszty logiki było na tyle proste, że nie widzę powodu, aby na ten moment sięgać po frameworki, które zrobią to za mnie. 

Główny kod aplikacji tworzę w Node.js, wykorzystując framework [hono.dev](https://hono.dev/), z którym pracuję po raz pierwszy. Podobnie, debiutuję w pracy z SQLite w połączeniu z [Drizzle ORM](https://orm.drizzle.team/). Te decyzje skutkują bardzo małą listą zależności projektu, gdzie większość bibliotek jest związana z narzędziami używanymi przez agenta.

Zatem zarówno framework, baza danych, jak i struktura katalogów aplikacji jest dopasowana do małego projektu, ponieważ takie jest też jego założenie. Zależy mi na tym, aby całość była tak prosta, jak to możliwe, ale opierała się o solidne fundamenty (choć te moim zdaniem w tej chwili są jeszcze dyskusyjne). 

![](https://cloud.overment.com/2024-12-04/aidevs3_structure-315b6ae2-4.png)

Mamy więc kilka plików konfiguracyjnych, pliki migracji bazy danych, funkcje middleware, katalogi z promptami, ścieżkami, serwisami oraz kilka funkcji pomocniczych. Najwięcej dzieje się naturalnie w akcjach przypisanych do **ścieżek** (katalog routes) oraz poszczególnych **serwisach**. Całkiem istotne są także funkcje **middleware**, które dbają o transformację zapytań z formatów OpenAI/Anthropic na format Vercel AI SDK.

No i oczywiście w temacie rozwoju promptów oraz obserwowania aplikacji, do gry wchodzi tutaj Langfuse oraz Promptfoo (aczkolwiek ten nie jest jeszcze podłączony). Sama integracja odbywa się bezpośrednio przez oficjalne SDK, co daje kontrolę nad monitorowanymi zdarzeniami. 

![](https://cloud.overment.com/2024-12-04/aidevs3_langfuse-902181b8-5.png)

Nie zdecydowałem się jedynie na podłączenie promptów pod Langfuse, ale nie wykluczam tego w przyszłości. Po prostu na ten moment, prompty obecne w plikach projektu wydają się wystarczającym rozwiązaniem. 
## Główna logika

Logika Alice AGI to zmodyfikowana wersja przykładu logiki agenta, którą omawialiśmy w kilku ostatnich lekcjach. 

Co prawda warto spojrzeć na nią z lekkim dystansem, ponieważ opiera się wyłącznie o moje doświadczenie i już na tym etapie nie mam żadnych publikacji czy przykładów, które są w stanie poprzeć moje założenia. 

Trudno mi więc na tym etapie określić możliwości tego systemu, choć ostatnie tygodnie pokazały mi, że są one znacznie lepsze od tego, z czym pracowałem do tej pory. 

![](https://camo.githubusercontent.com/f3f679cbbf018892d56cf462707a1b8b5d0ad2097dffd66b5134b59c1a90fa4c/68747470733a2f2f636c6f75642e6f7665726d656e742e636f6d2f323032342d31322d30332f6c6f6769632d30303538313362642d392e706e67)

Mamy więc tutaj:

- Główny endpoint `chat`, który przyjmuje i wysyła dane zgodne z formatem OpenAI. Wspiera także dodatkową właściwość `conversation_uuid`, o której mówiłem w kontekście rozpoznawania wątków.
- Etap "fast track" to klasyfikacja zapytania pod kątem tego, czy odpowiedź wymaga uruchamiania pełnej logiki agenta. Ułatwia to prowadzenie rozmowy, ponieważ nie zawsze wiadomości wymagają podejmowania nowych akcji.
- Etap "observe" polega na kompresji informacji pochodzących z otoczenia oraz profilu użytkownika. Dochodzi tutaj także do naszkicowania wstępnego planu działań.
- Etap "reasoning loop" zawiera w sobie niemal tę samą logikę, którą omawiałem w przykładzie `assistant`. Mamy więc tam planowanie zadań, oraz akcji które muszą być podjęte w związku z nimi.
- Etap "response" to po prostu wygenerowanie odpowiedzi na podstawie wszystkich dostępnych informacji

Jest to stosunkowo prosta logika, która pozwala na połączenie agenta z zestawem narzędzi, które także omawialiśmy w AI_devs 3. Chciałbym jednak, aby na tym etapie już nic nie pozostawiało wątpliwości.

Poniżej mamy nasz główny endpoint. Cała logika sprowadza się tutaj do:

- Ustalenia stanu konwersacji, czyli wczytania wszystkich niezbędnych danych.
- Klasyfikacji zapytania pod kątem tego, czy może zostać zaadresowane bez fazy "myślenia"
- Wygenerowania odpowiedzi albo w formie zwykłej odpowiedzi, albo strumieniowania. 

![](https://cloud.overment.com/2024-12-04/aidevs3_agi-c4450c32-7.png)

Dodatkowo, zanim jeszcze zostanie uruchomiona powyższa akcja, dane przechodzą przez zestaw funkcji "middleware". Odpowiadają one między innymi za zabezpieczenie ścieżek przed zbyt dużą liczba zapytań oraz nieautoryzowanym dostępem. Także wszystkie zapytania (poza kilkoma wyjątkami) muszą posiadać nagłówek `Authorization` ustawiony na `Bearer API_KEY` (wartość tego klucza należy ustawić w pliku .env na dowolną wartość).

![](https://cloud.overment.com/2024-12-04/aidevs3_middleware-fb851304-3.png)

To, co niebawem ulegnie tutaj zmianie, dotyczy sposobu strumieniowania informacji tak, aby rozpoczęło się ono **od razu**. Nawiązuje to do jednej z ostatnich aktualizacji AI SDK "non-blocking data streams" o której wspominałem w lekcji S05E04.

Takie strumieniowanie, lub przejście na komunikację opartą o zdarzenia jest istotne zarówno ze względu na długi czas odpowiedzi, jak i w ogóle możliwość obserwowania i ewentualnego wpływania na proces. 

No bo jeśli spojrzymy sobie na metodę `think`, to jej wykonanie zajmuje najwięcej czasu i tam możemy mieć potrzebę **przerwania wykonania** lub **nawiązania kontaktu z użytkownikiem**. 

![](https://cloud.overment.com/2024-12-04/aidevs3_loop-dc050d6c-e.png)

Skoro już jesteśmy przy fazie `thinking`, to wewnątrz niej działają następujące zapytania:

- **observe**: wykonywane są tam dwa prompty, które pobierają tylko istotne informacje z **otoczenia** oraz **profilu użytkownika**. Chodzi o to, że z wielu dostępnych danych wydobywamy tylko te, które są kluczowe w danym momencie.
- **draft**: tutaj także wykonywane są dwa prompty. Jeden z nich generuje notatki na temat potencjalnie istotnych obszarów pamięci do przeszukania, a drugi robi to samo z listą narzędzi. Inaczej mówiąc, tutaj agent wstępnie zastanawia się, co zrobić. Jest to istotne, ponieważ taka refleksja zwykle jest poprawna i wzmacnia nacisk na podjęcie tych działań.
- **plan:** etap planowania dąży do wygenerowania **listy zadań** potrzebnych do udzielenia odpowiedzi.
- **next:** tutaj dochodzi do wyboru **kolejnej akcji** w ramach wybranego przez model zadania.
- **use:** polega na wygenerowaniu danych potrzebnych do uruchomienia akcji. W przypadku Function Calling, byłoby to wygenerowanie argumentów potrzebnych do uruchomienia funkcji. W moim przypadku jest to po prostu zwykły obiekt JSON
- **act:** tutaj akcja zostaje wykonana, a jej rezultat zostaje zapisany w bazie danych i wpływa na wykonanie kolejnego obrotu pętli

No i klasycznie, pętla `while` jest ograniczona programistycznie w taki sposób, że zostanie przerwana, gdy dojdzie do wyboru akcji `final_answer` lub gdy zostanie przekroczona dopuszczalna liczba kroków.

Powyższe podejście sprawdza się świetnie w przypadku zadań, których plan można ustalić od razu, ale ma jeszcze problemy ze scenariuszami, które wymagają znaczącej zmiany podejścia w trakcie wykonywania. Są to dość rzadkie scenariusze występujące w najbardziej złożonych zadaniach, ale jednak się zdarzają. 
## API

API opiera się przede wszystkim o główny endpoint `/api/agi/chat`, ale nie jest to jedyny adres, na który możemy kierować zapytania. 

- `POST /api/conversation/new`: pozwala utworzyć nowy wątek rozmowy i zwraca jego identyfikator. Jest to przydatne w kontekście integracji z zewnętrznym interfejsem, np. Siri Shortcuts
- `GET /api/conversation`: pobiera konwersację, która miała miejsce w ciągu ostatnich 15 minut. To również jest przydatne w kontekście integracji z zewnętrznym interfejsem. Warunkiem jest tutaj wykluczenie interakcji, które nie zostały uruchomione automatycznie, np. na potrzeby automatyzacji czy harmonogramu zadań
- `GET /api/auth/spotify/authorize`: pozwala na nawiązanie połączenia ze Spotify przez oAuth 2.0
- `GET /api/auth/google/authorize`: pozwala na nawiązanie połączenia z API Google (Calendar / YouTube / Gmail) przez oAuth 2.0
- `GET /api/files/:uuid`: pozwala na wczytanie treści pliku/dokumentu na podstawie jego UUID
- `POST /api/upload`: pozwala na wgranie pliku i powiązanie go z konwersacją
- `POST /api/tools/memory`: pozwala na dodanie dodanie nowego wspomnienia, bez angażowania pełnej logiki agenta
- `POST /api/tools/memory/search`: pozwala na dostęp do pamięci agenta, bez angażowania jego pełnej logiki
- `PATCH /api/tools/memory/:uuid`: pozwala na aktualizację wybranego wspomnienia

Część pozostałych narzędzi również posiada własne endpointy, ale nie będę ich tutaj wymieniał, ponieważ nie odgrywa to już zbyt istotnej roli. Kluczowe jest natomiast to, że niektóre z umiejętności asystenta są dostępne bezpośrednio. Także z poziomu automatyzacji czy skryptów, które precyzyjnie dostarczają jakieś informacje, nie ma sensu kierować zapytania na główny endpoint. 

Natomiast zapytania ze strony użytkownika, zawsze są kierowane na `/api/agi/chat` i tam agent podejmuje decyzję o tym, co należy z nimi zrobić.
## Baza danych

Struktura bazy danych także wygląda dość znajomo w porównaniu do tego, co omawialiśmy w lekcjach. Jednak tutaj mamy kilka dodatkowych tabel, co widać na poniższym schemacie (otwórz go w nowej karcie):

![](https://cloud.overment.com/2024-12-04/aidevs3_db-3c9532c0-9.png)

- `users`: to klasyczna tabela przechowująca dane użytkowników. Nietypowe są jednak tutaj pola **environment** (JSON) oraz **context** (text) i ich rolą jest przechowywanie aktualnych danych na temat otoczenia oraz ogólnego profilu użytkownika, o których wspominałem przed chwilą.
- `conversations`: to lista interakcji przypisanych do użytkownika oraz listy wiadomości. Wyodrębnienie tej tabeli jest istotne, bo można rozpocząć wątek przed interakcją użytkownika. Na przykład, przy wgrywaniu plików do nowej rozmowy, zakładamy wątek, do którego użytkownik będzie mógł później przesyłać wiadomości.
- `messages`: tutaj mamy listę wiadomości, lecz wspierają one także możliwość przechowywania obrazów. Są także połączone z tabelą `documents` dzięki czemu możliwe jest powiązanie plików z konkretną wiadomością. 
- `categories & memories`: to bazowa struktura wspomnień. Każde ze wspomnień również jest powiązane z tabelą `documents`, której wpisy są (ale nie zawsze) indeksowane w silnikach wyszukiwania
- `tools`: to lista narzędzi, ich opisów oraz instrukcji wykonania. Narzędzia przypisywane są do akcji. 
- `tasks`: to lista zadań, które muszą zostać wykonane w celu udzielenia odpowiedzi. Rezultat zadania ma formę wpisu w tabeli `documents`
- `actions`: to lista akcji, które muszą zostać wykonane **w ramach jednego z zadań**. Rezultat akcji ma formę wpisu w tabeli `documents`
- `jobs`: to lista zadań wywoływanych według harmonogramu. Tutaj istnieje powiązanie z tabelą `tasks` oraz niebezpośrednio z `conversations`. W ten sposób, gdy nadchodzi odpowiedni moment, system wysyła wiadomość 'sam do siebie' i podejmuje zlecone zadanie.

Widać tutaj wyraźnie, jak istotną rolę odgrywa tabela `documents`. Jej wpisy pojawiają się praktycznie wszędzie, ale możemy korzystać z nich w jednolity sposób. Nie ma znaczenia, czy "dokumentem" jest plik, wynik działania akcji, czy informacja o błędzie - każdy z nich można przetwarzać według tych samych zasad.

Ogólna struktura bazy danych w jej obecnej formie, ma jednak przynajmniej kilka wad oraz mniejszych nieścisłości. 

Dla przykładu mam wątpliwość czy `tasks` powinno mieć powiązanie z konwersacją, czy z `messages`. Powodem jest fakt, że bez tego nie jestem w stanie odtworzyć pełnej historii interakcji. Obecnie nie stanowi to problemu, ale może się nim stać w przypadku najbardziej złożonych zadań. Nie jestem także przekonany do struktury dokumentów, ale ponownie, obecnie nie mam z tym problemu. 

Wniosek jest taki, że obecna struktura bazy danych jest bardzo elastyczna, a zarazem stosunkowo prosta i generyczna. Może stanowić fundament dla różnego rodzaju agentów, choć sama w sobie w obecnej formie nie przewiduje interakcji `agent - agent`.
## Dostępne narzędzia

Na ten moment Alice AGI posiada dostęp do 14 narzędzi i 33 umiejętności (konkretnie jest ich 37, ale mamy dwa rodzaje wyszukiwania). W skład narzędzi wchodzą te najbardziej podstawowe, takie jak **pamięć, dostęp do Internetu, listy zadań czy kalendarza**. Jest także możliwość przetwarzania plików oraz dostęp do usług pozwalających na wysłanie maila czy sterowanie muzyką. 

![](https://cloud.overment.com/2024-12-04/aidevs3_tools-d5922d29-0.png)

Jeśli chodzi o narzędzia, opieramy się dokładnie o te same koncepcje, które omawialiśmy. Poza drobnymi porządkami, jest to kod pochodzący wprost z repozytorium przykładów AI_devs 3. 

Podłączenie nowego narzędzia, opiera się tutaj o kilka kroków.

1. Utworzenia serwisu w katalogu `src/services` na wzór tych istniejących. Kluczową funkcją jest tam `execute`, która przyjmuje `nazwę akcji` oraz `payload`. W pliku `spotify.service.ts` znajduje się dobry przykład. 

![](https://cloud.overment.com/2024-12-05/aidevs3_execute-6f44d469-a.png)

2. Następnie serwis musi zostać dodany w pliku `config/tools.config.ts`, bo dzięki temu będzie dostępny w metodzie `act` z pliku `ai.service.ts`

![](https://cloud.overment.com/2024-12-05/aidevs3_services-0c3f8e5c-3.png)

3. W bazie danych musi zostać dodany wpis do tabeli `tools`, również na wzór tych istniejących. Wiemy też, że tam — nazwa musi być krótka i unikatowa, opis musi wyjaśniać kiedy z tego narzędzia należy skorzystać, a instrukcja opisywać sposób wygenerowania danych do jej uruchomienia.

No i właściwie nic więcej nie jest potrzebne do dodawania nowych narzędzi. Oczywiście w ramach jednego narzędzia można mieć wiele akcji, co jest bardzo wskazane. Warto więc zapoznać się z istniejącymi już narzędziami, aby na ich podstawie podjąć decyzję o dalszych krokach.

Także podsumowując kwestię głównej logiki, **Alice AGI to tak naprawdę połączenie dwóch rzeczy — narzędzi, które budowaliśmy w lekcjach, oraz logiki agenta, którą omawialiśmy w tym tygodniu.** 

## Uruchomienie projektu

Szczegóły na temat uruchomienia projektu zostały opisane przeze mnie w pliku README.md. W skrócie należy:

- pobrać repozytorium projektu: [pobierz](https://github.com/iceener/ai)
- zainstalować zależności: `bun install`
- przeprowadzić migrację bazy danych: `bun migrate`
- wypełnić ją początkowymi danymi: `bun seed` (można je dostosować w pliku `seed.ts`)
- skopiować plik `.env-example` i zmienić jego nazwę na `.env`
- wewnątrz pliku `.env` należy ustawić `API_KEY` na dowolną wartość, oraz klucze API dla OpenAI, Anthropic i wszystkie zmienne dla Langfuse, Qdrant, Algolia. Pozostałe zmienne są opcjonalne, ponieważ są bezpośrednio powiązane z narzędziami, które i tak trzeba dopasować do własnych potrzeb, lub stworzyć własne.

>> Konfiguracja <<  

Zatem samo uruchomienie projektu, nie jest szczególnie skomplikowane. Dobrze jednak zapoznać się ze strukturą narzędzi oraz logiki agenta. Nie bez powodu dołączam zestaw przykładowych integracji, ponieważ są one dobrym punktem odniesienia. 

Po uruchomieniu projektu, potrzebny nam będzie jeszcze graficzny interfejs. Tutaj możliwe jest podłączenie pod aplikację Alice (3-miesięczny trial dla AI_devs 3 dostępny jest [tutaj](https://bravecourses.circle.so/c/dyskusje-ai3/dostep-do-alice?login_token=6b8Zfn2abL7iLfJvhWnbgpgCmCmyQFdk28Qz#comment_wrapper_51552013)) lub poprzez szablon aplikacji Tauri, który publikowałem [tutaj](https://bravecourses.circle.so/c/dyskusje-ai3/wlasna-aplikacja-desktopowa-szablon-tauri). 

Na filmie poniżej pokazuję możliwości Alice AGI w zakresie posługiwania się narzędziami. Widać tutaj także wyraźnie aktualne ograniczenia modeli językowych (np. szybkość działania), ale także możliwości związane z przetwarzaniem poleceń zapisanych w naturalnym języku. 

>> Interfejs <<

Alice AGI jasno pokazuje to, że obecnie zbudowanie wyspecjalizowanego agenta, poruszającego się po określonym obszarze, jest już w pełni możliwa. Podobnie wygląda to w zastosowaniach produkcyjnych, choć tutaj ilość ograniczeń, które będziemy chcieli nałożyć na system, będzie odpowiednio większa, ponieważ ilość zmiennych wpływających na jego działanie, rośnie bardzo szybko.

## Alice AGI w praktyce

Alice AGI to projekt-piaskownica. Można więc go wykorzystać do nauki i eksplorowania możliwości modeli, albo z góry określić jego zakres, wdrożyć i po prostu patrzeć jak dla nas pracuje. W moim przypadku są to oba scenariusze, ponieważ projekt nieustannie ewoluuje, ale też coraz większy zakres funkcjonalności pozostaje ze mną na stałe.

W moim przypadku na stałe są ze mną:

- Głosowe dodawanie zadań, szczególnie gdy jestem poza domem. Możliwość podyktowania wiadomości, która zamienia się na zadania, wciąż robi na mnie wrażenie.
- Dodawanie wydarzeń w kalendarzu przez wiadomość na Slacku, gdy nie mam możliwości swobodnie mówić ze względu na hałas bądź wprost przeciwnie, ciszę, ale w otoczeniu innych.
- Pamięć długoterminowa — tutaj jest trochę prywaty (ale bez przesady). Wpisy na temat przeczytanych przeze mnie książek, prowadzonych projektów, testów osobowości czy luźnych notatek pozwalają na prowadzenie jakościowej dyskusji sprawiającej wrażenie, że po drugiej stronie jest ktoś, kto mnie zna. Choć omówienie niektórych tematów nadal sprawia wrażenie rozmowy z botem, tak nierzadko wśród wymienionych wiadomości pojawiają się sugestie na które bym nie wpadł. Aktualnie moduł pamięci jest przeze mnie modyfikowany ze względu na inspirację projektem AGI Memory
- Automatyzacje działające według harmonogramu lub zdarzeń. To akcje podłączone do mojej listy zadań, katalogów na Google drive czy nawet chwili w której bluetooth łączy się z moim samochodem. W zależności od kontekstu otrzymuję wiadomość lub po prostu uruchamia się jakaś akcja. Przykładem może być współpraca z osobą odpowiedzialną za montaż części z moich filmów — tam komunikacja, zadaniami oraz rozliczeniem, w pełni zarządza Alice.
- No i oczywiście fun. Nie bez powodu tak dużo w AI_devs było Spotify, zapalania światła czy sterowania akcjami w samochodzie przez API. Uważam, że właśnie te najbardziej absurdalne akcje, które z pozoru są bezużyteczne, uczyły mnie najwięcej.

Oczywiście nie wszystko zawsze jest idealne, ale największe problemy są związane z trzema obszarami — niedostępnością API modeli i/lub zewnętrznych usług, niedostępnością Internetu w podróży lub w niektórych pomieszczeniach, np. w garażu, brakującymi funkcjonalnościami lub ograniczeniami tych istniejących.

Same ograniczenia modeli językowych praktycznie już nie występują, ale mowa tutaj o sytuacji, w której sam jestem użytkownikiem tego systemu. Przekazanie go w ręce innych osób ogranicza się tylko do pojedynczych akcji lub umiejętności (np. tłumaczenia bądź korekty dokumentu na podstawie adresu URL w Notion). Powodem jest fakt, że tak "otwarty" system nadal trudno dopasować do potrzeb dowolnego użytkownika. Nawet integracja z kalendarzem w przypadku osoby pracującej na kilku kontach to już zupełnie inny temat niż integracja z pojedynczym kalendarzem.

Zarówno współpraca z dotychczasowymi wersjami Alice AGI, jak i sama budowa, jasno pokazują mi, że: 

- rozwój modeli nadal trwa i bynajmniej nie widzę tutaj spowolnienia
- większość wskaźników takich jak większy kontekst, czy spadające ceny, mają mniejsze znaczenie, niż twierdzą komunikaty marketingowe
- nadal nie wiemy praktycznie nic na temat natury modeli językowych. Zdarza mi się chodzić nietypowymi ścieżkami i nieustannie zaskakiwać się tym, co jest możliwe lub wprost przeciwnie
- warto obserwować ludzi stojących za tą technologią, narzędziami i badaniami. Jednak bezwarunkowo należy pamiętać, że są to tylko ludzie, a na przestrzeni nawet dwóch ostatnich lat duża część powszechnie uznawanych 'prawd' została podważona lub okazała się błędna od samego początku
- nic nie daje większej wartości, niż samodzielna eksploracja i budowanie, połączone z wymianą pomysłów w gronie osób, które uważają tak samo

Ostatecznie nie wiem, czy projekt Alice AGI lub choć sama idea, pozostaną z Tobą na dłużej. Mam jednak nadzieję, że ostatnie tygodnie były dla Ciebie wartościowe i znajdziesz praktyczne zastosowanie tej wiedzy i umiejętności w Twojej codzienności.
## Kolejny rozdział

Patrząc na ostatnie dwa lata rozwoju generatywnego AI, widzimy, że początkowo mogliśmy pytać o odpowiedzi, później o działania, a następnie serie działań. 

Dziś możemy dość swobodnie rozmawiać z modelem, a nawet stawiać przed nim cele, które samodzielnie jest w stanie osiągnąć. Wymaga to jednak znajomości natury modeli, a także programistycznej wiedzy. Pozwala to na zaplanowanie systemu w taki sposób, aby mógł spełniać swoje zadanie w sposób przewidywalny lub na tyle skuteczny, aby jego zastosowanie miało sens.

AI_devs 3 właśnie dobiegło końca. Oznacza to, że w tej chwili rozpoczyna się kolejny rozdział historii współpracy ze Sztuczną Inteligencją, którego część ... napiszesz Ty. 

Myślę, że teraz już każdy zgodzi się ze mną, że generatywne AI jest już nieodłączną częścią naszej pracy. Całkiem jasne jest także to, że przynajmniej na ten moment, budowanie kompleksowych systemów nadal możliwe jest tylko poprzez **połączenie naszego doświadczenia z możliwościami nowych technologii**. I nawet jeśli dziś spotykamy jeszcze bariery wynikające bezpośrednio z umiejętności obecnych modeli, to nawet wczorajsza premiera `o1` sugeruje, że część z nich niebawem zniknie, ale niewiele wskazuje na to, że wydarzy się to "jutro".

---

Z całego serca dziękuję Ci za udział w AI_devs 3 ♥️ Dla mnie prowadzenie tego szkolenia to zaszczyt, szczególnie biorąc pod uwagę to, że Twoja obecność tutaj to oznaka zaufania wobec mnie, mojej wiedzy, umiejętności oraz doświadczeń za które jestem Ci wdzięczny.

Zdaję sobie sprawę z tego, że w tej edycji nie wszystko było idealne oraz, że tu i tam pojawiały się mniejsze lub większe trudności. Jednak fakt, że czytasz te słowa sugeruje, że materiał był na tyle interesujący, aby było warto przez niego przejść.

Na koniec mam więc prośbę o dopisanie się do naszej "Ściany Miłości" z pomocą [tego formularza](https://app.easy.tools/review-ask/68a7fc7cc8444718ab3f0469f3eb9d8c?lang=pl). Jeśli chcesz też zostawić sugestie i/lub feedback na temat szkolenia, to niebawem prześlemy także dedykowaną ankietę w tej sprawie. 

![](https://cloud.overment.com/2024-12-05/aidevs3_love-b2f343f1-c.png)

Specjalne podziękowania kieruję także do:

- Jakuba oraz Mateusza — za opracowanie fabuły oraz systemu zadań oraz niezwykły klimat przy organizacji największego szkolenia online w mojej historii.
- Pawła Dulaka — za niezwykłe zaangażowanie oraz wsparcie przy obsłudze szkolenia oraz testowania zadań
- Pauli Skrzypeckiej — za merytoryczne i zabawne spotkanie, które rzuciło światło na odpowiedzialne wdrażanie systemów w których pojawia się GenAI
- Michałowi Furmankiewiczowi — za świetne spotkanie, które pokazało, że systemy GenAI już teraz są wdrażane w dużych organizacjach
- Mariuszowi Korzekwie, Dominikowi Fudziekiwieczowi oraz Pawłowi Manowieckiemu — za inicjatywy w postaci nieoficjalnego Discorda oraz meetupów OpenAI Devs
- Mateuszowi Szmigielowi, Mateuszowi Tomkiewiczowi, Bartkowi Karalus, Piotrowi Brzyskiemu — za inicjatywy spotkań AI_devs w różnych miastach
- Zespołu brave.courses — za bezbłędną organizację szkolenia i zadbanie nawet o najmniejsze detale związane z promocją, zewnętrznymi współpracami, wydarzeniami, oprawą graficzną oraz wszystkimi formalnościami
- Zespołu easy.tools — za obsługę płatności oraz pomoc w zakresie integracji naszego systemu zadań
- Alice — za burze mózgów i pomoc przy rozwiązywaniu problemów z przykładami, które wydawały się niemożliwe do rozwiązania.
- oraz przede wszystkim — Katarzynie Gospodarczyk i Grzegorzowi Rogowi — za ich obecność.

Do zobaczenia,
Adam