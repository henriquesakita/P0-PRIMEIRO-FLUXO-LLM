# Gerador de questões de múltipla escolha

Programa em Python que recebe um texto didático e pede a um modelo de linguagem (LLM) questões de múltipla escolha sobre ele, com alternativas, resposta correta e justificativa.

Este é o projeto **P0** do curso (primeiro fluxo com LLM). O que está aqui corresponde ao **nível Básico**.

## O problema

Professores do ensino médio gastam muito tempo preparando questões a partir do conteúdo que vão ensinar. Este programa faz o primeiro rascunho: o professor entrega um texto e recebe questões prontas para revisar.

Ele não substitui a revisão do professor. A ideia é encurtar o caminho entre "tenho o conteúdo" e "tenho questões para ajustar".

## Como funciona

1. Você passa o caminho de um arquivo `.txt` pelo terminal.
2. O programa lê o texto e envia ao LLM junto com instruções (o prompt está em `prompt.py`).
3. O modelo responde em JSON, e o programa imprime a resposta e verifica se ela é um JSON válido.

Cada questão vem neste formato:

```json
{
  "enunciado": "Qual é considerada a unidade básica da vida, segundo o texto?",
  "alternativas": {"A": "Tecido", "B": "Célula", "C": "Órgão", "D": "Organismo"},
  "resposta_correta": "B",
  "justificativa": "O texto afirma explicitamente: 'A célula é a unidade básica da vida'."
}
```

## Provedor e modelo

- **Provedor:** NVIDIA, pela API gratuita do [build.nvidia.com](https://build.nvidia.com), sem custo e sem cartão de crédito.
- **Modelo:** `nvidia/nemotron-3-ultra-550b-a55b`.
- **Biblioteca:** `openai`. A API da NVIDIA segue o mesmo formato da OpenAI, então basta trocar o endereço (`base_url`).
- **Por que não o LLM institucional:** ele estava com problemas durante o desenvolvimento, então usei uma alternativa gratuita.

Parâmetros usados na chamada:

| Parâmetro | Valor | Por quê |
|---|---|---|
| `temperature` | 0.3 | Baixa, para respostas mais estáveis e fiéis ao texto |
| `max_tokens` | 3000 | Este modelo gasta tokens raciocinando antes de responder. Com um limite pequeno, o JSON sai cortado |

## Como obter a chave de API

1. Crie uma conta em [build.nvidia.com](https://build.nvidia.com).
2. Abra a página **API Keys** e clique em **Generate API Key**.
3. Copie o valor na hora, porque ele só aparece uma vez.

A chave é pessoal. Não a compartilhe e não a coloque no código.

## Instalação

Precisa de Python 3 (desenvolvido com 3.12).

```bash
git clone https://github.com/henriquesakita/P0-PRIMEIRO-FLUXO-LLM.git
cd P0-PRIMEIRO-FLUXO-LLM

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows, o comando de ativação é `.venv\Scripts\activate`.

## Configuração

Crie um arquivo chamado `.env` na raiz do projeto com três linhas:

```
NVIDIA_API_KEY=sua_chave_aqui
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL_NAME=nvidia/nemotron-3-ultra-550b-a55b
```

Sem espaços em volta do `=` e sem aspas. O `.env` está no `.gitignore`, então não vai para o repositório.

Se alguma dessas variáveis faltar, o programa avisa qual é e para antes de chamar a API.

## Como rodar

```bash
python main.py exemplos/texto1_biologia.txt
```

A saída mostra o `finish_reason` (`stop` quer dizer que a resposta terminou normalmente), o JSON bruto e o resultado da validação.

Há três textos de exemplo na pasta `exemplos/` (biologia, ciências e física). Foram escritos por mim para este projeto, então não há conteúdo de terceiros nem dados de alunos.

## Erros tratados

- Variável do `.env` ausente ou vazia.
- Arquivo de entrada não informado.
- Arquivo de entrada inexistente.
- Resposta do modelo que não é JSON válido (o programa avisa em vez de quebrar).

## O que observei nos testes

Testei com os três textos de exemplo. O formato saiu correto em todos: JSON válido, 3 questões, 4 alternativas cada, resposta marcada certa. Mas alguns pontos pedem atenção:

- **O resultado muda a cada execução.** Com o mesmo texto e o mesmo prompt, as questões saem diferentes.
- **Distratores fracos.** Algumas alternativas erradas são óbvias (por exemplo, as que usam "toda a água..." ou "nenhuma das duas...").
- **A resposta certa costuma ser a mais longa.** Isso entrega o gabarito pelo formato.
- **Erros pontuais de idioma.** Em um teste apareceu uma palavra em inglês no meio de uma alternativa em português.
- **O modelo não verifica fatos por conta própria.** Ele usa o texto que recebe, e o prompt manda usar só esse texto, mas a conferência final é do professor.

Uma dica de quem tropeçou nisso: ao copiar a saída direto da tela do terminal, alguns espaços entre palavras somem por causa da quebra de linha. O arquivo gerado está correto. Para ler a saída com segurança, redirecione para um arquivo (`python main.py exemplos/texto1_biologia.txt > saida.txt`).

Conclusão: o programa serve como rascunho, e as questões devem ser revisadas antes de qualquer uso em sala.

## Estrutura do projeto

```
.
├── main.py            # programa principal
├── prompt.py          # instruções enviadas ao modelo
├── requirements.txt   # dependências
├── exemplos/          # textos de exemplo
├── .gitignore
└── README.md
```

## Próximos passos

Nos próximos níveis do projeto pretendo organizar o código em módulos, validar a estrutura de cada questão (4 alternativas, resposta válida) com nova tentativa em caso de falha, e escrever testes automatizados.

## Autor

Henrique Sakita
