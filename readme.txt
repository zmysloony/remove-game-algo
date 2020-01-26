AAL - projekt Usuń i wygraj
Autor: Piotr Zmyślony

- Żeby uzyskać listę opcji uruchomieniowych programu wpisz 'python main.py --help'.

- Dane wejściowe (dla trybów -m1, -m3 i -m4) muszą być w postaci pary liczb całkowitych oddzielonych spacją - poszczególne pary oddzielone znakiem nowej linii. np.:
1 100
2 200

Wyniki prezentowane są w konsoli i na wykresach generowanych przez matplotlib. Dodatkowo, żeby prześledzić dokładnie działanie algorytmu, możesz uruchomić program z opcją -v (--verbose).

- Program składa się z czterech plików:
    - main.py - główny plik uruchomieniowy, który interpretuje parametry, generuje instancje problemu i zajmuje się wyświetlaniem wyników działania
    - classes.py - przechowuje właściwe algorytmy i obiekty
    - findmax.pyx - metoda Cythonowa do przyspieszenia obliczeń
    - setup.py - generuje kod w języku C w pliku findmax.pyx
