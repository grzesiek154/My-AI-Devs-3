![](https://cloud.overment.com/S04E05-1732795281.png)

Proste zadania wykonywane przez LLM można uprościć do pojedynczego żądania HTTP. W przypadku niepowodzenia wystarczy powtórzyć zapytanie. W praktyce jednak potrzebujemy także złożonych zadań, składających się z wielu kroków. Dodatkowo, niezależnie od poziomu skomplikowania, chcemy zachować historię podjętych działań.

Potrzebujemy logiki pozwalającej na planowanie zadań, uruchamianie ich według harmonogramu oraz wznawianie tych, które nie zostały poprawnie zakończone, bez konieczności uruchamiania ich od początku.

Sama logika kolejkowania zapytań i przetwarzania rozbudowanych zadań w tle, nie jest nową koncepcją w programowaniu. Możemy więc zastosować podejście [event driven design](https://en.wikipedia.org/wiki/Event-driven_architecture) uwzględniające komunikację w czasie rzeczywistym (co zresztą sugeruje także real time API). Warto rozważyć ten kierunek ze względu na możliwość łatwego informowania o postępach oraz w pełni asynchronicznej komunikacji. Na początek wystarczy nam jednak możliwość tworzenia listy zadań oraz powiązanych z nią akcji i dokumentów.

W tej lekcji zbudujemy strukturę bazy danych i interfejs, który połączy nasze dotychczasowe doświadczenia w tworzeniu narzędzi dla LLM oraz integracji z zewnętrznymi danymi. Skupimy się na mechanice i kluczowych koncepcjach, a praktyczne wykorzystanie przez LLM omówimy w ostatnim tygodniu AI_devs. 
## Struktura danych

Do zarządzania zadaniami, potrzebna będzie nam struktura bazy danych, uwzględniająca:

- Historię konwersacji przypisanych do użytkownika
- Listę wiadomości powiązanych z konwersacją oraz z dokumentami
- Zadania powiązane z konwersacją oraz listą akcji
- Akcje powiązane z narzędziami oraz dokumentami

Inaczej mówiąc, chodzi nam o strukturę umożliwiającą zapisywanie interakcji z modelem, uwzględniając także podejmowane działania. Nie chodzi jednak tutaj o monitorowanie zachowania modelu, które przechodziliśmy na przykładzie LangFuse, lecz zapisywania danych, które są istotne dla sterowania logiką agenta (bądź agentów). 

Przykładowy schemat wygląda następująco: 

![](https://cloud.overment.com/2024-10-23/aidevs3_schema-06ab2daf-d.png)

Oczywiście detale związane z rodzajem tabel, kolumn oraz połączeń pomiędzy nimi, będą ulegały zmianie w zależności od aplikacji, którą będziemy tworzyć. Natomiast można uznać, że powyższy schemat jest dobrym punktem startowym. 

Po uruchomieniu przykładu `events` w jego katalogu zostanie utworzona baza danych SQLite i wykonana prosta symulacja rozmowy pomiędzy użytkownikiem, a asystentem, w której zachodzi potrzeba transformacji prostego dokumentu. Składają się na nią:

- **Utworzenie dokumentu**: krok ten można porównać do momentu w którym użytkownik wgrywa plik na serwer. Informacje o dokumencie zostają zapisane w bazie.
- **Utworzenie narzędzia:** w praktyce lista narzędzi będzie już dostępna, więc nie będziemy ich tworzyć. Po prostu agent będzie decydował o tym, które z narzędzi uruchomić na potrzeby poszczególnych akcji
- **Utworzenie / pobranie konwersacji**: na podstawie `conversation_uuid` pobieramy lub tworzymy wątek z listą wiadomości
- **Wiadomość użytkownika:** użytkownik przesyła prośbę o "analizę raportu"
- **Utworzenie zadania:** do konwersacji zostaje dopisane nowe zadanie
- **Utworzenie akcji:** akcja zostaje przypisana do zadania oraz dokumentu
- **Aktualizacja statusów:** statusy akcji oraz zadania zostają zaktualizowane jako 'zakończone'
- **Odpowiedź:** użytkownik otrzymuje gotowy dokument

![](https://cloud.overment.com/2024-10-23/aidevs3_processing-eaa9b7e3-a.png)

Taka logika pozwala nam na bardzo elastyczne prowadzenie interakcji, w tym także tworzenie wielu zadań i powiązanych z nimi akcji. Nic też nie stoi na przeszkodzie, aby system otrzymywał cyklicznie "polecenia", a **nawet przesyłał je sobie samodzielnie**.
## Odpowiedzialność modelu i programistyczne wsparcie

Rola modelu w logice powinna być ograniczona wyłącznie do zadań, których nie da się wykonać programistycznie. Natomiast wszystkie pozostałe aktywności, pozostać zapisane w kodzie. Przykładowo: 

- **Domyślne właściwości:** domyślne właściwości obiektu JSON powinny być ustawiane automatycznie (np. zakres dat dla przeszukiwania)
- **Weryfikacja:** Przy zadaniach związanych z klasyfikacją do wskazanej listy kategorii, zawsze programistycznie musimy sprawdzać, czy zwrócona odpowiedź jest jedną z dopuszczalnych nazw
- **Referencja:** Jeśli model może wskazać potrzebny zasób, lepiej wybrać tę opcję zamiast zmuszać go do przepisywania treści
- **Pętle:** Jeśli logika uwzględnia swobodę modelu w aspekcie samoodniesienia, to w kodzie musimy wprowadzić ograniczenia zapobiegające zapętleniu
- **Kontekst:** Choć model powinien móc wskazywać dokumenty do wczytania w kontekście, to warstwa programistyczna powinna określać sposób ich prezentacji oraz zakres uwzględnianych właściwości

Mówiąc inaczej, zawsze musimy zadawać sobie pytanie o to, **czy za daną akcję faktycznie musi odpowiadać model** i tam gdzie to możliwe, minimalizować jego zaangażowanie. 
## Efektywne posługiwanie się narzędziami

Na temat efektywnego posługiwania się narzędziami dowiedzieliśmy się już przy okazji ich budowania. Jednak teraz rysuje się nam obraz logiki zdolnej do samodzielnego posługiwania się nimi. Łącząc to z naszym doświadczeniem zarówno w kontekście programowania jak i pracy z modelami, możemy połączyć fakty i zauważyć, że:

- **Kontrola instrukcji:** Instrukcje ze strony użytkowników zwykle są bardzo nieprecyzyjne, a model posługujący się narzędziami tej precyzji wymaga. Możemy więc próbować "wzbogacać zapytania użytkownika" lub dopytywać go o szczegóły, albo **ograniczyć kontakt z modelem do minimum**. W końcu nikt nie powiedział, że zapytania do modelu muszą pochodzić od człowieka i mogą być one generowane w wyniku **akcji, które użytkownik podejmuje**. Np. dodanie pliku przesyła zapytanie w stylu "Wczytaj treść dokumentu `[[uuid]]`, wypisz z niego wszystkie zagadnienia z kategorii `...` i prześlij na e-mail `@`". 
- **Kompresja:** Podział `task > action > tool` oraz relacja `action > documents` zapewnia elastyczny dostęp do danych i kontrolę nad ich szczegółowością. Możemy opisać zadanie używając tylko **nazw zadania, akcji i kategorii** lub rozszerzyć je o **opisy, kontekst i powiązania**. Takie podejście wspiera **zarządzanie ilością informacji kierowanych do promptu systemowego**, co sprzyja zasadzie "ograniczania szumu" w postaci zbędnych treści
- **Wznawianie:** Zarówno `task` jak i `action` posiadają statusy, które umożliwiają reagowanie na problemy i kontynuację w miejscu wystąpienia błędu. Reakcja może być automatyczna, gdzie model sam decyduje o korekcie danych wejściowych. Należy jednak zawsze implementować programistyczne limity, jak maksymalna liczba prób przed oznaczeniem zadania statusem `failed`
- **Pamięć podręczna:** Część akcji będzie bardzo powtarzalna i czasem nie będzie potrzeby wykonywać ich wielokrotnie. Jednocześnie zapytania nie będą **dokładnie takie same** i nie będziemy mogli ich ze sobą porównać. Dlatego warto rozważyć tzw. `semantic cache` polegający na indeksowaniu **zapytań użytkownika** i ich przeszukiwaniu w celu odnalezienia tych najbardziej podobnych
- **Podział:** Podział zadań na `akcje` pozwala wyróżnić bardzo małe, pojedyncze aktywności, na których model może się w danej chwili skupić. To istotny detal wpływający na skuteczność całego systemu - ryzyko rozproszenia uwagi modelu jest mniejsze przy prostych zadaniach niż przy złożonych operacjach na dużym zestawie danych. Przykład: generowanie zagnieżdżonej struktury obiektu JSON jest znacznie trudniejsze, niż wygenerowanie kilku mniejszych obiektów i programistyczne połączenie ich w całość.
- **Weryfikacja:** Zarówno na etapie `task` jak i `action` możemy dodać prompty weryfikujące to, czy odpowiedź modelu jest poprawna, ponieważ jak już wiemy, że "weryfikacja jest prostsza niż generowanie"

Co więcej, w przypadku promptów, które wymagają posługiwania się pamięcią długoterminową lub dużym zestawem zewnętrznych danych, warto rozważyć cache'owanie promptu oraz zaangażowanie modelu Gemini 1.5 Pro (Google DeepMind), który charakteryzuje się bardzo dużym limitem okna kontekstowego. 

## Oczekiwanie na odpowiedź

W przypadku zadań (`task`) jedna z właściwości określa to, czy ich realizacja ma nastąpić asynchronicznie. Oznacza to, że użytkownik dostanie jedynie potwierdzenie tego, że zadanie zostało rozpoczęte. Natomiast rezultat zostanie do niego dostarczony mailem lub innym kanałem komunikacji. Ponownie w takim przypadku można rozważyć skorzystanie z `web socketów` lub alternatywnych rozwiązań dla aplikacji real-time.

W projektowaniu doświadczeń użytkownika (UX design) powszechnie mówi się o tym, że **użytkownik nie ma problemu z oczekiwaniem, o ile widzi postęp**. Przykładem może być przechodzenie przez wieloetapowy proces rejestracji w którym widoczny jest pasek postępu. Inną sytuacją może być korzystanie z wyszukiwarki z rozbudowanymi filtrami, w przypadku których każdy kolejny krok przybliża nas do celu.

Dlatego przy budowaniu generatywnych aplikacji, które wykonują złożone zadania, warto rozważyć interfejs wyświetlający aktualne postępy. Może on uwzględniać także opcję kontaktu z użytkownikiem w dowolnej chwili, w tym także przerwanie operacji. 

Przykładem może być tutaj [real-time console](https://github.com/openai/openai-realtime-console), czyli repozytorium prezentujące możliwości [Real-time API](https://openai.com/index/introducing-the-realtime-api/) od OpenAI. Aktualnie korzystanie z tej usługi jest kosztowne, lecz zawarte w niej koncepcje można wykorzystać w połączeniu z dowolnymi modelami.

![](https://cloud.overment.com/2024-10-23/aidevs3_realtime-2c6e76c8-f.png)

Jeśli posiadasz już dostęp do OpenAI Real Time API, to spróbuj uruchomić wspomnianą konsolę. Pamiętaj jednak o tym, że **koszt korzystania z niej w chwili pisania tych słów jest bardzo wysoki, więc zapoznaj się wcześniej z aktualnym cennikiem**.
## Kolejkowanie zapytań

Praktycznie każde API, z którym przyjdzie nam pracować, posiada rate limit, który może skutecznie przerwać wykonywanie naszych zadań. W przypadku modeli językowych, limity obejmują **liczbę zapytań**, **liczbę tokenów na minutę / dzień**, **liczbę tokenów wejściowych**, **liczbę tokenów wyjściowych**, a także sam budżet. W dodatku dla usług takich jak Anthropic musimy brać pod uwagę także częste problemy z dostępnością samego API.

Limity najłatwiej ominąć korzystając z bibliotek takich jak Vercel AI SDK czy frameworków takich jak LangChain. Możemy także bez większych problemów stworzyć własną integrację do kontrolowania liczby zapytań oraz oczekiwania na ponowną dostępność usługi.

W przypadku OpenAI oraz Anthropic otrzymujemy także informację na temat aktualnych limitów, które zapisane są w formie nagłówków HTTP. Na podstawie ich wartości możemy określić czas oczekiwania na dalsze zapytania. 

![](https://cloud.overment.com/2024-10-23/aidevs3_rate_limit-a9b3550c-3.png)

Rate Limit dotyczy także innych usług z którymi będziemy się integrować. Przykładem może być FireCrawl, który ma duże ograniczenia związane z liczbą równolegle przeglądanych stron.
## Specjalizacja i generalizacja

Programowanie do tej pory charakteryzowało się deterministycznymi rozwiązaniami. Projektując je, dążymy do opisania w kodzie wszystkich możliwych scenariuszy i poprowadzenia przepływu danych tak, aby uzyskać pożądany efekt. Co więcej **takie również jest oczekiwanie naszych pracodawców, klientów i użytkowników**. Natomiast wiemy już, że w przypadku generatywnych aplikacji coś takiego nie jest możliwe i z "pewności" przeszliśmy w obszar "prawdopodobieństwa". 

Pytanie więc: **co możemy z tym zrobić?**

Obecna generacja modeli językowych jest na tyle zaawansowana, że sama ta nazwa nie oddaje już w pełni możliwości. Pomimo tego, sami doświadczamy ich aktualnych ograniczeń, w tym także trudności w prowadzeniu ich nawet w okolice wybranego celu.

Mówiąc inaczej — **czas w którym modele językowe będą w stanie autonomicznie wykonywać bardzo złożone zadania, jeszcze nie nadszedł**.

Przykładowo, jeśli tworzymy **system do zarządzania projektami** z integracją do rozbudowanego rozwiązania takiego jak ClickUp, trudno stworzyć go w sposób elastyczny, który dopasuje się do dowolnej organizacji. Natomiast w naszym zasięgu jest dostosowanie systemu do nas samych, naszego zespołu czy całej firmy. Powodem jest fakt, że każdy używa narzędzi takich jak ClickUp w nieco inny sposób, a brak kontekstu w tym zakresie obniży skuteczność działania modelu.

Mówimy więc tutaj o **bardzo wąskiej specjalizacji**.

Z drugiej strony, na przykładzie `todo` przekonaliśmy się, że nawet taki system **nie będzie działał** w oparciu o **sztywno zdefiniowane reguły**, lecz **ogólne zasady opisujące dobieranie akcji i sposobu ich wykonania**.

Otrzymujemy więc tutaj **połączenie** generalizacji i specjalizacji, której granicę będziemy przesuwać coraz dalej w kierunku autonomiczności, wraz z rozwojem modeli oraz ekosystemu narzędzi. 

Wniosek jest następujący: **projektując generatywne aplikacje nie możemy podążać schematami, które znamy z klasycznych aplikacji**. Powodem jest fakt, że mamy do dyspozycji zupełnie inną kategorię narzędzi i gramy według nowych zasad.
## Zaangażowanie użytkownika

Na temat **weryfikacji**, **feedbacku** ze strony człowieka oraz **ograniczenia kontaktu** mówiliśmy już całkiem sporo. Jest jednak jeszcze kilka kwestii:

- **Personalizacja:** dobrze zaprojektowany system powinien być w stanie **dopasowywać się do użytkownika**. Mowa tutaj nie tylko o dynamicznych fragmentach promptu takich jak imię, nazwy projektów czy budowanie pamięci długoterminowej, ale także **wyciąganie wniosków z interakcji i autonomiczne ulepszanie promptów**. 
- **Transparentność:** dużo mówi się na temat problemów związanych z przechwyceniem promptu systemowego przez użytkownika. W praktyce jednak, ich **udostępnienie** może okazać się korzystne, ponieważ pomaga to lepiej zrozumieć działanie systemu, nawet osobom nietechnicznym
- **Przekierowanie:** zawsze gdy model generuje nowy dokument, wpis w systemie CRM lub tworzy dowolny, nowy zasób, warto wygenerować link kierujący do niego. Jest to dobra praktyka, która pozwala także na szybkie zweryfikowanie odpowiedzi modelu. W przypadku większości aplikacji, możemy wygenerować taki link korzystając z parametru `?id=7bbe3` lub jego odpowiednika
- **Potwierdzenie:** wiemy, że model nie powinien być bezpośrednio połączony ze Światem i np. publikowanie wpisów i komentarzy w mediach społecznościowych, powinno być dla niego niedostępne. Dlatego w odpowiedzi możemy **dołączyć link** pozwalający na szybkie **potwierdzenie** wygenerowanej treści i jej publikację. Potwierdzenie to musi być obsługiwane już wyłącznie przez kod (nie model).
- **Odwoływanie do samego siebie:** system powinien mieć możliwość korzystania z własnego API, w tym także wpływania na elementy promptów lub budowania dynamicznych narzędzi w środowisku typu "sandbox" (np. e2b). Odwoływanie do samego siebie może obejmować także wydawanie sobie poleceń, dokładnie tak samo, jak robi to użytkownik
- **Prośba o pomoc:** część narzędzi powinna umożliwiać "zawieszenie" wykonania do czasu uzyskania pomocy ze strony człowieka. Może to mieć miejsce w wyniku braku dostępu do usługi lub przekroczeniu liczby dostępnych prób wykonania zadania 

W skrócie: generatywne aplikacje powinny dopasowywać się do użytkownika i tworzyć dla niego wartość, przy jednoczesnym minimalizowaniu wymaganego zaangażowania z jego strony.

##Podsumowanie

W tej lekcji zapoznaj się przede wszystkim ze strukturą tabeli z przykładu events. Jeśli masz już pomysł na swojego agenta (nawet prostego), to zastanów się w jaki sposób zorganizujesz dane na których będzie on pracował. I nie mam tutaj na myśli wyłącznie pamięci czy informacji wczytanych z plików, ale przede wszystkim historię wiadomości, historię podjętych działań czy mechaniki obsługi błędów w taki sposób, aby agent miał możliwość podjęcia próby ich naprawienia.

O szczegółach porozmawiamy w ostatnim tygodniu AI_devs 3.