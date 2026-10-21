create table if not exists solicitacoes(
    id_solicitacao text primary key,
    data text not null,
    area text not null,
    descricao text not null,
    valor numeric not null,
    status text not null
);



