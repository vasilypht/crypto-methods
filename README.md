<p align="center">
    <img src="/resources/crypto-methods.png" alt="preview" height="128" width="128">
</p>
<div>
    <h1 align="center">Crypto-methods</h1>
    <p align="center">Laboratory work on the subject "Cryptographic methods of information protection". These works include asymmetric and symmetric encryption, as well as some cryptanalysis methods.</p>
</div>

![image-app](/resources/screenshots/image-app.png)


## :books: Contents

- [**Supported ciphers**](#fire-features)
- [**Dependencies**](#gear-dependencies)
- [**Installation**](#hammer_and_wrench-installation)
- [**Attribution links**](#link-attribution-links)

## :fire: Features


| Category           | Module                                                                 | Widget                                                                                        | Description                                                                        |
|--------------------|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Symmetric ciphers  | [`atbash.py`](/app/crypto/symmetric/atbash.py)                         | [`atbash_widget.py`](/app/gui/symmetric/atbash/atbash_widget.py)                              | [Atbash cipher](https://en.wikipedia.org/wiki/Atbash)                              |
|                    | [`scytale.py`](/app/crypto/symmetric/scytale.py)                       | [`scytale_widget.py`](/app/gui/symmetric/scytale/scytale_widget.py)                           | [Scytale cipher](https://en.wikipedia.org/wiki/Scytale)                            |
|                    | [`polybius_square.py`](/app/crypto/symmetric/polybius_square.py)       | [`polybius_square_widget.py`](/app/gui/symmetric/polybius_square/polybius_square_widget.py)   | [Polybius square](https://en.wikipedia.org/wiki/Polybius_square)                   |
|                    | [`caesar.py`](/app/crypto/symmetric/caesar.py)                         | [`caesar_widget.py`](/app/gui/symmetric/caesar/caesar_widget.py)                              | [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher)                       |
|                    | [`cardan_grille.py`](/app/crypto/symmetric/cardan_grille.py)           | [`cardan_grille_widget.py`](/app/gui/symmetric/cardan_grille/cardan_grille_widget.py)         | [Cardan grille](https://en.wikipedia.org/wiki/Cardan_grille)                       |
|                    | [`richelieu.py`](/app/crypto/symmetric/richelieu.py)                   | [`richelieu_widget.py`](/app/gui/symmetric/richelieu/richelieu_widget.py)                     | Richelieu cipher                                                                   |
|                    | [`alberti_disc.py`](/app/crypto/symmetric/alberti_disc.py)             | [`alberti_disc_widget.py`](/app/gui/symmetric/alberti_disc/alberti_disc_widget.py)            | [Alberti cipher](https://en.wikipedia.org/wiki/Alberti_cipher)                     |
|                    | [`gronsfeld.py`](/app/crypto/symmetric/gronsfeld.py)                   | [`gronsfeld_widget.py`](/app/gui/symmetric/gronsfeld/gronsfeld_widget.py)                     | Gronsfeld cipher                                                                   |
|                    | [`vigenere.py`](/app/crypto/symmetric/vigenere.py)                     | [`vigenere_widget.py`](/app/gui/symmetric/vigenere/vigenere_widget.py)                        | [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)              |
|                    | [`playfair.py`](/app/crypto/symmetric/playfair.py)                     | [`playfair_widget.py`](/app/gui/symmetric/playfair/playfair_widget.py)                        | [Playfair cipher](https://en.wikipedia.org/wiki/Playfair_cipher)                   |
|                    | [`hill.py`](/app/crypto/symmetric/hill.py)                             | [`hill_widget.py`](/app/gui/symmetric/hill/hill_widget.py)                                    | [Hill cipher](https://en.wikipedia.org/wiki/Hill_cipher)                           |
|                    | [`vernam.py`](/app/crypto/symmetric/vernam.py)                         | [`vernam_widget.py`](/app/gui/symmetric/vernam/vernam_widget.py)                              | [Vernam cipher](https://en.wikipedia.org/wiki/One-time_pad)                        |
|                    | [`xor.py`](/app/crypto/symmetric/xor.py)                               | [`xor_widget.py`](/app/gui/symmetric/xor/xor_widget.py)                                       | [XOR cipher](https://en.wikipedia.org/wiki/XOR_cipher)                             |
|                    | [`des.py`](/app/crypto/symmetric/des.py)                               | [`des_widget.py`](/app/gui/symmetric/des/des_widget.py)                                       | [DES cipher](https://en.wikipedia.org/wiki/Data_Encryption_Standard)               |
|                    | [`gost.py`](/app/crypto/symmetric/gost.py)                             | [`gost_widget.py`](/app/gui/symmetric/gost/gost_widget.py)                                    | [GOST 28147-89](https://en.wikipedia.org/wiki/GOST_(block_cipher))                 |
| Asymmetric ciphers | ...                                                                    | ...                                                                                           | ...                                                                                |
| Crypto tools       | [`freqanalysis.py`](/app/crypto/tools/freqanalysis.py)                 | [`freqanalysis_widget.py`](/app/gui/cryptotools/freqanalysis/freqanalysis_widget.py)          | [Frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis)             |
|                    | [`index_of_coincidence.py`](/app/crypto/tools/index_of_coincidence.py) | [`ic_widget.py`](/app/gui/cryptotools/index_of_coincidence/ic_widget.py)                      | [Index of coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence)         |
|                    | [`autocorrelation.py`](/app/crypto/tools/autocorrelation.py)           | [`autocorrelation_widget.py`](/app/gui/cryptotools/autocorrelation/autocorrelation_widget.py) | [Автокорреляционный метод](https://ru.wikipedia.org/wiki/Автокорреляционный_метод) |
|                    | [`kasiski.py`](/app/crypto/tools/kasiski.py)                           | [`kasiski_widget.py`](/app/gui/cryptotools/kasiski/kasiski_widget.py)                         | [Kasiski examination](https://en.wikipedia.org/wiki/Kasiski_examination)           |
| PRNGs              | [`rc4.py`](/app/crypto/prngs/rc4.py)                                   |                                                                                               | [RC4](https://en.wikipedia.org/wiki/RC4)                                           |

## :gear: Dependencies

- `python-3.10+`
- `PyQt6`
- `numpy`
- `sympy`
- `pyqtgraph`
- `scipy`

## :hammer_and_wrench: Installation

To install the program, just run this script:

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/vasilypht/crypto-methods/main/install.sh)"
```

## :link: Attribution links

- <a href="https://www.flaticon.com/free-icons/cyber-security" title="cyber security icons">Cyber security icons created by Graphix's Art - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/telegram" title="telegram icons">Telegram icons created by Freepik - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/vk" title="VK icons">VK icons created by Fathema Khanom - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/github" title="github icons">Github icons created by Pixel perfect - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/paper" title="paper icons">Paper icons created by inipagistudio - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/files-and-folders" title="files and folders icons">Files and folders icons created by inipagistudio - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/more" title="more icons">More icons created by Freepik - Flaticon</a>
