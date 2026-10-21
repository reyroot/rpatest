AS-IS:

Recebe-se um arquivo CSV com os registros de solicitações. Em seguida, uma pessoa confere cada linha e separa os registros inválidos, anotando o motivo. Depois da conferência, lança no sistema apenas os registros válidos e, com esses lançamentos, elabora o relatório com o total financeiro dos registros aprovados.

TO-BE:

```mermaid
flowchart TD
    inicio([Chega o CSV]) --> arq{O arquivo abre?}
    arq -->|Não| parar([Stop: erro de sistema])
    arq -->|Sim| base{A base abre?}
    base -->|Não| parar
    base -->|Sim| linhas{Ainda há linhas?}
    linhas -->|Não| informe[Gerar relatório: totais e soma dos Aprovado por área]
    informe --> fim([Fim])
    linhas -->|Sim| campos{Campos obrigatórios vazios?}
    campos -->|Sim| rejCampo[Rejeitar: campo obrigatório vazio]
    campos -->|Não| data{Data inválida?}
    data -->|Sim| rejData[Rejeitar: data inválida]
    data -->|Não| valor{Valor inválido?}
    valor -->|Sim| rejValor[Rejeitar: valor inválido]
    valor -->|Não| sinal{Valor menor ou igual a zero?}
    sinal -->|Sim| rejSinal[Rejeitar: valor menor ou igual a zero]
    sinal -->|Não| status{Status diferente de Aprovado, Pendente ou Cancelado?}
    status -->|Sim| rejStatus[Rejeitar: status inválido]
    status -->|Não| dup{Já existe ocorrência válida deste id?}
    dup -->|Sim| rejDup[Rejeitar: identificador duplicado]
    dup -->|Não| gravar[Gravar na base]
    rejCampo --> linhas
    rejData --> linhas
    rejValor --> linhas
    rejSinal --> linhas
    rejStatus --> linhas
    rejDup --> linhas
    gravar --> linhas
```

Exceções de negócio: linha rejeitada, com o motivo, no arquivo de rejeições. O lote continua.

Exceção de sistema: o arquivo ou a base não abre. A execução para. Não se processam linhas.

Decisão: status fora de Aprovado, Pendente e Cancelado é rejeitado. Duplicado significa a segunda ocorrência válida do mesmo id, nesta execução ou já gravada na base. Só Aprovado entra na soma financeira. Pendente e Cancelado válidos são gravados e não entram nessa soma.



