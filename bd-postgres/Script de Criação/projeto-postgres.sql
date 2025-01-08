/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/*==============================================================*/

DROP TABLE IF EXISTS EQUIPAMENTOS_FATURA;
DROP TABLE IF EXISTS ENCOMENDAS_COMPONENTES;
DROP TABLE IF EXISTS FORNECEDORES_COMPONENTES;
DROP TABLE IF EXISTS RECEITAEQUIP;
DROP TABLE IF EXISTS STOCKCOMPONENTES;
DROP TABLE IF EXISTS STOCKEQUIPAMENTOS;
DROP TABLE IF EXISTS LOTES;
DROP TABLE IF EXISTS ENCOMENDAS;
DROP TABLE IF EXISTS FATURA;
DROP TABLE IF EXISTS GUIAREMESSACOMPRAS;
DROP TABLE IF EXISTS GUIAREMESSAVENDAS;
DROP TABLE IF EXISTS PRODUCAO_DIARIA;
DROP TABLE IF EXISTS EQUIPAMENTOS;
DROP TABLE IF EXISTS COMPONENTES;
DROP TABLE IF EXISTS CATEGORIACOMPONENTES;
DROP TABLE IF EXISTS TIPOEQUIPAMENTOS;
DROP TABLE IF EXISTS MAODEOBRA;
DROP TABLE IF EXISTS CLIENTES;
DROP TABLE IF EXISTS FORNECEDORES;
DROP TABLE IF EXISTS ARMAZEM;
DROP TABLE IF EXISTS ACESSO_PGESTAO;
DROP TABLE IF EXISTS NIVELACESSO_PGESTAO;
DROP TABLE IF EXISTS FUNCIONARIOS;

/*==============================================================*/
/* Table: FUNCIONARIOS                                          */
/*==============================================================*/
create table FUNCIONARIOS (
   ID_FUNCIONARIO       SERIAL               not null,
   NOME                 TEXT                 not null,
   DATANASC             DATE                 not null,
   NIF                  INT4                 not null unique,
   EMAIL                TEXT                 not null,
   CONTACTO             NUMERIC(9)           not null,
   MORADA               TEXT                 not null,
   CARGO                TEXT                 null,
   constraint PK_FUNCIONARIOS primary key (ID_FUNCIONARIO)
);

/*==============================================================*/
/* Table: ARMAZEM                                               */
/*==============================================================*/
create table ARMAZEM (
   ID_ARMAZEM           SERIAL               not null,
   NOME_ARMAZEM         TEXT                 not null,
   MORADA_ARMAZEM       TEXT                 not null,
   EMAIL_ARMAZEM        TEXT                 not null,
   CONTACTO_ARMAZEM     NUMERIC(9)           not null,
   ID_FUNCIONARIO       INT4                 not null,
   constraint PK_ARMAZEM primary key (ID_ARMAZEM),
   constraint FK_ARMAZEM_FUNCIONARIO foreign key (ID_FUNCIONARIO)
      references FUNCIONARIOS (ID_FUNCIONARIO)
      on delete restrict on update cascade
);

/*==============================================================*/
/* Table: CATEGORIACOMPONENTES                                  */
/*==============================================================*/
create table CATEGORIACOMPONENTES (
   ID_CATCOMPONENTES    SERIAL               not null,
   NOME_CATCOMPONENTES  TEXT                 not null,
   DESCRICAO_CATCOMPONENTES TEXT                 null,
   constraint PK_CATEGORIACOMPONENTES primary key (ID_CATCOMPONENTES)
);

/*==============================================================*/
/* Table: CLIENTES                                              */
/*==============================================================*/
create table CLIENTES (
   ID_CLIENTE           SERIAL               not null,
   NOME_CLIENTE         TEXT                 not null,
   DATANASC_CLIENTE     DATE                 not null,
   MORADA_CLIENTE       TEXT                 not null,
   NIF_CLIENTE          INT4                 not null,
   EMAIL_CLIENTE        TEXT                 not null,
   CONTACTO_CLIENTE     NUMERIC(9)           not null,
   constraint PK_CLIENTES primary key (ID_CLIENTE)
);

/*==============================================================*/
/* Table: COMPONENTES                                           */
/*==============================================================*/
create table COMPONENTES (
   ID_COMPONENTE        SERIAL               not null,
   ID_CATCOMPONENTES    INT4                 not null,
   NOME_COMPONENTE      TEXT                 not null,
   DESCRICAO_COMPONENTE TEXT                 null,
   PRECOMEDIO_COMPONENTE DECIMAL(10,2)        null,
   constraint PK_COMPONENTES primary key (ID_COMPONENTE),
   constraint FK_COMPONEN_ASSOCIACA_CATEGORI foreign key (ID_CATCOMPONENTES)
      references CATEGORIACOMPONENTES (ID_CATCOMPONENTES)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: GUIAREMESSACOMPRAS                                    */
/*==============================================================*/
create table GUIAREMESSACOMPRAS (
   ID_GUIACOMPRAS       SERIAL               not null,
   ID_ARMAZEM           INT4                 not null,
   DATA_GUIACOMPRAS     DATE                 not null,
   ID_FUNCIONARIO       INT4                 not null,
   constraint PK_GUIAREMESSACOMPRAS primary key (ID_GUIACOMPRAS),
   constraint FK_GUIAREME_ASSOCIACA_ARMAZEM foreign key (ID_ARMAZEM)
      references ARMAZEM (ID_ARMAZEM)
      on delete restrict on update restrict,
   constraint FK_GUIAREME_ASSOCIACA_FUNCIONARIO foreign key (ID_FUNCIONARIO)
      references FUNCIONARIOS (ID_FUNCIONARIO)
      on delete restrict on update cascade
);

/*==============================================================*/
/* Table: ENCOMENDAS                                            */
/*==============================================================*/
create table ENCOMENDAS (
   ID_ENCOMENDA         SERIAL               not null,
   ID_GUIACOMPRAS       INT4                 not null,
   DATA_ENCOMENDA       DATE                 not null,
   ID_FUNCIONARIO       INT4                 not null,
   constraint PK_ENCOMENDAS primary key (ID_ENCOMENDA),
   constraint FK_ENCOMEND_ASSOCIACO_GUIAREME foreign key (ID_GUIACOMPRAS)
      references GUIAREMESSACOMPRAS (ID_GUIACOMPRAS)
      on delete restrict on update restrict,
   constraint FK_ENCOMEND_ASSOCIACO_FUNCIONARIO foreign key (ID_FUNCIONARIO)
      references FUNCIONARIOS (ID_FUNCIONARIO)
      on delete restrict on update cascade
);

/*==============================================================*/
/* Table: ENCOMENDAS_COMPONENTES                                */
/*==============================================================*/
create table ENCOMENDAS_COMPONENTES (
   ID_ENCOMENDA         INT4                 not null,
   ID_COMPONENTE        INT4                 not null,
   QUANTIDADE_EC        INT4                 not null,
   PRECOUNIDADE_EC      DECIMAL(10,2)        not null,
   constraint PK_ENCOMENDAS_COMPONENTES primary key (ID_ENCOMENDA, ID_COMPONENTE),
   constraint FK_ENCOMEND_ASSOCIACA_ENCOMEND foreign key (ID_ENCOMENDA)
      references ENCOMENDAS (ID_ENCOMENDA)
      on delete restrict on update restrict,
   constraint FK_ENCOMEND_ASSOCIACA_COMPONEN foreign key (ID_COMPONENTE)
      references COMPONENTES (ID_COMPONENTE)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: TIPOEQUIPAMENTOS                                      */
/*==============================================================*/
create table TIPOEQUIPAMENTOS (
   ID_TIPOEQUIP         SERIAL               not null,
   NOME_TIPOEQUIP       TEXT                 not null,
   DESC_TIPOEQUIP       TEXT                 null,
   constraint PK_TIPOEQUIPAMENTOS primary key (ID_TIPOEQUIP)
);

/*==============================================================*/
/* Table: MAODEOBRA                                             */
/*==============================================================*/
create table MAODEOBRA (
   ID_MO                SERIAL               not null,
   NOME_MO              TEXT                 not null,
   DESC_MO              TEXT                 null,
   CUSTO_MO             DECIMAL(10,2)        not null,
   constraint PK_MAODEOBRA primary key (ID_MO)
);

/*==============================================================*/
/* Table: EQUIPAMENTOS                                          */
/*==============================================================*/
create table EQUIPAMENTOS (
   ID_EQUIP             SERIAL               not null,
   ID_TIPOEQUIP         INT4                 not null,
   ID_MO                INT4                 null,
   NOME_EQUIP           TEXT                 not null,
   DESC_EQUIP           TEXT                 null,
   CUSTO_EQUIP          DECIMAL(10,2)        not null,
   constraint PK_EQUIPAMENTOS primary key (ID_EQUIP),
   constraint FK_EQUIPAME_ASSOCIACA_TIPOEQUI foreign key (ID_TIPOEQUIP)
      references TIPOEQUIPAMENTOS (ID_TIPOEQUIP)
      on delete restrict on update restrict,
   constraint FK_EQUIPAME_ASSOCIACA_MAODEOBR foreign key (ID_MO)
      references MAODEOBRA (ID_MO)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: GUIAREMESSAVENDAS                                     */
/*==============================================================*/
create table GUIAREMESSAVENDAS (
   ID_GUIAVENDAS        SERIAL               not null,
   ID_ARMAZEM           INT4                 not null,
   DATA_GUIAVENDAS      DATE                 not null,
   ID_FUNCIONARIO       INT4                 not null,
   constraint PK_GUIAREMESSAVENDAS primary key (ID_GUIAVENDAS),
   constraint FK_GUIAREME_ASSOCIACA_ARMAZEM foreign key (ID_ARMAZEM)
      references ARMAZEM (ID_ARMAZEM)
      on delete restrict on update restrict,
   constraint FK_GUIAREME_ASSOCIACA_FUNCIONARIO foreign key (ID_FUNCIONARIO)
      references FUNCIONARIOS (ID_FUNCIONARIO)
      on delete restrict on update cascade
);

/*==============================================================*/
/* Table: FATURA                                                */
/*==============================================================*/
create table FATURA (
   ID_FATURA            SERIAL               not null,
   ID_GUIAVENDAS        INT4                 null,
   ID_CLIENTE           INT4                 not null,
   PRECO_FATURA         DECIMAL(10,2)        not null,
   DATA_FATURA          DATE                 not null,
   constraint PK_FATURA primary key (ID_FATURA),
   constraint FK_FATURA_ASSOCIACA_GUIAREME foreign key (ID_GUIAVENDAS)
      references GUIAREMESSAVENDAS (ID_GUIAVENDAS)
      on delete restrict on update restrict,
   constraint FK_FATURA_ASSOCIACA_CLIENTES foreign key (ID_CLIENTE)
      references CLIENTES (ID_CLIENTE)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: EQUIPAMENTOS_FATURA                                   */
/*==============================================================*/
create table EQUIPAMENTOS_FATURA (
   ID_FATURA            INT4                 not null,
   ID_EQUIP             INT4                 not null,
   QUANTIDADE_EQUIPFATURA INT4                 not null,
   constraint PK_EQUIPAMENTOS_FATURA primary key (ID_FATURA, ID_EQUIP),
   constraint FK_EQUIPAME_ASSOCIACA_FATURA foreign key (ID_FATURA)
      references FATURA (ID_FATURA)
      on delete restrict on update restrict,
   constraint FK_EQUIPAME_ASSOCIACA_EQUIPAME foreign key (ID_EQUIP)
      references EQUIPAMENTOS (ID_EQUIP)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: FORNECEDORES                                          */
/*==============================================================*/
create table FORNECEDORES (
   ID_FORNECEDOR        SERIAL               not null,
   NOME_FORNECEDOR      TEXT                 not null,
   MORADA_FORNECEDOR    TEXT                 not null,
   EMAIL_FORNECEDOR     TEXT                 not null,
   CONTACTO_FORNECEDOR  NUMERIC(9)           not null,
   constraint PK_FORNECEDORES primary key (ID_FORNECEDOR)
);

/*==============================================================*/
/* Table: FORNECEDORES_COMPONENTES                              */
/*==============================================================*/
create table FORNECEDORES_COMPONENTES (
   ID_COMPONENTE        INT4                 not null,
   ID_FORNECEDOR        INT4                 not null,
   constraint PK_FORNECEDORES_COMPONENTES primary key (ID_COMPONENTE, ID_FORNECEDOR),
   constraint FK_FORNECED_ASSOCIACA_COMPONEN foreign key (ID_COMPONENTE)
      references COMPONENTES (ID_COMPONENTE)
      on delete restrict on update restrict,
   constraint FK_FORNECED_ASSOCIACA_FORNECED foreign key (ID_FORNECEDOR)
      references FORNECEDORES (ID_FORNECEDOR)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: RECEITAEQUIP                                          */
/*==============================================================*/
create table RECEITAEQUIP (
   ID_EQUIP             INT4                 not null,
   ID_COMPONENTE        INT4                 not null,
   QUANTIDADE_RECEITA   INT4                 not null,
   constraint PK_RECEITAEQUIP primary key (ID_EQUIP, ID_COMPONENTE),
   constraint FK_RECEITAE_ASSOCIACA_EQUIPAME foreign key (ID_EQUIP)
      references EQUIPAMENTOS (ID_EQUIP)
      on delete restrict on update restrict,
   constraint FK_RECEITAE_ASSOCIACA_COMPONEN foreign key (ID_COMPONENTE)
      references COMPONENTES (ID_COMPONENTE)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: STOCKCOMPONENTES                                      */
/*==============================================================*/
create table STOCKCOMPONENTES (
   ID_ARMAZEM           INT4                 not null,
   ID_COMPONENTE        INT4                 not null,
   QUANTIDADE_STOCKCOMP INT4                 not null,
   constraint PK_STOCKCOMPONENTES primary key (ID_ARMAZEM, ID_COMPONENTE),
   constraint FK_STOCKCOM_ASSOCIACA_ARMAZEM foreign key (ID_ARMAZEM)
      references ARMAZEM (ID_ARMAZEM)
      on delete restrict on update restrict,
   constraint FK_STOCKCOM_ASSOCIACA_COMPONEN foreign key (ID_COMPONENTE)
      references COMPONENTES (ID_COMPONENTE)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: STOCKEQUIPAMENTOS                                     */
/*==============================================================*/
create table STOCKEQUIPAMENTOS (
   ID_ARMAZEM           INT4                 not null,
   ID_EQUIP             INT4                 not null,
   QUANTIDADE_STOCKEQUIP INT4                 not null,
   constraint PK_STOCKEQUIPAMENTOS primary key (ID_ARMAZEM, ID_EQUIP),
   constraint FK_STOCKEQU_ASSOCIACA_ARMAZEM foreign key (ID_ARMAZEM)
      references ARMAZEM (ID_ARMAZEM)
      on delete restrict on update restrict,
   constraint FK_STOCKEQU_ASSOCIACA_EQUIPAME foreign key (ID_EQUIP)
      references EQUIPAMENTOS (ID_EQUIP)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: PRODUCAO_DIARIA                                       */
/*==============================================================*/
create table PRODUCAO_DIARIA (
   ID_PRODUCAO          SERIAL               not null,
   DATA_PRODUCAO        DATE                 not null,
   ID_ARMAZEM           INT4                 not null,
   constraint PK_PRODUCAO_DIARIA primary key (ID_PRODUCAO),
   constraint FK_PRODUCAO_DIARIA_ARMAZEM foreign key (ID_ARMAZEM)
      references ARMAZEM (ID_ARMAZEM)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: LOTES                                                 */
/*==============================================================*/
create table LOTES (
   ID_LOTE              SERIAL               not null,
   ID_PRODUCAO          INT4                 not null,
   ID_TIPOEQUIP         INT4                 not null,
   QUANTIDADE_PRODUTOS  INT4                 not null,
   ID_ARMAZEM           INT4                 not null,
   ID_FUNCIONARIO       INT4                 not null,
   constraint PK_LOTES primary key (ID_LOTE),
   constraint FK_LOTES_PRODUCAO_DIARIA foreign key (ID_PRODUCAO)
      references PRODUCAO_DIARIA (ID_PRODUCAO)
      on delete restrict on update restrict,
   constraint FK_LOTES_TIPOEQUIP foreign key (ID_TIPOEQUIP)
      references TIPOEQUIPAMENTOS (ID_TIPOEQUIP)
      on delete restrict on update restrict,
   constraint FK_LOTES_ARMAZEM foreign key (ID_ARMAZEM)
      references ARMAZEM (ID_ARMAZEM)
      on delete restrict on update restrict,
   constraint FK_LOTES_FUNCIONARIO foreign key (ID_FUNCIONARIO)
      references FUNCIONARIOS (ID_FUNCIONARIO)
      on delete restrict on update restrict
);

/*==============================================================*/
/* Table: NIVELACESSO_PGESTAO                                   */
/*==============================================================*/
create table NIVELACESSO_PGESTAO (
   ID_NIVEL             SERIAL               not null,
   NOME_NIVEL           TEXT                 not null,
   DESC_NIVEL           TEXT                 null,
   constraint PK_NIVELACESSO_PGESTAO primary key (ID_NIVEL)
);

/*==============================================================*/
/* Table: ACESSO_PGESTAO                                        */
/*==============================================================*/
create table ACESSO_PGESTAO (
   ID_UTILPGESTAO       SERIAL               not null,
   ID_FUNCIONARIO       INT4                 not null,
   ID_NIVEL             INT4                 not null,
   PASSWORD_PGESTAO     TEXT                 not null,
   constraint PK_ACESSO_PGESTAO primary key (ID_UTILPGESTAO),
   constraint FK_ACESSO_PGESTAO_FUNCIONARIO foreign key (ID_FUNCIONARIO)
      references FUNCIONARIOS (ID_FUNCIONARIO)
      on delete cascade on update cascade,
   constraint FK_ACESSO_PGESTAO_NIVEL foreign key (ID_NIVEL)
      references NIVELACESSO_PGESTAO (ID_NIVEL)
      on delete cascade on update cascade
);
