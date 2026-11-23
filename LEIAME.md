# BIT-PUZZLE-EXCALIBUR

*[English version: README.md](README.md)*

Uma interface gráfica para montar e rodar **volantes** (grades de bytes) contra o desafio
público dos **puzzles de Bitcoin** — o front-end visual do motor `exlottery` do EXCALIBUR.

É um **front-end fino**: não contém nem copia o motor de busca. Ao iniciar, ele localiza a
GUI e o binário `exlottery` e os dirige. Um motor, uma GUI — sem código duplicado.

## O que faz

- Monta o volante clicando bytes numa grade 16×16 (primeiro byte + bytes compartilhados),
  com contador ao vivo, faixa legal por puzzle e importação/exportação de listas.
- **Aposta honesta, ao vivo:** ao escolher os bytes, mostra a **cobertura** (= a chance real
  de a chave estar no volante) e o **tempo de varredura** — os números que os "finders" de
  golpe escondem.
- **Roda pela GUI:** dispara a busca e acompanha progresso, taxa e o resultado verificado;
  **checkpoint/resume** sobrevive a pausa ou reboot.
- **Overlay histórico (honesto):** tinge a grade pela frequência de cada byte nas chaves
  **resolvidas** públicas — sai como ruído achatado, uma *prova visual* de que nenhum byte é
  mais quente — e revela os bytes de qualquer chave resolvida na grade. É prova, não dica.

## Arquitetura

```
BIT-PUZZLE-EXCALIBUR  (este pacote: launcher + empacotamento + docs)
        │  localiza em runtime
        ├── GUI    → EXCALIBUR-LOTTERY369/panel/app.py   (fonte única da interface)
        └── motor  → exlottery                            (projeto separado; o núcleo C++)
```

Nada é copiado: a GUI fica no repo dela e o motor continua um binário à parte. Assim há uma
fonte única pra cada um e se evita um fork que divergiria com o tempo.

## Instalar e rodar

Requisitos: Python 3.8+, Tk (`sudo apt install python3-tk`) e o motor `exlottery` compilado
no EXCALIBUR-LOTTERY369.

```bash
pip install -e .
bit-puzzle-excalibur
# ou, sem instalar:
PYTHONPATH=src python -m bit_puzzle_excalibur
```

O launcher acha o motor e a GUI sozinho. Se estiverem em outro lugar, aponte por variáveis:

```bash
export EXLOTTERY_BIN=/caminho/do/exlottery         # o binário do motor
export BITPUZZLE_PANEL=/caminho/do/LOTTERY369/panel # a pasta da GUI (tem o app.py)
```

Compile o motor se ainda não tiver:

```bash
cd ../EXCALIBUR-LOTTERY369
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j4
```

## Uso pretendido

Para o desafio público dos puzzles de Bitcoin e para estudar como uma busca em intervalo se
comporta — use apenas em chaves suas ou em alvos publicados para serem resolvidos. A leitura
de cobertura existe justamente para a aposta ser sempre honesta sobre a chance (ínfima).
**Não** é uma ferramenta para recuperar a carteira de outra pessoa, e nem poderia ser: chave
real é sorteio uniforme de 256 bits.

## Apoie

Trabalho de tempo livre, bancado por mim. O próximo passo grande — a versão GPU — precisa
de hardware. Se isto te for útil e quiser ajudar, doações em Bitcoin são bem-vindas, sem
promessa de retorno:

`bc1qhsq406jt6ghkzmhpnqe4r2s639t6mtrhj6zx03`

## Licença

[MIT](LICENSE) para este launcher. O motor e a GUI têm as licenças próprias deles.
