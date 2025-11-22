![...](https://cloud.overment.com/2024-12-02/s05e02-5ceadb39-0.png)

Zdolność do zrozumienia bieżącej sytuacji, zidentyfikowania problemu i opracowania planu jego rozwiązania umożliwia podejmowanie złożonych działań oraz dążenie do ustalonego celu, mimo zmieniających się warunków. Jest to też fundamentalna umiejętność agenta, od której zależy cała reszta i to właśnie na niej skupimy się w tej lekcji.

**Refleksja** oraz **planowanie** o których mówiliśmy w poprzedniej lekcji to aktywności, które stanowią elementy tego, czym dziś będziemy się zajmować. Jednak tym razem, spojrzymy na temat z nieco szerszej perspektywy.

Zarówno ogólne komponenty, jak i szczegóły implementacji będą nieco różnić się w zależności od tego, jaki system będziemy budować. Dlatego dla nadania kontekstu, zarysujmy ogólny kształt naszego agenta. 

Załóżmy, że będzie to zaawansowany asystent, przypominający tych, które budowaliśmy we wcześniejszych edycjach AI_devs (czyli osobistego asystenta), ale ten będzie miał znacznie większą swobodę działania. Mamy zatem:

- **Zdolność do prowadzenia rozmowy**, ale tym razem obejmującej także różne "zmysły" (obraz / audio) oraz obsługę dokumentów i plików. 
- **Umiejętność posługiwania się narzędziami**, ale tym razem zdolność ta ma charakter otwarty i agent samodzielnie może zdecydować, z których narzędzi skorzystać. Wśród narzędzi będzie: **pamięć**, **internet**, **system plików**, **lista zadań**, **spotify** oraz inne, powiązane z możliwością wspierania nas w codziennej pracy.
- **Możliwość zapamiętywania informacji**, ale tym razem będzie to prosta tablica "wspomnień". 

Są to więc główne komponenty agenta, które widzieliśmy już w poprzedniej lekcji. Teraz możemy spojrzeć na nie przez kilka scenariuszy:

- **Przypomnienie:** Użytkownik pyta o przypomnienie wcześniej zapamiętanej informacji, np. linku do filmu.
- **Akcję:** Użytkownik wydaje polecenie wymagające wiedzy na temat jego preferencji.
- **Zlecenie:** Użytkownik przesyła plik z prośbą o sprawdzenie jego poprawności, na podstawie danych z Internetu, a następnie przesłanie efektów na e-mail.
- **Myśl:** Agent przesyła wiadomość do samego siebie w wyniku działania harmonogramu zadań, np. "miałem przypomnieć użytkownikowi o ...".

Wszystkie z tych zadań, choć różnią się sposobem realizacji, posiadają elementy wspólne. Zobaczmy więc, jak mógłby wyglądać taki agent, skupiając się na jednym z wymienionych scenariuszy. 
## Przegląd mechaniki agenta

W przykładzie `assistant` znajduje się logika podobna do tej, którą omawialiśmy w lekcji S05E01 — Agent AI, jednak ta jest nieco bardziej złożona. Z tego powodu uprościłem większość mechaniki (narzędzia, pamięć), dzięki czemu możemy skupić się wyłącznie na części związanej z LLM.

Główna mechanika prezentuje się następująco: 

![](https://cloud.overment.com/2024-10-29/aidevs3_assistant_schema-0535f470-4.png)

Uwzględnia ona następujące etapy: 

- **Etap początkowej refleksji** / rozpoznania w której agent dąży do zorientowania się w aktualnej sytuacji.
- **Etap planowania** w którym powstaje **lista zadań** koniecznych do wykonania, przed udzieleniem odpowiedzi użytkownikowi. Lista ta może być aktualizowana, 
- Jeszcze na etapie planowania, ustalana jest decyzja o **akcji**, która ma zostać podjęta w ramach **bieżącego zadania**.
- **Etap wykonania** w którym generowane są dane potrzebne do uruchomienia akcji czy też skorzystania z przypisanego do niego narzędzia
- Etap wykonania uwzględnia także faktyczne uruchomienie funkcji oraz dodanie jej rezultatu do kontekstu.

Zatem różnice w porównaniu do przykładu `agent` są następujące: 

- Początkowy etap refleksji pozwala na zainicjowanie głównej mechaniki, dostarczając do niej informacje, których nie podał użytkownik. Tutaj prompty mają charakter "mowy wewnętrznej" w przypadku której model jest poinformowany o tym, że użytkownik nie widzi jego wypowiedzi. 
- Etap planowania obejmuje podział na **zadania** oraz **akcje** w ich ramach. Różnica jest istotna, ponieważ zadanie (np. wczytanie i transformacja dokumentu) może zakończyć się niepowodzeniem podczas realizacji. Dzięki hierarchii `task > action`, możemy łatwo sprawdzić, która z akcji zawiodła i w razie potrzeby ją wznowić, bez konieczności powtarzania wszystkich wcześniejszych etapów.
- Etap wykonania uwzględnia oddzielny krok skupiający się **wyłącznie na wygenerowaniu obiektu żądania** potrzebnego do uruchomienia narzędzia / podjęcia akcji. Tutaj uwaga modelu skupia się wyłącznie na tej jednej rzeczy. 

Taka konfiguracja agenta znacznie przekłada się przede wszystkim na większą elastyczność, oraz skuteczność ze względu na wyższej jakości kontekst oraz możliwość zmiany planu w trakcie jego realizacji. 
## Przykład

Przykład `assistant` ma na celu zaprezentowanie głównych mechanik i gdybyśmy chcieli zastosować go w połączeniu z różnymi narzędziami, to prawdopodobnie konieczne będzie wprowadzenie zmian w samych promptach. Natomiast ogólna logika, obejmuje wszystkie najważniejsze elementy, które będą występować u większości agentów.

Uruchom więc ten przykład dla ustawionego przeze mnie zapytania. Spróbuj zmodyfikować wartości / informacje zawarte w kontekście oraz także listę narzędzi i sprawdź jak zachowuje się agent. Zwróć uwagę na zmiany, które są potrzebne oraz fakt, że agent może mieć trudności w odnalezieniu się w każdej sytuacji. 

Oczekiwane zachowanie polega więc na tym, aby na prośbę użytkownika o włączenie ulubionej muzyki, agent musi "przypomnieć sobie" o jaką muzykę chodzi i wykorzystać tę wiedzę w dalszych krokach. 

Poniżej znajduje się log z poprawnej realizacji zadania, wykonanego w czterech fazach (łącznie z początkową). Cała widoczna ścieżka nie została przez nas zakodowana, lecz jest wynikiem działania modelu językowego połączonego z logiką zapisaną w kodzie.

![](https://cloud.overment.com/2024-10-30/aidevs3_example-357e853f-1.png)

## Persona

Zaczynając od pierwszego etapu "refleksji", pojawia się w nim wątek **środowiska**, **osobowości / ogólnego kontekstu**, a także zadania sobie kilku pytań. 

Etap ten jest ważny, ponieważ nawet jeśli agent jest podłączony do bazy danych i może wczytać informacje na nasz temat, to i tak w chwili rozpoczęcia interakcji, nie ma do niej dostępu i musi "jakoś" dotrzeć do wiedzy wymaganej do dalszego działania. 

Po lekcjach dotyczących wyszukiwania wiemy, że możemy wzbogacać zapytanie użytkownika poprzez prompty w których model zadaje sobie pytania pomagające mu w eksploracji pamięci i wczytaniu właściwych wspomnień.

Przykładowo, gdy zapytam: **Jaka jest teraz pogoda?**

Agent może zadać pytanie pomocnicze: **Gdzie aktualnie znajduje się użytkownik?**

W ten sposób agent dociera do potrzebnych informacji i może je wykorzystać w połączeniu z narzędziami / umiejętnościami, które posiada. 

Nie zawsze jednak zadanie takich pytań będzie takie oczywiste i może prowadzić do generowania zapytań, które nie będą miały sensu lub co gorsza, doprowadzą do danych niemających znaczenia w danym kontekście. 

Przykład: **Wyjaśnij mi, jak działa streaming?**

"Streaming" to zagadnienie, które posiada wiele znaczeń i sposób zadawania pytań na ten temat, będzie różnić się w zależności od kontekstu i czym innym będzie dla programisty, a czym innym dla twórcy Internetowego. A skoro agent go początkowo nie posiada, to ryzyko wygenerowania błędnych zapytań jest wysokie.

Z tego powodu warto utworzyć tzw. "ogólny kontekst" lub wspomnianą "personę" agenta, w której będą zapisane najważniejsze informacje na jego temat, które nie zmieniają się w czasie zbyt często. To samo może dotyczyć wiedzy na temat użytkownika, lub informacji pochodzących z otoczenia. Początkowo można pomyśleć, że ogólny kontekst powinien być dostępny w całości, jednak treść obszernej notatki może niepotrzebnie rozpraszać model. Warto więc coś z tym zrobić. 

W przykładzie `assistant` rozpoczęcie interakcji uwzględnia etap o nazwie `thinking`, którego celem jest: 

- Kompresja informacji dotyczących otoczenia oraz wiedzy o sobie i użytkowniku. Inaczej mówiąc, agent pobiera z "ogólnego kontekstu" tylko te informacje, które uznaje za pomocne. Dzięki temu nie mamy potrzeby wczytywać ich wszystkich w dalszych krokach.
- Zadanie sobie kilku początkowych pytań na temat **obszarów pamięci**, które mogą być przydatne do przeskanowania oraz **wskazania potencjalnych narzędzi/umiejętności**

![](https://cloud.overment.com/2024-10-29/aidevs_context-5718c022-5.png)

Inaczej mówiąc — **agent próbuje zorientować się w danej sytuacji** i postawić wstępne założenia. Założenia te nie są jednak ostateczne i będą stanowić jedynie wskazówkę w dalszych krokach.

Takie podejście nawiązuje także do "czasu na myślenie" dla modelu, o którym wielokrotnie mówiliśmy. Poniżej widzimy przykład dla prośby o "włączenie ulubionej muzyki". Widzimy, że agent zauważył muzykę, która aktualnie jest uruchomiona, i nawet założył, że prawdopodobnie może to być jedna z moich ulubionych. Dodatkowo z ogólnego kontekstu / osobowości wczytał ogólną informację o tym, że "kocham klasycznego rocka". 

![](https://cloud.overment.com/2024-10-29/aidevs3_thoughts-3607f1f5-7.png)

Mamy więc wstępne wskazówki pozwalające na kontynuowanie odpowiedzi, ale jednocześnie nie mamy wszystkich potrzebnych detali potrzebnych do wykonania akcji i udzielenia odpowiedzi. 
## Wstępne rozpoznanie

Poza wypisaniem istotnych fragmentów na temat otoczenia i ogólnego kontekstu, agent zadaje sobie także serię pytań dotyczących **narzędzi** oraz **pamięci**. Jednak zapytania te nie są wykonywane **równolegle** do wcześniejszych, ponieważ ich rezultaty są wykorzystywane do lepszego formułowania pytań.

Jest to ważna kwestia, ponieważ zawsze musimy brać pod uwagę to, **jakich informacji na danym etapie potrzebuje model** w danej chwili.

Poniżej widzimy, że zapytania z kategorii "Memory" oraz "Tools" nie są już ogólne, lecz dotyczą (w tym przypadku) klasycznego rocka. To ponownie umożliwia lepsze przeszukanie pamięci. 

![](https://cloud.overment.com/2024-10-29/aidevs3_selfqueries-68f98888-9.png)

Celem powyższych zapytań jest **ukierunkowanie uwagi modelu** na konkretny kierunek i wygenerowanie jakościowej treści, która zostanie dołączona jako kontekst do dalszych zapytań. 

Także patrząc na to z szerszej perspektywy, podejmujemy kroki, które wykorzystują możliwości modeli językowych po to, aby uzupełnić oryginalne zapytanie użytkownika o możliwie dużo szczegółów. 

Najważniejszym wyzwaniem tego etapu jest sprawienie by model **nie angażował się w odpowiedź użytkownikowi**, lecz skupił wyłącznie na wygenerowaniu "przemyśleń". Nacisk na takie zachowanie kładziemy bezpośrednio w prompcie systemowym. 

![](https://cloud.overment.com/2024-10-29/aidevs3_internal_dialogue-501789e1-9.png)

## Aktualny stan agenta

W przykładzie `assistant`, stan agenta również jest bardziej rozbudowany, niż w przykładzie z poprzedniej lekcji. Uwzględnia: 

- Ustawienia: liczbę dostępnych kroków i aktualne zadanie oraz akcję.
- Ogólny kontekst / dane środowiskowe, które mogą być wczytywane z profilu użytkownika
- Listę umiejętności / narzędzi wraz z instrukcją ich obsługi
- Listę "przemyśleń", o których przed chwilą mówiliśmy
- Listę wczytanych dokumentów oraz przywołanych wspomnień
- Listę wiadomości z bieżącej konwersacji. 

![](https://cloud.overment.com/2024-10-29/aidevs3_state-a54dc561-9.png)

Struktura stanu będzie różnić się w zależności od agenta, ale jej głównym założeniem jest przechowywanie wszystkich informacji związanych z jego działaniem, w kontekście bieżącej konwersacji. Dane przechowywane w stanie będą dostępne praktycznie na każdym etapie logiki agenta i poszczególne wartości będą dodawane jako kontekst promptów.

Dla przykładu na etapie ustalania zadań widzimy wyłącznie nazwę oraz opis każdego z nich, bez detali dotyczących wykonywanych akcji (aczkolwiek dodanie ich listy ze statusem realizacji jest wskazane).

![](https://cloud.overment.com/2024-10-29/aidevs3_tasks-8c87bbf5-2.png)

Natomiast w prompcie odpowiedzialnym za decydowanie o kolejnej akcji, dostarczony kontekst uwzględnia także **rezultat wcześniejszych kroków**.

![](https://cloud.overment.com/2024-10-29/aidevs3_actions-12494a00-2.png)

Poza dostępem do informacji, istotne jest także zadbanie o logikę odpowiedzialną za **aktualizowanie stanu**. Tutaj zgodnie z tym, czego uczyliśmy się we wcześniejszych lekcjach AI_devs, wszędzie tam, gdzie to możliwe, będziemy wspierać model logiką zapisaną w kodzie.

Zatem w przypadku promptu w którym tworzone / modyfikowane są zadania agenta, programistycznie blokuję możliwość edytowania tych, których status został ustawiony na "zakończony". 

![](https://cloud.overment.com/2024-10-29/aidevs3_state_management-f6b54ddd-d.png)

Stan agenta pełni jeszcze jedną, ważną rolę, dotyczącą zachowania "świadomości" na temat tego, co wydarzyło się pomiędzy wcześniejszymi wiadomościami. Co więcej, decyzja o tym, które z tych informacji należy wczytać, również może zostać podjęta na etapie "wstępnego rozpoznania", który wykonywany jest przed rozpoczęciem pętli. 
## Pamięć

Agent zwykle będzie dysponować pamięcią **długoterminową**, którą będzie mógł przywołać w dowolnym momencie oraz pamięć **krótkoterminową**, do której dostęp będzie możliwy tylko w danym wątku. Mówimy tutaj zarówno **omawianych dokumentach** czy **"wspomnieniach"**, a niekiedy także historii wiadomości. Aczkolwiek w tym ostatnim przypadku, treści rozmów czy nawet pojedynczych poleceń nie stanowią wartości z punktu widzenia przyszłych interakcji. Warto więc ustalić jasne granice pomiędzy treścią, która ma zostać zapisana w pamięci na stałe, a która jest potrzebna jedynie w danej chwili.

W przykładzie `assistant` znajduje się fragment w którym agent wczytuje do wspomnienie na temat "ulubionej muzyki użytkownika". W tym przypadku dodanie jego zawartości do promptu systemowego nie jest problemem, a nawet jest konieczne do dalszego działania. 

![](https://cloud.overment.com/2024-10-30/aidevs3_memories-1bc9b62d-d.png)

Jednak wystarczyłoby, aby zadanie polegało na wczytaniu treści strony www, i szybko mogłoby się okazać, że kontekst promptu zostaje zapełniony informacjami, które w dużej mierze rozpraszają uwagę modelu. W takiej sytuacji warto rozważyć zastosowanie promptów "pobierających istotne informacje" na wzór tych, które działają na etapie "refleksji". 

Alternatywnie możemy skompresować dokument do kilku, kilkunastu słów opisujących jego zawartość. Inaczej mówiąc, nie możemy zapominać o tym, że mamy do dyspozycji model językowy, który może transformować treści na różne sposoby i dopasowywać je w zależności od przypadku. Wówczas nawet jeśli lista wspomnień jest obszerna, to wczytujemy tylko te fragmenty, które są w danym momencie potrzebne.

Także, łącząc wiedzę z lekcji S01E04 — Techniki optymalizacji oraz S03E03 — Wyszukiwanie Hybrydowe, możemy zbudować system pamięci długoterminowej dla agenta. Jednak, oprócz skutecznego przeszukiwania, musimy także zadbać o ograniczenie wczytywanego kontekstu do niezbędnego minimum.

## Plan rozwoju

Mechanika przykładu `assistant` w dużym stopniu przypomina tę, która działa w jednym z moich projektów. W tamtym przypadku agent dysponuje kilkunastoma narzędziami, w ramach których w sumie znajduje się około 70 różnych akcji. Jest więc dość elastyczna, ale powinna być traktowana przede wszystkim jako punkt odniesienia. 

Nie oznacza to jednak, że każdy agent musi mieć taki wachlarz umiejętności, a jego logika może być znacznie prostsza. Z drugiej strony, agent może mieć swój interfejs lub w ogóle nie kontaktować się z użytkownikiem, poza potrzebą weryfikacji efektów jego pracy.

Agent może mieć także formę **jednego pliku**, a jego "specjalizacja" może być na tyle szeroka, aby był w stanie "budować samego siebie". Nie bez powodu umieszczam te wyrażenia w cudzysłowie, ponieważ mam na myśli mały, hobbystyczny projekt, który pomimo wszystko prezentuje ważną ideę. Mowa o [projekcie Ditto](https://github.com/yoheinakajima/ditto). 

![](https://cloud.overment.com/2024-10-30/aidevs_ditto-cf7aa9fb-0.png)

Ditto nie jest też agentem całkowicie wyrwanym od rzeczywistości, ponieważ chociażby projekt [aider.chat](https://aider.chat/) pokazuje wysoką skuteczność modelu w pracy z systemem plików i implementowania funkcjonalności aplikacji.

W budowaniu agentów często nadrzędnym problemem jest sam pomysł. Dlatego warto obserwować rynek w poszukiwaniu projektów, szczególnie tych Open Source, które mogą zainspirować nas do tworzenia własnych agentów. Na GitHub można spotkać repozytoria zawierające obszerne listy takich projektów. Przykładem jest [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents?tab=readme-ov-file#open-source-projects) rozwijana przez e2b, ale można znaleźć więcej takich miejsc. 

![](https://cloud.overment.com/2024-10-30/aidevs3_inspiration-55c5280a-d.png)

Całkiem prawdopodobnym scenariuszem jest także sytuacja w której stworzenie danego agenta nie będzie możliwe lub jego skuteczność będzie zbyt niska, aby można było go sensownie zastosować. Trzeba jednak pamiętać, że zdecydowana większość przykładów przez które do tej pory przeszliśmy, jeszcze rok temu była niemożliwa do wykonania.
## Podsumowanie

Logika agenta, którą zobaczyliśmy dzisiaj może zostać połączona z praktycznie **każdym narzędziem, które omówiliśmy do tej pory w AI_devs 3**. Co więcej, mogą być one wykorzystane w praktycznie dowolnej kolejności, a to otwiera całkiem ciekawe możliwości. 

Poniżej widzimy slajd z jednego z moich warsztatów, który można zestawić z tym, czego do tej pory dowiedzieliśmy się w AI_devs. Mianowicie mając **programistyczne narzędzia** którymi model może się posługiwać, to stosunkowo prosta aplikacja będzie w stanie adresować różne procesy. Konkretnie agent wyposażony w dostęp do Internetu, wczytywanie i tworzenie plików oraz przesyłania maili, poradzi sobie z niemal całkowicie różnymi zadaniami.

![](https://cloud.overment.com/2024-10-30/aidevs3_options-a1ad3007-6.png)

To wszystko powinno zwrócić naszą uwagę na nieco inne zasady projektowania aplikacji. Do tej pory większość z nas tworzyła oprogramowanie posiadające bardzo wąską specjalizację. Tutaj wychodzimy na wyższy poziom abstrakcji, tworząc rozwiązania, które nie opisują precyzyjnie logiki konkretnych zadań. 

Z tej lekcji warto zabrać tylko jedną rzecz i będzie z nią doświadczenie tego, jak jednocześnie przykład `assistant` **może oraz nie może** samodzielnie dopasować się do dowolnej sytuacji. Świadomość ta pozwoli ostudzić entuzjazm związany z w pełni autonomicznymi agentami (przynajmniej na razie), na rzecz tych wyspecjalizowanych, wymagających weryfikacji ze strony człowieka.