![](https://cloud.overment.com/S05E04-1732627999.png)

Kilkukrotnie wspominałem, że warto projektować agentów AI z myślą o jasno określonym obszarze. Ponadto ich kontakt ze światem zewnętrznym powinien być ograniczany, aby wyeliminować część problemów "by design".

Prawda jest taka, że agent będzie musiał wchodzić w interakcję ze światem, a być może nawet z użytkownikami. Nie zawsze jednak przyjmie to formę czatu czy rozmowy głosowej, ponieważ nikt nie mówi, że to jedyne formy interakcji, jakie mamy do dyspozycji.

Zmierzam jednak do tego, że **warto podejść rozsądnie, ale i odważnie, zarówno do budowy agentów**, jak i zarządzania ich dostępem do informacji oraz listą zadań. W tym celu pomocne okażę się wszystko, czego do tej pory dowiedzieliśmy się na temat samych modeli, a także zasugerowanych przeze mnie zasad projektowania narzędzi.
## Interakcja z użytkownikiem

Przekonaliśmy się wiele razy, że sterowanie zachowaniem modelu wymaga precyzji i nie możemy liczyć na czytanie w myślach. Problem polega na tym, że użytkownicy nieświadomi ograniczeń LLM nadal mają takie oczekiwania i przekłada się to na sposób korzystania z narzędzi, które tworzymy oraz finalnie — ich doświadczenia.

Poza tym, trudno obecnie stworzyć agenta zdolnego do wykonania każdego zadania. Tym bardziej, że są też takie, które mogą położyć nawet najlepszy system. 

![](https://cloud.overment.com/aidevs3-1732788448.png)

A tak poważnie, w takiej sytuacji system powinien poinformować użytkownika o braku dostępnych umiejętności oraz o ewentualnych opcjach, które są dostępne. Problem w tym, że w przypadku interfejsu czatu, nie jesteśmy w stanie przewidzieć wszystkich możliwych zapytań. Wiemy także, że ze względu na podatność modeli na prompt injection, trudno mówić o pełnym zabezpieczeniu zarówno przed atakami, jak i zwykłymi pomyłkami.

Oczywiście odpowiedź powyżej, powinna wyglądać mniej więcej tak: 

![](https://cloud.overment.com/2024-11-28/aidevs3_fallback-92605464-7.png)

Kolejną kwestią jest sam sposób komunikacji, który zdecydowanie inaczej wygląda w przypadku osoby posiadającej wiedzę na temat możliwości agenta. Przykład tego widać poniżej, ponieważ moja prośba odwołuje się do dostępnych integracji z **Linear**, **Google Calendar**, **CoinMarketCap** czy **Resend**. 

![](https://cloud.overment.com/2024-11-28/aidevs3_report-e2492c61-f.png)

Nawet pomimo tego, że moja prośba zaczynała się od "wyślij mail", a potem wymieniała poszczególne aktywności, to agent poprawnie ustalił kolejność tych zadań. Także elastyczność systemu jest wysoka, ale z pewnością nie jest **nieograniczona**.

Co więcej, w przypadku złożonych zadań może dojść do problemów z zewnętrznymi usługami. Ale jeśli związane z nimi akcje nie są krytyczne, to nie powinny zaburzyć realizacji pozostałej części zadania. Widać to poniżej, ponieważ Alice poinformowała mnie o tym, że w tym przypadku nie była w stanie pobrać wydarzeń z mojego kalendarza. 

![](https://cloud.overment.com/2024-11-28/aidevs3_daily-aca638f9-2.png)

Powyższa sytuacja jest bezpośrednio wynikiem tego, co mówiłem na temat zwracania **dokumentów** (obiekt text + metadata) jako rezultat działania narzędzi. W tym przypadku "obsługa błędu" polegała na tym, aby poinformować agenta o jego wystąpieniu. 

Nie oznacza to jednak, że sama obsługa błędów rozwiązuje nam wszystkie problemy i każdy użytkownik będzie w stanie pracować z takim agentem jak Alice. Powodem jest fakt, że część poleceń musi być wydana bardzo precyzyjnie i tym samym wspierać rozumowanie agenta. Przykładowo prośba o wejście na wybrane strony i przygotowanie podsumowania, w moim przypadku wygląda tak:

- Wczytaj treść stron `*tutaj adresy*`, następnie utwórz dokument zawierający `*tutaj opis oczekiwanej treści*`, wgraj je na serwer i prześlij mi mailem

Widać tutaj, jak moje polecenie **prowadzi agenta** przez pewien schemat uwzględniający serię kroków potrzebnych do wykonania zadania. Natomiast typowy użytkownik powiedziałby raczej:

- Pobierz `*ogólny opis oczekiwanej treści*` ze stron `*lista adresów*` i prześlij mi mailem

Takie zapytanie jest mniej precyzyjne i w zależności od sytuacji, może negatywnie wpłynąć na skuteczność działania agenta. Co gorsza, nawet jeśli zaadresujemy ten konkretny przypadek, to i tak nie jesteśmy w stanie przewidzieć wszystkich możliwych zapytań.

No ale skoro tak, to **w jaki sposób sprawić, by z agenta mogli korzystać inni?** 

Opcji jest przynajmniej kilka:

- Agent może być ograniczony interfejsem, który nie pozwala na zbyt dużą interakcję ze strony użytkownika. Przykładem takiego agenta jest Perplexity. W zależności od zapytania podejmowane są różne kroki mające na celu zwiększenie precyzji i dostarczenie wysokiej jakości rezultatu. Użytkownik nie ma większego wpływu na ten proces, ani możliwości zapytania o wykonanie akcji niezwiązanej z wyszukiwaniem, ponieważ ogranicza go interfejs.

![](https://cloud.overment.com/2024-11-29/aidevs3_vercel-ab286591-a.png)

- Sam interfejs może jeszcze bardziej ograniczać swobodę użytkownika (jakkolwiek to brzmi), ale nadal wykonywać dla niego wartościową pracę. Oto przykład z jednej z wcześniejszych lekcji: automatyzacja podłączona do mojej skrzynki e-mail i wiadomości z określoną etykietą. Na podstawie informacji z maila tworzona jest wiadomość do agenta, który w tym przypadku dodaje nowe zadanie w Linear. Wciąż mówimy tutaj o wartości dla użytkownika, a znaczenie ograniczamy problem nieprecyzyjnych komunikatów. 

![](https://cloud.overment.com/2024-11-29/aidevs3_mail-822ee985-1.png)

- Z drugiej strony, możliwe są sytuacje w których nie będziemy chcieli ograniczać interakcji z użytkownikiem. Wówczas koniecznie musimy zadbać o zachowanie dobrych praktyk aplikacji produkcyjnych, o których mówiliśmy w pierwszej części AI_devs. Dodatkowo konieczny staje się tutaj także **onboarding** wyjaśniający użytkownikom, w jaki sposób mogą pracować z agentem oraz jakie oczekiwania mogą mieć wobec naszego systemu. Przykładem może być tutaj moja aplikacja heyalice.app, która pozwala na **dopasowanie jej ustawień** do swoich własnych preferencji. Oczywiście stwarza to ogromną barierę wejścia dla nowych użytkowników, ale też daje mnóstwo swobody tym, którzy przejdą przez etap konfiguracji. 

![](https://cloud.overment.com/2024-11-29/aidevs3_alice-826f6b70-7.png)

Mówiłem już, że według mnie obecnie ci najbardziej rozbudowani agenci powinni działać "w tle". Natomiast ci, którzy mają kontakt z użytkownikiem, powinni być maksymalnie ograniczeni już na etapie założeń projektu. Oczywiście, można się tutaj ze mną nie zgodzić, tym bardziej że rozwój narzędzi oraz samych modeli wcześniej czy później może sprawić, że takie nastawienie przestanie być aktualne.

Idąc dalej, bardziej zaawansowana logika agenta uniemożliwi prowadzenie interakcji w czasie rzeczywistym lub z niskim czasem reakcji. Rzecz w tym, że nie wszystkie interakcje z agentem będą wymagały wykonywania zaawansowanego "rozumowania", więc możemy wykorzystać koncepcję "routera" z której sam zacząłem korzystać od niedawna. 

Polega ona na prostej klasyfikacji zapytania w celu określenia tego, czy potrzebne są jakieś narzędzia i obszary pamięci, czy też nie. Jeśli router zdecyduje, że nie ma takiej potrzeby, to po prostu generujemy odpowiedź. 

![](https://cloud.overment.com/2024-11-29/aidevs3_fasttrack-210c5ead-c.png)

Co prawda jest w tym pewien haczyk, ponieważ niekiedy granica pomiędzy koniecznością skorzystania z narzędzia, a bezpośrednią odpowiedzią jest bardzo cienka, nawet dla człowieka. Warto więc zachować tutaj ostrożność, bądź po prostu pamiętać o tym, aby podkreślać konieczność skorzystania z narzędzi bądź "zastanowienie się".

W temacie oczekiwania na odpowiedź, w lekcji S00E03 wspominałem także o praktycznym strumieniowaniu akcji agenta i w tym temacie chciałem dodać jedną z ostatnich aktualizacji Vercel AI SDK, która ułatwia ten proces. Dzięki temu serwer może poinformować użytkownika o podejmowanej akcji, bez potrzeby oczekiwania na całkowite zakończenie zapytania. 

![](https://cloud.overment.com/2024-11-29/aidevs3_nonblocking-55ed0ba6-f.png)

Także podsumowując temat interakcji agenta z człowiekiem — **uniwersalne systemy, zdolne do w pełni autonomicznego działania, są jeszcze poza naszym zasięgiem**. Powinniśmy się zatem skupić na **wyspecjalizowaniu agentów** w wybranym obszarze, oraz narzucić ograniczenia po stronie logiki oraz interfejsu tak, aby przestrzeń na popełnienie błędu lub niepożądaną interakcję, była jak najmniejsza. 
## Współpraca z innymi agentami

Choć w sieci można znaleźć wiele informacji na temat budowy zespołów agentów zdolnych do rozwiązywania bardzo złożonych problemów, moje doświadczenie sugeruje, że warto najpierw skupić się na umiejętności stworzenia **jednego agenta**, który dobrze wykona swoją pracę. Wówczas połączenie go z innymi agentami, staje się znacznie prostsze, ale też niekiedy w ogóle niepotrzebne. 

W AI_devs 3 niebezpośrednio omawialiśmy rozwiązania, które równie dobrze można porównać do systemów zbudowanych z wielu agentów, ponieważ:

- Narzędzia podłączane do modelu, miały formę **niezależnych modułów** i zachowywały spójny interfejs. Natomiast ich logika nierzadko uwzględniała kompleksową interakcję z LLM, a także momentami z sobą nawzajem. Oznacza to, że chociażby przykład `websearch` mógłby być rozwinięty do pełnej logiki agenta i wówczas nasz główny agent, kontaktowałby się z nim w sprawie przeszukania Internetu.
- W naszym przypadku za **planowanie zadań oraz akcji** również odbywa się poprzez kilka zapytań do modelu, ale w razie potrzeby moglibyśmy rozwinąć ten etap do formy pełnoprawnego agenta.
- Narzędzia mają dostęp do **wspólnego stanu** oraz **stanu lokalnego**, dzięki czemu mogą wymieniać pomiędzy sobą informacje, dokładnie jak w przypadku wielu agentów. 

Zatem cały czas spełniamy główne założenia dotyczące **niezależności** oraz **spójnego formatu wymiany danych**, a dany moduł możemy rozwinąć dopiero wtedy, gdy pojawi się taka potrzeba. Wówczas kolejny agent, staje się jedynie kolejnym narzędziem, który może zostać wywołany w razie potrzeby.

Z drugiej strony, agenci mogą mieć także znacznie prostszą strukturę niż to, co budowaliśmy w AI_devs. Dobrym przykładem jest wspomniany [Ditto](https://github.com/yoheinakajima/ditto), który wykorzystuje tylko jeden prompt i zestaw kilku prostych narzędzi uruchamianych z pomocą Function Calling. Poniższy prompt jest bardzo prosty w porównaniu do tych, które omawialiśmy. Pomimo tego, Ditto jest w stanie budować proste aplikacje w ramach jednego wątku. 

![](https://cloud.overment.com/2024-11-29/aidevs3_ditto-b8316e2e-1.png)

Zarówno w przypadku Ditto, jak i kontekstu naszych lekcji, ciągle mówimy o jednym agencie zdolnym do wykonywania mniej lub bardziej złożonych zadań. Natomiast prędzej czy później będziemy chcieli pójść krok dalej i znajdziemy realny powód do zbudowania oraz połączenia wielu agentów. Obecnie jednak jest to temat eksploracji i trudno jednoznacznie wskazać sprawdzone techniki pracy oraz wzorce. 

Pojawiają się jednak publikacje takie jak [Scaling Large-Language-Model-based Multi-Agent Collaboration](https://arxiv.org/pdf/2406.07155), które przedstawiają propozycje związane z architekturą takich systemów. Mowa więc tutaj o łączeniu agentów w łańcuch, struktury drzewiaste czy różne rodzaje grafów. 

![](https://cloud.overment.com/2024-11-29/aidevs3_topologies-b1c9046c-7.png)

Patrzenie na agentów w ten sposób, otwiera wprost absurdalne możliwości, czego przykładem jest [Projekt Sid](https://github.com/altera-al/project-sid) zakładający stworzenie cywilizacji agentów. Oczywiście na ten moment warto zachować spory dystans wobec tego projektu, ale kierunek, który rysuje, może zainspirować do nieszablonowych rozwiązań naszych problemów. 

![](https://cloud.overment.com/2024-11-29/aidevs3_altera-f84185dc-a.png)

Znacznie bardziej przyziemnym przykładem, jest wpis [Orchestrating Agents: Routines and Handoffs](https://cookbook.openai.com/examples/orchestrating_agents) udostępniony przez OpenAI. Pokazuje on przykład implementacji zespołu agentów odpowiadających za obsługę klienta. Tutaj różnica względem tego, czego się uczyliśmy, jest znacznie mniejsza i już teraz stworzenie takiego systemu nie powinno stanowić większego problemu (aczkolwiek wszystko rozbija się o szczegóły). 

![](https://cloud.overment.com/2024-11-29/aidevs3_code-e98eebe7-e.png)

Wnioski z tych przykładów są następujące: 

- Tam, gdzie nie jest to potrzebne, logika agencyjna, silnie opierająca się o działanie modelu, powinna zostać pominięta. Zastosowanie zwykłego "łańcucha" zapytań do LLM nierzadko będzie w pełni wystarczające w przypadku prostych zadań. 
- Jeden agent może być wyposażony w wiele narzędzi oraz z powodzeniem się nimi posługiwać, dopasowując przy tym plan swoich działań do zmieniających się warunków. Ma to jednak swoje granice. W pewnym momencie narzędzia mogą zacząć się ze sobą pokrywać (ale różnić detalami) i system nie będzie działać poprawnie.
- Wówczas możemy stworzyć zespół agentów i decydować o tym, kiedy ich aktywować. W ten sposób zyskujemy możliwość dalszego skalowania systemu i zwiększamy jego zdolność do rozwiązywania skomplikowanych zadań.
## API agenta

Część przykładów przez które przeszliśmy, pozwalała na interakcję poprzez endpoint `/api/chat` na który zwykle mogliśmy przesłać zapytanie zapisane językiem naturalnym, a model decydował, co z nim należy zrobić. No i dokładnie w ten sposób będzie to wyglądało w przypadku agenta bądź zespołu agentów. Sam określam to mianem "single-entry point". Taki endpoint daje nam ogromną elastyczność, ale nie będziemy potrzebować jej w każdej sytuacji.

Załóżmy, że nasz agent posiada informacje na temat otoczenia: lokalizacji, pogody i kilku innych danych, potencjalnie przydatnych do wykonywania swoich zadań. 

Dane te charakteryzuje fakt, że zmieniają się w czasie, a w dodatku ich pobranie w czasie rzeczywistym nie zawsze będzie uzasadnione. Przykładowo w moim przypadku informacja o tym, czy znajduję się w samochodzie aktualizowana jest w chwili gdy mój telefon łączy się z nim przez bluetooth. Sama aktualizacja wpisu nie wymaga zaangażowania logiki agenta, więc mogę wykonać bezpośrednie zapytanie na adres `/api/users/:id`.

Podobnie jest z dostępem do narzędzi. Mój agent posiada możliwość wgrywania plików na serwer. Ale nierzadko sam chcę to zrobić lub skorzystać z tej możliwości z poziomu automatyzacji. Wówczas ponownie wystarczy mi proste zapytanie na adres `/api/files`. Zatem struktura API może wyglądać następująco: 

![](https://cloud.overment.com/2024-12-01/aidevs3_api-06960ff9-e.png)

Koncepcja samego API, nie jest czymś nowym w kontekście aplikacji. Zwykle wykorzystujemy je po to, aby różne interfejsy (np. aplikacja mobilna, webowa i desktopowa) mogła komunikować się z tym samym serwerem. Podobnie jest z agentem, tylko tutaj mówimy o zewnętrznych usługach, które będą dostarczać informacje do agenta bez angażowania jego głównej logiki. No i do gry wchodzi także ten "główny endpoint" zdolny do przetwarzania zapytań w języku naturalnym. 

Ostatecznie struktura API będzie uzależniona od aplikacji i sposobu interakcji z nią. Natomiast bez wątpienia musimy mieć na uwadze zmienną w postaci **obecności LLM**, który wpływa na architekturę właśnie ze względu na fakt, że jednym z użytkowników API, mogą być także inni agenci. 
## Połączenie z różnymi interfejsami

We wpisie "[Jak pracuję z AI](https://bravecourses.circle.so/c/dyskusje-ai3/jak-pracuje-z-ai-material-bonusowy)" mowię o zastosowaniu **wspólnego back-endu** dla kilku interfejsów w postaci aplikacji oraz urządzeń. Pomimo tego, że logika działająca na serwerze pozostaje taka sama, to jest tam kilka rzeczy, na które warto zwrócić uwagę.

Przede wszystkim, wiadomości są powiązane z konwersacją poprzez identyfikator. Z kolei konwersacje, są powiązane z użytkownikiem. Tutaj z programistycznego punktu widzenia, odbywa się to dokładnie tak, jak w klasycznych aplikacjach. 

![](https://cloud.overment.com/2024-12-01/aidevs3_uuid-33f92540-2.png)

Taka organizacja danych umożliwia połączenie z różnymi interfejsami, które mogą przesłać jedynie **najnowszą wiadomość użytkownika** oraz **identyfikator konwersacji**. Przykładem jest moje makro Shortcuts uruchamiane na telefonie czy zegarku, w którym **przed wysłaniem zapytania** odpytuję serwer o **identyfikator ostatniej rozmowy**, która odbyła się w ciągu ostatnich 15 minut. Dzięki temu, pomimo tego, że w danej chwili przesyłam tylko bieżącą wiadomość, to i tak rozmowa odbywa się w ramach danego wątku. 

![](https://cloud.overment.com/2024-12-01/aidevs3_shortcut-434ac067-1.png)

Jest jednak pewna zmienna, która odróżnia, czy komunikuję się z back-endem z poziomu zegarka (interfejs audio), czy aplikacji desktopowej (interfejs czatu). Konkretnie, poza listą wiadomości, przesyłam dodatkową właściwość określającą **rodzaj interfejsu**. Informacja ta wykorzystywana jest w **prompcie odpowiedzialnym za wygenerowanie ostatecznej odpowiedzi** i dopasowanie jej do danego formatu. Na przykład, wiadomość wyświetlona w oknie czatu będzie wyglądać inaczej niż w przypadku formy audio.

![](https://cloud.overment.com/2024-12-01/aidevs3_source-2f48137b-7.png)

W niektórych sytuacjach możemy także podjąć decyzję o tym, aby identyfikator konwersacji pochodził z zewnętrznej aplikacji. Przykładem jest tutaj Slack, w którym mamy dostępne **wątki**. Co więcej, składania formatowania wiadomości w przypadku Slacka również jest dość charakterystyczna i skorzystanie tutaj z właściwości **source** również ma sens. 

![](https://cloud.overment.com/2024-12-01/aidevs3_dm-83826d6f-1.png)

Ostatecznie sami musimy zdecydować o tym, jaki interfejs będzie najlepszy dla naszego agenta / agentów. Warto jednak rozważyć skorzystanie z istniejących już rozwiązań, zamiast budować coś od podstaw (o ile z jakiegoś powodu nie jest to dla nas ważne). Ewentualnie możemy zdecydować, że nasz agent w ogóle nie będzie posiadał interfejsu dostępnego dla użytkownika i to również jest jedną z opcji. 
## Agenci działający w czasie rzeczywistym

Możliwość uzyskania natychmiastowej odpowiedzi od agenta AI stanowi oczekiwanie ze strony wielu osób oraz klientów. Praktyka pokazuje jednak, że agent zwykle będzie potrzebował więcej czasu na odpowiedź i nierzadko jedyną formą optymalizacji, będzie strumieniowanie informacji o postępach jego pracy.

Nie oznacza to jednak, że logika w której pojawia się LLM oraz narzędzia musi zawsze eliminować interakcji w czasie rzeczywistym. Pokazuje to przykład `live`, który różni się od przykładu `tool_use` jedynie tym, że przełączyłem model z GPT-4o na Llama 3 z platformy [Groq](https://groq.com). Dzięki temu czas reakcji wynosi "jedynie" 856 sekund, ALE w tym przypadku brakuje faktycznego uruchomienia narzędzia. Można więc powiedzieć, że czas odpowiedzi wydłuży się do 1 sekundy, ale to i tak drastyczna zmiana w porównaniu do pracy z OpenAI. 

Jednocześnie trzeba pamiętać o tym, że na dzień pisania tych słów, platformy takie jak Groq czy Rysana wciąż nie oferują sensownych planów cenowych przy których limity API pozwolą na praktyczne zastosowanie ich usługi (według twórców możliwe jest jednak przejście na plan biznesowy, ale nie mam informacji o warunkach i minimalnej kwocie).

![](https://cloud.overment.com/2024-12-01/aidevs3_live-2bf46a47-4.png)

Jeśli jednak będziemy chcieli pozostać przy OpenAI/Anthropic i wykorzystać ich modele do budowy takiego interfejsu, to:

- Rola LLM powinna zostać ograniczona do niezbędnego minimum
- Tam gdzie to możliwe, musimy zoptymalizować prompty tak, aby mogły działać z modelami GPT-4o-mini bądź Claude 3.5 Haiku
- W sytuacji, gdy konieczne jest przetwarzanie audio, możemy pominąć krok transkrypcji i generowania audio za pomocą zewnętrznych usług, korzystając z najnowszych możliwości modeli OpenAI, które obsługują audio zarówno na wejściu, jak i na wyjściu
- Powinniśmy wykorzystać strumieniowanie wszędzie tam, gdzie jest to możliwe, wliczając w to także strumieniowanie dźwięku

Natomiast i tak mówimy tutaj o scenariuszach wykorzystujących stosunkowo proste interakcje z narzędziami. **Wszędzie tam, gdzie wymagana będzie bardziej złożona logika, możemy na ten moment odłożyć interakcję w czasie rzeczywistym na bok**. 
## Agenci jako narzędzia

Cały czas patrzyliśmy na agentów jako systemy zdolne do posługiwania się narzędziami. Natomiast sam agent, również może być jednym z takich narzędzi, lub nawet odpowiadać za **tylko jeden etap logiki**.

Przykładowo [Weaviate](https://weaviate.io/blog/what-is-agentic-rag) opisuje na swoim blogu przykład tzw. "Agentic RAG", czyli jak nazwa wskazuje — agenta odpowiadającego za wczytywanie treści do kontekstu LLM. 

![](https://cloud.overment.com/2024-12-01/aidevs3_agenticrag-7208069a-1.png)

Dokładnie tak samo możemy patrzeć na agentów w kontekście innych narzędzi, np. przeglądania Internetu czy scrapowania treści stron www. 

![](https://cloud.overment.com/2024-12-01/aidevs3_scrapper-304da124-d.png)

Zasadniczo, wszędzie tam, gdzie pojawia się problem wymagający dynamicznego dostosowania się do aktualnej sytuacji, warto rozważyć stworzenie agenta, który go rozwiąże. Później inni agenci bedą mogli jedynie zwracać się do agenta specjalizującego się w danym zadaniu, przesyłając do niego zapytania zapisane w języku naturalnym. 

Sama budowa takiego agenta, nie różni w porównaniu do tego, co do tej pory omówiliśmy i na czym skupimy się jutro. Po prostu zakres jego działania będzie znacznie mniejszy. 
## Agent zdobywający wiedzę

Podczas gdy w sieci można spotkać mnóstwo pytań o sposoby połączenia agenta z własną wiedzą, tak niemal nikt nie pyta o to, w jaki sposób agent może zdobywać wiedzę. Co więcej, wiele wskazuje na to, że takie podejście jest znacznie bardziej skuteczne od próby połączenia LLM z dokumentami, które powstały z myślą o człowieku.

Przekonaliśmy się już wielokrotnie o tym, jak trudno jest przetworzyć niektóre formaty dokumentów. Zresztą nawet jeśli nam się to uda, wciąż istnieje duże ryzyko utracenia kontekstu na etapie wyszukiwania oraz wczytania treści do promptu systemowego.

Sytuacja zmienia się jednak, gdy pamięć agenta przestaje mieć formę treści wczytanej z zewnętrznych źródeł i w zamian może on budować ją według swoich własnych zasad. Tutaj przykładem który zrobił na mnie największe wrażenie, jest repozytorium [AGI Memory System](https://github.com/cognitivecomputations/agi_memory), które opisuje strukturę tabel oraz sposób interakcji z nimi, w kontekście dynamicznie budowanej pamięci. Całość obejmuje praktycznie wszystko, czego uczyliśmy się do tej pory i porządkuje zagadnienia związane z wyszukiwaniem full-text, wyszukiwaniem znaczeniowym czy pracą z grafami. W tym jednak przypadku całość opiera się w pełni o PostgreSQL w której przechowujemy zarówno embedding, jak i uproszczoną strukturę powiązań pomiędzy wspomnieniami. 

![](https://cloud.overment.com/2024-12-02/aidevs3_agi-4f6f7799-a.png)

Różnica pomiędzy pamięcią budowaną poprzez wczytywanie treści dokumentów, a budowanie wspomnień na ich podstawie jest fundamentalna. Główną różnicą jest tutaj fakt, że w tym drugim przypadku agent **samodzielnie ustala sposób organizacji informacji**, co pozwala na zachowanie spójności nawet w sytuacji, gdy dane pochodzą z różnych źródeł. Taka spójność pozwala na znacznie bardziej skuteczne przeszukiwanie oraz dalszą rozbudowę.

Moje doświadczenie sugeruje jednak, że w pełni dynamiczne budowanie systemu wspomnień jest jeszcze poza naszym (lub moim) zasięgiem i ma to związek albo z możliwościami samych modeli, ekosystemu narzędzi bądź technik pracy z nimi. Warto więc jak zwykle narzucić ograniczenia, chociażby w zakresie **drzewa kategorii** **chmury tagów** w ramach których model może organizować informacje. Przykład takiej początkowej struktury mamy poniżej. 

![](https://cloud.overment.com/2024-12-02/aidevs3_memories-44e6ae9c-b.png)

No i teraz wykorzystując to, co wiemy na temat silników wyszukiwania oraz baz wektorowych, sugeruje, że:

- zapisywanie nowej informacji będzie wymagało wydobycia z niej istotnych danych, nierzadko dzieląc ją na mniejsze dokumenty. Następnie dane te będą klasyfikowane i przyporządkowywane do konkretnych kategorii. Ostatecznie każdy dokument będzie też odpowiednio opisany, aby umożliwić filtrowanie na etapie wyszukiwania
- odczytywanie informacji będzie polegało na wygenerowaniu zapytań względem powyższej struktury, a następnie przeprowadzenia wyszukiwania, które pozwoli zebrać wszystkie wymagane wspomnienia.

Wyzwanie w tym przypadku polega jednak na tym, aby unikać sytuacji w której jakaś informacja zostaje zapisana w kategorii "A", a później próbujemy ją odnaleźć w kategorii "B". Możemy więc wykonać dwa rodzaje wyszukiwania — wąskie (zawężone do kategorii) oraz szerokie (skanujące całą dostępną bazę wiedzy). Wówczas ryzyko wystąpienia wspomnianego błędu, będzie niższe, ale rekordy z szerokiego wyszukiwania będą musiały być odfiltrowane przez sam model (tutaj do gry wchodzi re-rank realizowany przez LLM).

## Podsumowanie

Podczas AI_devs przeszliśmy przez dziesiątki przykładów narzędzi i dowiedzieliśmy się w jaki sposób tworzyć je z myślą o agentach AI. W końcu poznaliśmy także fundamenty pozwalające na zbudowanie logiki w której LLM niemal samodzielnie posługuje się tymi narzędziami. 

Takie systemy są zdolne do realizowania zadań, których sposób wykonania nie musi być z góry ustalony. Pomimo tego, **nie jesteśmy jeszcze w miejscu w którym możliwe jest budowanie w pełni autonomicznych systemów zdolnych do wykonywania całych procesów.** 

Natomiast dziś już nic nie stoi na przeszkodzie, aby budować systemy zdolne do poruszania się po ograniczonym obszarze, z szeregiem limitów narzuconych przez nas. Co więcej, systemy te powoli zaczynają ze sobą współpracować i tym samym ich możliwości rosną z każdym miesiącem.

Na tym etapie kluczowe jest więc zdobycie praktycznych umiejętności związanych z wyspecjalizowanych agentów oraz wdrażaniem ich na potrzeby prywatne bądź wewnątrzfirmowe. W międzyczasie wiele wskazuje na to, że dalej będą rozwijać się biblioteki, frameworki oraz techniki pracy, które pomogą tworzyć coraz bardziej złożone systemy, które być może na pewnym etapie będą w stanie rozwijać się samodzielnie. 

Dziś jednak, nadal wszystko leży w naszych rękach.