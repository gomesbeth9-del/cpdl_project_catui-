# CPDL Downloader para Edições de Catuí Côrte-Real Suarez

Este projeto contém um script Python para baixar todas as partituras e arquivos de áudio das edições de Catuí Côrte-Real Suarez disponíveis no Choral Public Domain Library (CPDL).

## Pré-requisitos

- Python 3.x
- Biblioteca `requests`

Você pode instalar a biblioteca `requests` com o seguinte comando:
```bash
pip install requests
```

## Como Usar

1.  **Clone ou baixe este projeto.**

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd cpdl-downloader
    ```

3.  **Execute o script de download:**
    ```bash
    python downloader.py
    ```

O script irá:
- Criar uma pasta chamada `musicas`.
- Dentro da pasta `musicas`, criar um subdiretório para cada obra musical.
- Baixar todos os arquivos disponíveis (PDF, MIDI, etc.) para o subdiretório correspondente.

O processo pode levar alguns minutos, dependendo da quantidade de obras e da sua conexão com a internet.

## Estrutura de Arquivos

Após a execução, a estrutura de pastas ficará assim:

```
cpdl-downloader/
├── musicas/
│   ├── Nome da Obra 1/
│   │   ├── arquivo1.pdf
│   │   └── arquivo2.mid
│   └── Nome da Obra 2/
│       ├── arquivo3.pdf
│       └── arquivo4.xml
├── downloader.py
└── README.md
