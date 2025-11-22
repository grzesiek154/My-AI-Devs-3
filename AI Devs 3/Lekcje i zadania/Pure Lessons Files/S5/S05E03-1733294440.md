![](https://cloud.overment.com/2024-11-04/s05e03-ee52ce90-9.png)

Model językowy może posługiwać się narzędziami, rozszerzając swoją wiedzę i otrzymując nowe umiejętności. Co więcej, jego zdolność do przetwarzania języka naturalnego pozwala na **wskazywanie narzędzia** oraz **opisania sposobu jego użycia**. Jest to mechanizm, który mieliśmy okazję już poznać przy różnych okazjach. 

Połączenie z narzędziami stało się tak ważne, że OpenAI, Anthropic oraz większość innych platform oferuje dedykowane funkcjonalności ułatwiające ten proces. Mowa tutaj o tzw. function calling / tool use.

Mamy więc możliwość przekazania **listy narzędzi**, ich opisów oraz **schematów danych**. Na tej podstawie model może decydować o tym, jaką akcję podjąć w danym momencie. 

Przykład `tool_use` zawiera **dwa narzędzia**: **web_search** oraz **send_mail**. Pomijam tutaj ich implementację i zwracam domyślne wartości, ponieważ nic więcej nie jest nam potrzebne do zrozumienia Function Calling. 

![](https://cloud.overment.com/2024-11-05/aidevs_3-06a0b055-8.png)

Każdą z tych funkcji musimy opisać z pomocą [JSON Schema](https://json-schema.org/) (ale uwaga, bo OpenAI [nie wspiera tej składni w 100%](https://platform.openai.com/docs/guides/structured-outputs#supported-schemas)). Samą strukturę obiektu możemy wygenerować z pomocą LLM, natomiast sami musimy skupić się na trzech rzeczach: 

- nazwach funkcji oraz właściwości
- opisach funkcji oraz właściwości
- zachowaniu **unikatowości** pomiędzy nazwami oraz opisami, aby zmniejszyć ryzyko pomylenia funkcji

Przykład JSON Schema dla funkcji **web_search** wygląda tak: 

![](https://cloud.overment.com/2024-11-05/aidevs3_tools_schema-189d4a09-5.png)

Widzimy więc, że jest to coś, co budowaliśmy do tej pory, ale opisane w ustrukturyzowanej formie. 

Tak przygotowane opisy narzędzi możemy podłączyć do konwersacji. Poniżej w **81 linii** znajduje się właściwość **tools**, czyli **lista schmeatów narzędzi**, do których dostęp ma model. 

![](https://cloud.overment.com/2024-11-05/aidevs3_messages-289d6e24-c.png)

Struktura tych narzędzi zostanie dołączona **do promptu systemowego**, ale OpenAI nie dzieli się szczegółami na temat tego, jak dokładnie się to odbywa. Istotną informacją jest jednak to, że schematy **stanowią część promptu trafiającego do modelu**.

Efektem działania tej logiki na obecnym etapie jest **odpowiedź asystenta** z właściwością `content` ustawioną na `null`. W zamian jednak dostajemy tablicę `tool_calls` zawierającą obiekty opisujące funkcję, którą należy uruchomić wraz z listą argumentów. 

Naturalnie **nie oznacza to, że funkcja została uruchomiona**, ponieważ model nie ma takiej możliwości i samo wykonanie odbywa się po stronie programistycznej (czyli tak, jak robiliśmy to do tej pory). Mamy jednak wszystko czego potrzebujemy, aby uruchomić funkcję. 

![](https://cloud.overment.com/2024-11-05/aidevs_args-86fe44c0-1.png)

Podobnie jak w przykładach z wcześniejszych lekcji, wykorzystujemy dane zwrócone przez model do uruchomienia funkcji. Ale poza tym robimy coś jeszcze. Mianowicie do listy wiadomości **dodajemy dwie pozycje**. Jedną w linii 88, a drugą w linii 102 na poniższym screenie. **W ten sposób do konwersacji trafia informacja o tym, że została wywołana funkcja, oraz jaki był jej rezultat**. 

![](https://cloud.overment.com/2024-11-05/aidevs3_tool_use-73854477-d.png)

No i w zasadzie to jest najważniejsza informacja, której potrzebowaliśmy z Function Calling. Czyli **informacja o posługiwaniu się narzędziami, trafia do rozmowy**. 

## Function Calling vs Własny kod

Function Calling zaprezentowany w przykładzie `tool_use` świetnie strukturyzuje kod i pozwala na wygodne przekazanie informacji o wykonanej akcji do modelu. Jednak przez całe szkolenie AI_devs 3 pokazywałem inne podejście, polegające na samodzielnym tworzeniu logiki odpowiadającej za decydowanie o wyborze funkcji oraz generowania argumentów, a także późniejszego przekazywania wyników do modelu.

Nie stało się tak bez powodu. Otóż wiedza, którą już mamy, pozwala na łatwe korzystanie z Function Calling. Natomiast doświadczenie mówi mi, że nie zawsze będzie to najlepsza opcja. Konkretnie: 

- Function Calling **łączy** etap wybrania funkcji z **generowaniem parametrów do niej**. W przypadku agentów, bardzo często będziemy potrzebowali **czasu** pomiędzy jedną, a drugą akcją. Czyli najpierw decydujemy się na wybór narzędzia, a dopiero potem na wygenerowanie danych do skorzystania z niego. Przykładem może być wybór narzędzia linear, które w celu wykonania akcji potrzebuje kontekstu w postaci listy zadań z ostatnich dni.

![](https://cloud.overment.com/2024-11-23/aidevs3_linear-15597f7b-e.png)

- Sam proces budowania argumentów do wywołania funkcji, może składać się z wielu etapów. Ponownie Function Calling nam to utrudnia. 

- Function Calling domyślnie realizowany jest w ramach jednego wątku. W przeciwnym razie konieczne jest przenoszenie wartości wywołania funkcji + rezultatu zwróconego narzędzia. Inaczej otrzymamy błąd. 

![](https://cloud.overment.com/2024-11-05/aidevs3_continue-5096fb7b-8.png)

- Function Calling (ale tylko w przypadku OpenAI) ogranicza opis narzędzia do 1024 znaków. Trudno powiedzieć, jak długo to ograniczenie będzie utrzymane, bo kiedyś dotyczyło także opisów parametrów. 

![](https://cloud.overment.com/2024-11-04/aidevs3_openai-24d6aa1b-b.png)

- Function Calling wymaga z góry zdefiniowanych schematów funkcji. Rzecz w tym, że nie zawsze będziemy je znać, ponieważ mogą one się zmieniać w zależności od kontekstu. 
- Struktura Function Calling wygląda nieco inaczej w zależności od providera. Jeśli w ramach jednej aplikacji korzystamy z dwóch modeli, komplikuje to logikę. 

Zatem Function Calling ma swoje niezaprzeczalne zalety, ale też uciążliwe wady, które ujawniają się szczególnie w sytuacji, gdy budujemy zaawansowanego agenta AI. Wówczas okazuje się, że detale takie jak natychmiastowe wybieranie funkcji i generowania argumentów, uniemożliwia nam wdrożenie pełnej logiki.

Z tego powodu sam unikam stosowania Function Calling na rzecz własnych implementacji. Nie są one trudne do wdrożenia, a jednocześnie ich skuteczność jest wysoka. **Nie oznacza to jednak, że jest to uniwersalna praktyka** i że nie warto korzystać z Function Calling. Po prostu trzeba mieć na uwadze ograniczenia tej funkcjonalności. 

Jeśli uznasz, że moje spojrzenie na ten temat nie jest poprawne lub Twoje projekty pozwolą Ci na zastosowanie Function Calling, to jako wskazówkę podkreślę fakt, że przy generowaniu JSON Schema bardzo pomocny jest sam model, szczególnie gdy podamy mu jako kontekst treść strony dokumentacji OpenAI na ten temat. Poza tym cała wiedza, którą zdobyliśmy do tej pory, ma bezpośrednie przełożenie na Function Calling. 

## Narzędzia w logice agenta

Samo budowanie narzędzi już wystarczająco omawialiśmy w lekcjach S04E03 oraz S04E05, ale teraz skupimy się na nich w kontekście logiki agenta. 

Zacznijmy od tego, że obecne wyobrażenie agentów często obejmuje ich nieograniczone możliwości i zdolność do wykonywania niezwykle złożonych zadań w sposób autonomiczny. Rzeczywistość jednak tak nie wygląda, a przynajmniej nie w tej chwili, co ma związek zarówno z obecnymi możliwościami modeli, jak i typowo technicznymi ograniczeniami API oraz infrastruktury.

Z tego powodu **wyspecjalizowanie agenta** w określonym obszarze jest dobrym pomysłem. Co więcej, taki agent zwykle **nie powinien mieć kontaktu z użytkownikiem końcowym** lub kontakt ten powinien narzucać pewne ograniczenia. Oczywiście są wyjątki, ale w ich przypadku musimy mieć na uwadze wszystkie wyzwania związane z wdrożeniem takiego systemu, o czym już wielokrotnie mówiłem.

Wyspecjalizowanie agenta pozwala na precyzyjne dobranie narzędzi oraz opisania sposobu korzystania z nich, w tym także relacji, które występują pomiędzy nimi. 

Poniżej mamy przykład zestawu narzędzi dla agenta zdolnego do przeszukiwania Internetu, tworzenia plików, wgrania ich na serwer oraz przesłania mailem. Jest to dość prosty zestaw, którymi model bez większych problemów będzie mógł się posługiwać. 

![](https://cloud.overment.com/2024-11-23/aidevs3_tools-6a65615b-c.png)
 
Zatem jeśli zadanie postawione przed agentem będzie polegać na tym, aby:

- przeszukał wskazane strony pod kątem wspomnianych książek, 
- utworzył plik z listą tych narzędzi
- wgrał go na serwer
- przesłał jako załącznik w mailu

Powyższy plan może zostać wygenerowany przez model i poprawnie zrealizowany, **ale** możemy także rozważyć **wsparcie tej logiki** po stronie programistycznej. Pytanie tylko **jak?**

Otóż jeśli napisanie pliku **zawsze** będzie wiązało się z koniecznością wgrania go na serwer, to nie ma sensu dodawać w tym celu oddzielnego narzędzia. Nie tylko zwiększy to czas potrzebny na wykonanie zadania, ale także stworzy przestrzeń do ewentualnej pomyłki.

Oczywiście takie podejście nie będzie możliwe w przypadku, gdy narzędzie **write** oraz **upload** nie zawsze będą się ze sobą łączyć. Przykładem może być sytuacja w której treść napisanego dokumentu będzie mogła być niekiedy przekazana do innego narzędzia. 

Widzimy zatem, że potrzebujemy określić to, **jaki rodzaj zadań będzie wykonywać nasz agent**. Na tej podstawie przypiszemy do niego narzędzia z których będzie mógł korzystać w różnej konfiguracji. Musimy tylko pamiętać o wnioskach z poprzednich lekcji związanych z tym, że **narzędzia nie mogą się pokrywać** i **muszą posiadać spójny interfejs dla danych wejściowych oraz rezultatów**, dzięki czemu będziemy mogli osadzić je w logice agenta. 

Spójrzmy na początek na schemat, przedstawiający Function Calling. Bloki z czarnym tłem, stanowią część listy wiadomości `messages` wymienianych pomiędzy użytkownikiem, a modelem. Blok bez tła to akcja wykonana programistycznie, która nie jest częścią konwersacji (ale jej rezultat już tak). 

![](https://cloud.overment.com/2024-11-05/aidevs3_tooluse-72091d39-8.png)

W przypadku agenta, schemat wygląda nieco inaczej, ponieważ pojawiają się w nim akcje, których rezultat będzie potrzebny **ale tylko w ramach bieżącego zadania** oraz takie, które pozostaną istotne **na czas trwania całej konwersacji**.

![](https://cloud.overment.com/2024-11-05/aidevs3_agent-66a0c510-c.png)

Inaczej mówiąc, mamy tutaj trzy rodzaje bloków: 

- Te, których treść zostaje w całym wątku bieżącej konwersacji (czarne tło)
- Te, których treść zostaje w bieżącej operacji (prześwitujące tło)
- Te, których treść jest natychmiast usuwana lub przechowywana w innej formie (brak tła)

Także przy projektowaniu agenta, potrzebujemy zaplanować to, **na jak długo zachowujemy dane informacje** oraz **w jaki sposób agent może z nich korzystać**.
## Decyzja o podjęciu działań i opisanie akcji

W poprzedniej lekcji, w przykładzie `assistant`, mieliśmy logikę odpowiedzialną za układanie **zadań** oraz związanych z nimi **akcji**. Zarówno etap **planowania** jak i **wykonywania** uruchamiany jest **w pętli**, co pozwala na jego aktualizację w trakcie wykonywania i reagowanie na bieżące wydarzenia.

Zatem po wygenerowaniu planu, zostaje on przekazany do etapu **wykonania**, w którym zostaje wybrana akcja, która ma zostać uruchomiona jako kolejna. Następnie model generuje obiekt żądania potrzebny do wywołania funkcji. Zatem w przeciwieństwie do Function Calling, model w danej chwili skupia się albo **na wyborze funkcji**, albo **na wygenerowaniu jej parametrów**. 

Przykład `assistant` zawiera zatem oddzielną funkcję, która specjalizuje się wyłącznie w tym, aby **zbudować obiekt żądania** dla akcji aktualnie aktywnego zadania. Inaczej mówiąc — aby przygotować się do podjęcia następnego kroku. 

![](https://cloud.overment.com/2024-11-06/aidevs3_use-6cc83957-9.png)

Obiekt żądania powinien mieć **możliwie prostą strukturę**, a generujący go prompt powinien posiadać **minimum niezbędnych informacji** do jej utworzenia. W sytuacji gdy nie będzie to możliwe i obiekt żądania będzie musiał być skomplikowany, wówczas dobrym pomysłem jest skorzystanie ze [Structured Output](https://platform.openai.com/docs/guides/structured-outputs), które **gwarantuje** zgodność obiektu ze strukturą (ale naturalnie nie gwarantuje, że jego wartości będą zgodne z naszymi oczekiwaniami). 

Gdy zajrzymy do promptu tego przykładu, to zobaczymy że mamy tam informację **tylko o jednym narzędziu** oraz **bieżącej akcji**. Brakuje więc w nim wiedzy o rezultatach wcześniejszych kroków, ale nie powinno mieć to znaczenia, ponieważ wszystkie niezbędne dane powinny być zawarte w zapytaniu użytkownika.

![](https://cloud.overment.com/2024-11-06/aidevs3_action_prompt-d2a75bfa-c.png)

No bo przykładowo, jeśli w kroku pierwszym pobraliśmy listę trzech koncepcji, takich jak Transformer, Encoder, Decoder, to w drugim kroku zapytanie wymagające skorzystania z wyszukiwarki powinno brzmieć: "**Znajdź informację na temat: Transformer, Encoder i Decoder**".

Może się jednak zdarzyć, że dodanie informacji o wcześniejszych krokach będzie tutaj wymagane. Przykładem może być polecenie: "**Wejdź na tę stronę `https://...` i pobierz z niej dane oraz wyślij mi je na e-mail**". Wówczas do wysłania maila **musimy mieć dane pochodzące z wcześniejszej akcji**. 

Wniosek jest więc prosty — struktura agenta będzie różnić się w zależności od jego specjalizacji. I choć można już mówić o agentach ogólnego zastosowania, doświadczenie sugeruje mi, że jest na to jeszcze dość wcześnie ze względu na ograniczenia modeli oraz narzędzi. Możliwe jednak, że zmieni się to w nadchodzących miesiącach ze względu na duży nacisk branży na temat agentów. 

Nie wiem, czy to wyraźnie widać, ale w logice agenta **programistycznie selekcjonujemy dane** i **wykorzystujemy je w kilku lub kilkunastu mniejszych zapytaniach**. Oczywiście, nie zawsze będzie to konieczne, a czasem nawet niewskazane. Jeśli możemy wykonać jakieś operacje jednym zapytaniem i osiągnąć wysoką skuteczność, powinniśmy to zrobić. Z kolei, gdy skuteczność działania agenta spada, poszukiwanie sposobu na rozbicie jego aktywności na mniejsze kroki zwykle będzie dobrym kierunkiem.

Zatem podsumowując: 

- Etap wykonania, powinien być odseparowany od etapu planowania. Samo wykonanie musi skupiać uwagę modelu wyłącznie na uruchomieniu narzędzi, a nie decydowaniu o tym, które z nich wybrać. Wyjątek stanowi prosta logika z którą model poradzi sobie w ramach jednego zapytania. 
- Struktury danych potrzebne do uruchomienia narzędzi powinny być tak proste, jak to możliwe, aby redukować ryzyko błędu.
- Ilość danych na których pracuje model przy korzystaniu z umiejętności/narzędzia, powinna być jak najmniejsza, ale jednocześnie powinna obejmować wszystkie niezbędne informacje.

## Reagowanie na podjęte akcje i błędy

W związku z tym, że w przykładzie `assistant` mamy jedynie przykładowe implementacje narzędzi, skorzystam tutaj z fragmentów kodu pochodzących z jednego z moich projektów. 

Poniżej znajduje się **jedna funkcja**, która jest uruchamiana przez **każde narzędzie**, ale na podstawie jej argumentów wybierany jest docelowy serwis oraz funkcja. Inaczej mówiąc, mamy tutaj metodę **decydującą** o tym, w jaki sposób obsłużyć wskazane narzędzie oraz wygenerowany obiekt żądania. 

Co więcej, od razu widzimy, że w przypadku błędu zwracam tutaj **dokument** zawierający informację o **niepowodzeniu**. Struktura tego dokumentu jest taka sama jak tych, które wykorzystujemy do pracy z plikami czy zewnętrznymi źródłami wiedzy. Pytanie tylko — dlaczego? 

![](https://cloud.overment.com/2024-11-06/aidevs3_executor-9cc196f8-b.png)

Otóż zawsze powtarzam, że w logice agenta powinniśmy dążyć do uzyskania spójnego formatu danych. W ten sposób możliwe będzie łączenie różnych modułów bez konieczności tworzenia dedykowanych połączeń. Dane będą po prostu swobodnie między nimi przepływać. Dlatego w tym przypadku **podjąłem decyzję o takiej, a nie innej strukturze danych**. 

Wynika więc to z **mojej decyzji** oraz **potrzeb danego projektu**, a nie standardu. Jednym założeniem, którego trzeba się tutaj trzymać, jest zachowanie spójności. To wszystko.

Zatem, patrząc na kod zapisany powyżej, nie ma większego znaczenia to, czy mój agent będzie posługiwał się 1 czy 50 narzędziami (w przypadku większej liczby, proces decyzyjny może być bardziej złożony). Wystarczy tylko, że zaktualizuję listę dostępnych serwisów, a ten sam kod będzie obsługiwał je wszystkie. Co więcej, niezależnie od tego, czy wystąpi błąd, czy zostaną uruchomione poprawnie, ten sam format danych zapewni, że agent zostanie o tym zdarzeniu właściwie poinformowany.
## Aktualizacja planu z postępami

Jeśli główna logika agenta (ta wykonująca się w pętli) zostanie poprawnie połączona ze stanem, a dynamiczne elementy promptu będą poprawnie wczytywać wszystkie informacje, to aktualizacja planu działań wydarzy się automatycznie. Po prostu do kontekstu będą trafiać nowe dane i model będzie reagował zgodnie z nimi. Jest jednak tutaj kilka rzeczy, które zasługują na uwagę. 

Po pierwsze — **organizacja informacji**.

Do tej pory **cały kontekst** trafiał do promptu systemowego. Oznacza to, że zawarte w nim informacje znajdują się **powyżej listy wiadomości**, sugerując, że zdarzenia te wydarzyły się **wcześniej**.

Widzimy to na schemacie poniżej, na którym po prawej stronie znajduje się podgląd etapu "Plan Next Step". Widać wyraźnie, że lista podjętych kroków znajduje się **przed** zapytaniem użytkownika. 

![](https://cloud.overment.com/2024-11-06/aidevs3_confusion-fa782d9c-e.png)

Taka organizacja informacji **może** (ale nie musi) zaburzyć ich zrozumienie instrukcji i doprowadzić do **ponownego wykonania tych samych działań**. 

Przykład: **Użytkownik prosi o wyłączenie światła**. Agent wykonuje tą akcję, a informacja o niej trafia **do promptu systemowego**. 

Tutaj z perspektywy modelu, użytkownik **wciąż prosi o wyłączenie światła**, ponieważ jego zapytanie znajduje się "później", niż informacja o wykonanej akcji. 

No i w tym miejscu użyteczne okazuje się to, co sugeruje nam Function Calling, a mianowicie **dodawanie jako wiadomości asystenta/narzędzia** do konwersacji. Dzięki temu lista podjętych działań pojawia się **po zapytaniu użytkownika** i ma to logiczny sens. 

![](https://cloud.overment.com/2024-11-06/aidevs3_order-eb0824ad-8.png)

Podobne sytuacje można spotkać przy różnych okazjach, szczególnie gdy złożoność logiki agenta / agentów będzie wzrastać. Mówię o tym dlatego, aby zwrócić uwagę na dbanie o porządek, spójność formatu danych oraz możliwie wysoką dokładność w kodzie aplikacji. 

Niezależnie od tego, czy błąd logiki ma miejsce po stronie programistycznej, czy po stronie modelu, to przy jego rozwiązaniu możemy skorzystać z pomocy LLM. Sam już wielokrotnie przekonałem się, że nawet "debugowanie" promptu jest znacznie łatwiejsze, gdy pojawiający się problem omawiam z modelem. 

Poniżej mamy fragment wypowiedzi, w której GPT-4o pomógł mi zrozumieć dlaczego w niektórych przypadkach agent decyduje się na wybór wyszukiwarki Internetowej, pomimo tego, że użytkownik nie wspomina aktualnych informacji. Model wskazał jednak, że określenie "modern neuroscience" może być zinterpretowane jako zagadnienie wymagające dostępu do sieci i po części trudno się z tym nie zgodzić.

![](https://cloud.overment.com/2024-11-06/aidevs3_analysis-7cf43958-c.png)

Podobnie też model pomógł mi rozwiązać problem dotyczący zapętlającej się logiki, gdy po raz pierwszy spotkałem problem kolejności wykonanych zadań, o którym wspomniałem wcześniej.

Idąc dalej, to model pomaga mi **w kształtowaniu promptów**, w **opisywaniu narzędzi**, **planowaniu struktur danych** czy układaniu **całej logiki agenta**. Takie wsparcie odbywa się poprzez czas oraz standardowe, iteracyjne dążenie do rozwiązania. Inaczej mówiąc — **dbamy tutaj o to, aby projektować takie systemy, wspierając się możliwościami aktualnych modeli.** 
## Kontakt z użytkownikiem, oraz odpowiedź

W przykładzie `assistant` kontakt agenta z użytkownikiem może wystąpić w dwóch sytuacjach: **gdy agent o tym zdecyduje**, lub gdy zostanie przekroczony **limit dopuszczalnych iteracji pętli.** W obu przypadkach chodzi o wywołanie akcji "final_answer". 

Jednak sytuacji w których programistycznie wymuszamy kontakt z użytkownikiem, może być więcej. Jedną z nich może być **potwierdzenie uruchomienia akcji**. 

No bo do tej pory mówiłem, że powinniśmy bezwzględnie uniemożliwiać agentowi podejmowanie działań, których rezultatów nie można odwrócić. Przykładem takiej akcji jest wysłanie maila. 

Natomiast nic nie stoi na przeszkodzie, aby w momencie, gdy agent zdecyduje się na wysłanie maila i nawet wygeneruje jego treść, programistycznie zakończyć lub wstrzymać jego działanie. Wówczas użytkownik może otrzymać informację lub dynamiczny komponent, który pozwoli mu na wykonanie tej "nieodwracalnej" akcji. Następnie potwierdzenie jej wykonania może wrócić do agenta i wznowić jego działanie, ale eliminujemy tutaj w pełni element "niedeterministycznej natury". 

Taki rodzaj kontaktu zakłada jednak, że nasz agent posiada jakiś interfejs pozwalający na kontakt z użytkownikiem, a nie zawsze tak będzie. Wówczas samo potwierdzenie może odbyć się poprzez **przesłanie maila** czy wiadomości **na Slacku**. Poniżej przykład wiadomości napisanej na podstawie linku do filmu z kanału [AI Explained](https://www.youtube.com/@aiexplained-official). 


![](https://cloud.overment.com/2024-11-18/aidevs3_mail-4203c17b-9.png)

Z kolei jeśli graficzny interfejs będzie dostępny, możemy rozważyć skorzystanie z rozwiązań takich jak Vercel AI SDK oraz jego funkcjonalności **generatywnego UI**. Poniżej widzimy przykłady pochodzące ze strony, w których odpowiedzi asystenta mają formę nie tylko tekstu, ale dynamicznych komponentów, uzupełnionych danymi dopasowanymi do zapytania. 

![](https://cloud.overment.com/2024-11-06/aidevs3_generativeui-92ccd330-7.png)

Także projektując system wykorzystujący logikę agencyjną, musimy odpowiedzieć sobie na pytanie: **w jaki sposób będzie odbywać się interakcja z użytkownikiem**. Konkretnie:

- **działanie w tle:** wykonywanie zadań odbywa się bez kontaktu z człowiekiem i dopiero rezultat przechodzi w jego ręce. Przykładem może być agent reagujący na zdarzenia na których podstawie podejmuje decyzję o potrzebnych akcjach
- **kontakt asynchroniczny**: wykonanie zadań nie wymaga bieżącego kontaktu z człowiekiem, ale samo zlecenie pochodzi od użytkownika. Przykładem może być agent z którym można komunikować się poprzez e-mail
- **kontakt bezpośredni:** wykonywanie zadań odbywa się przy współpracy z człowiekiem, a wymiana informacji odbywa się na czacie. 
- **kontakt w czasie rzeczywistym**: to wariant kontaktu bezpośredniego, lecz w tym przypadku nacisk położony jest na niski czas reakcji
- **kontakt z samym sobą**: agent może być wyposażony w narzędzie **planowania zadań** pozwalającego na ustawienie kolejki zapytań, których wykonanie może być uzależnione od spełnionych warunków (np. określony czas i lokalizacja)

To jednak nie wszystko, ponieważ mówimy tutaj nie tylko o ogólnych założeniach systemu, ale także detalach opisujących zakres odpowiedzialności oraz uprawnień agenta, a także użytkownika lub innych agentów.
## Podsumowanie

Praktycznie **wszystkie** dotychczasowe przykłady kodu, które pojawiły się w treści lekcji, po dopasowaniu mogą pełnić rolę narzędzi dla agenta. W praktyce większość z nich, w nieco zmienionej formie działa w na co dzień w moich aplikacjach i automatyzacjach.

Ostatecznie to w jaki sposób zorganizowana jest logika agenta oraz do jakich narzędzi ma dostęp, będzie zależało wyłącznie od nas. Wszystko, co pokazałem do tej pory może stanowić albo punkt startowy, albo jedynie przykład, którego wprost nie będziesz stosować w praktyce.

Jest tutaj jednak kilka bardzo uniwersalnych reguł, które powinny sprawdzić się w każdym z Twoich projektów. Mowa o:

- **Głównej logice agenta** zaprojektowanej w taki sposób, aby dołączanie lub odłączanie kolejnych narzędzi, nie było od niej uzależnione. Dzięki temu zachowujemy dużą elastyczność, co ułatwia rozwój systemu.
- **Wspólny format danych** z którymi pracuje agent. Tutaj moją sugestia polega na stosowaniu dokumentów o tej samej strukturze, którą wykorzystywaliśmy na potrzeby RAG. Dzięki temu dokładnie ten sam format danych możemy wykorzystywać **zarówno w pamięci, umiejętnościach agenta, jak i przetwarzaniu dokumentów**, co ponownie daje ogromną elastyczność
- **Niezależność** narzędzi, pozwalająca na ich wykorzystanie **poza logiką agenta**. Przykładowo narzędzie `websearch` omawiane we wcześniejszych lekcjach, powinno być dla nas dostępne bez konieczności angażowania agenta. Pozwala to na tworzenie prostych automatyzacji czy wykorzystywanie tej samej logiki w wielu miejscach.

W tej chwili, mając na uwadze wszystko, co do tej pory dowiedzieliśmy się na temat agentów, możesz zastanowić się nad tym — jak mógłby działać pierwszy, prosty agent pracujący dla Ciebie.

Podziel się swoim pomysłem w komentarzu.