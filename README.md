# Automação de solicitações

## Instalação

Na pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

O processo usa apenas a biblioteca padrão. O `requirements.txt` existe para o pytest. A pasta `.venv` não entra no repositório.

## Execução

Coloque o arquivo em `input/solicitacoes.csv`. Na pasta do projeto, não dentro de `src`:

```bash
python3 src/main.py
```

O ambiente virtual não é necessário para essa execução. Ao terminar, a pasta `output` contém `solicitacoes.db`, `rejeitados.csv`, `relatorio.csv` e o log do dia.

## Testes

Com o ambiente ativado:

```bash
python3 -m pytest tests/test_validator.py
```

Há três testes do validador: uma linha válida (`350,00` vira `350.0`), um valor `abc` e uma área vazia. Para a reexecução, rode `python3 src/main.py` duas vezes. A tabela permanece com 8 linhas, porque a chave primária recusa o mesmo `id_solicitacao`.

## Exemplo de log

```text
2026-10-20 23:17:49,979 INFO Inicio
2026-10-20 23:17:49,993 INFO Solicitacao SOL-001 gravada
2026-10-20 23:17:50,002 ERROR SOL-005: O campo valor tem um valor menor ou igual que 0
2026-10-20 23:17:50,008 ERROR SOL-008: O campo valor deve ser um numero valido
2026-10-20 23:17:50,011 INFO Solicitacao SOL-009 gravada
2026-10-20 23:17:50,011 ERROR SOL-009: Identificador duplicado
2026-10-20 23:17:50,011 ERROR SOL-010: O campo area, esta vazio
2026-10-20 23:17:50,015 INFO Fim. lidos=12, validos=8, rejeitados=4, aprovados=5, pendentes=2, cancelados=1, soma_por_area={'Peças': 3200.0, 'Vendas': 270.0}
```

## Perguntas

### Como garantir que a automação não lance o mesmo registro duas vezes?

`id_solicitacao` é a chave primária da tabela. Se o identificador já existe, o SQLite recusa o `INSERT` e `insert_row` devolve "Identificador duplicado". O `main.py` anota essa linha no arquivo de rejeições e segue com as demais. A base não cresce. Na segunda execução do mesmo arquivo, os ids já gravados caem nesse mesmo caso.

### Como diferenciar erro de dado e erro de infraestrutura?

Erro de dado é uma linha que não cumpre a regra de negócio: valor `abc`, área vazia, valor menor ou igual a zero, data inválida ou status fora da lista. O robô grava o motivo e continua o lote.

Erro de infraestrutura é o ambiente que impede o trabalho: o CSV não abre ou a base não abre. Não há linhas para processar. O `main.py` registra o erro e encerra a execução.

### Quando usar API em vez de automação por interface (RPA)?

Uso API quando o outro sistema oferece uma porta para programas, em geral HTTP com JSON. Automatizo a tela quando a única porta é a que uma pessoa usa: botões, formulários e HTML.

### Como proteger credenciais para acessar um sistema real?

As credenciais ficam em variáveis de ambiente, nunca no código. O arquivo `.env` não entra no repositório. O log não escreve a senha.

### Que indicadores monitorar em produção?

- Se a execução terminou ou parou ao abrir o arquivo ou a base.
- Quantos registros foram lidos, gravados e rejeitados.
- Quantos duplicados apareceram.
- A soma dos valores aprovados.
- Quanto tempo durou a execução.
- O horário da última execução que terminou bem.

Se os rejeitados disparam, o arquivo de origem mudou. Se não houve execução na hora prevista, a agenda falhou.

## Evolução: portal web, indisponibilidade e agenda

Para capturar dados de um portal, primeiro verifico se existe API ou download de arquivo. Se existir, uso essa porta. O CSV desta prova já é esse caso. A ferramenta de RPA que simula o clique da pessoa entra só quando a única porta é a tela.

Se o sistema estiver indisponível, isso é erro de infraestrutura. Programo reintentos com espera entre eles, por exemplo três tentativas. Um valor inválido não se tenta de novo. Se o portal continuar fora, a execução para, o log registra a falha e um mecanismo de observabilidade avisa.

A execução diária fica no cron do sistema operacional: dispara, processa e termina. Um processo vivo o tempo todo serve para escutar uma fila, não para um arquivo que chega uma vez por dia.

## Uso de IA

A IA ajudou a montar o diagrama de fluxo em Mermaid a partir do roteiro do processo. Ajudou a redigir este README. Fez o esqueleto dos testes. Os `assert` foram escritos por mim. Ajudou a entender os fundamentos de RPA e o funcionamento de alguns métodos, e também na criação de arquivos CSV de teste.

O código da automação foi escrito à mão, da forma tradicional. A IA serviu como um Stack Overflow avançado: explicou, revisou e apontou erros. As decisões e o código final são meus.
