-- Função para listar todos os registros da tabela COMPONENTES
CREATE OR REPLACE FUNCTION fn_componentes_list()
RETURNS SETOF COMPONENTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_COMPONENTE,
        ID_CATCOMPONENTES,
        NOME_COMPONENTE,
        DESCRICAO_COMPONENTE,
        PRECOMEDIO_COMPONENTE
    FROM COMPONENTES;
END;
$$
LANGUAGE plpgsql;


-- Função para listar todos os registros da tabela ENCOMENDAS
CREATE OR REPLACE FUNCTION fn_encomendas_list()
RETURNS SETOF ENCOMENDAS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_ENCOMENDA,
        ID_GUIACOMPRAS,
        DATA_ENCOMENDA,
        ID_FUNCIONARIO
    FROM ENCOMENDAS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela FUNCIONARIOS
CREATE OR REPLACE FUNCTION fn_funcionarios_list()
RETURNS SETOF FUNCIONARIOS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_FUNCIONARIO,
        NOME,
        DATANASC,
        NIF,
        EMAIL,
        CONTACTO,
        MORADA,
        CARGO
    FROM FUNCIONARIOS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela ARMAZEM
CREATE OR REPLACE FUNCTION fn_armazem_list()
RETURNS SETOF ARMAZEM AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_ARMAZEM,
        NOME_ARMAZEM,
        MORADA_ARMAZEM,
        EMAIL_ARMAZEM,
        CONTACTO_ARMAZEM,
        ID_FUNCIONARIO
    FROM ARMAZEM;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela CATEGORIACOMPONENTES
CREATE OR REPLACE FUNCTION fn_categoriacomponentes_list()
RETURNS SETOF CATEGORIACOMPONENTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_CATCOMPONENTES,
        NOME_CATCOMPONENTES,
        DESCRICAO_CATCOMPONENTES
    FROM CATEGORIACOMPONENTES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela CLIENTES
CREATE OR REPLACE FUNCTION fn_clientes_list()
RETURNS SETOF CLIENTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_CLIENTE,
        NOME_CLIENTE,
        DATANASC_CLIENTE,
        MORADA_CLIENTE,
        NIF_CLIENTE,
        EMAIL_CLIENTE,
        CONTACTO_CLIENTE
    FROM CLIENTES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela GUIAREMESSACOMPRAS
CREATE OR REPLACE FUNCTION fn_guiaremessacompras_list()
RETURNS SETOF GUIAREMESSACOMPRAS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_GUIACOMPRAS,
        ID_ARMAZEM,
        DATA_GUIACOMPRAS,
        ID_FUNCIONARIO
    FROM GUIAREMESSACOMPRAS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela ENCOMENDAS_COMPONENTES
CREATE OR REPLACE FUNCTION fn_encomendas_componentes_list()
RETURNS SETOF ENCOMENDAS_COMPONENTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_ENCOMENDA,
        ID_COMPONENTE,
        QUANTIDADE_EC,
        PRECOUNIDADE_EC
    FROM ENCOMENDAS_COMPONENTES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela TIPOEQUIPAMENTOS
CREATE OR REPLACE FUNCTION fn_tipoequipamentos_list()
RETURNS SETOF TIPOEQUIPAMENTOS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_TIPOEQUIP,
        NOME_TIPOEQUIP,
        DESC_TIPOEQUIP
    FROM TIPOEQUIPAMENTOS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela MAODEOBRA
CREATE OR REPLACE FUNCTION fn_maodeobra_list()
RETURNS SETOF MAODEOBRA AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_MO,
        NOME_MO,
        DESC_MO,
        CUSTO_MO
    FROM MAODEOBRA;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela EQUIPAMENTOS
CREATE OR REPLACE FUNCTION fn_equipamentos_list()
RETURNS SETOF EQUIPAMENTOS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_EQUIP,
        ID_TIPOEQUIP,
        ID_MO,
        NOME_EQUIP,
        DESC_EQUIP,
        CUSTO_EQUIP
    FROM EQUIPAMENTOS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela GUIAREMESSAVENDAS
CREATE OR REPLACE FUNCTION fn_guiaremessavendas_list()
RETURNS SETOF GUIAREMESSAVENDAS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_GUIAVENDAS,
        ID_ARMAZEM,
        DATA_GUIAVENDAS,
        ID_FUNCIONARIO
    FROM GUIAREMESSAVENDAS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela FATURA
CREATE OR REPLACE FUNCTION fn_fatura_list()
RETURNS SETOF FATURA AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_FATURA,
        ID_GUIAVENDAS,
        ID_CLIENTE,
        PRECO_FATURA,
        DATA_FATURA
    FROM FATURA;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela EQUIPAMENTOS_FATURA
CREATE OR REPLACE FUNCTION fn_equipamentos_fatura_list()
RETURNS SETOF EQUIPAMENTOS_FATURA AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_FATURA,
        ID_EQUIP,
        QUANTIDADE_EQUIPFATURA
    FROM EQUIPAMENTOS_FATURA;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela FORNECEDORES
CREATE OR REPLACE FUNCTION fn_fornecedores_list()
RETURNS SETOF FORNECEDORES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_FORNECEDOR,
        NOME_FORNECEDOR,
        MORADA_FORNECEDOR,
        EMAIL_FORNECEDOR,
        CONTACTO_FORNECEDOR
    FROM FORNECEDORES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela FORNECEDORES_COMPONENTES
CREATE OR REPLACE FUNCTION fn_fornecedores_componentes_list()
RETURNS SETOF FORNECEDORES_COMPONENTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_COMPONENTE,
        ID_FORNECEDOR
    FROM FORNECEDORES_COMPONENTES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela RECEITAEQUIP
CREATE OR REPLACE FUNCTION fn_receitaequip_list()
RETURNS SETOF RECEITAEQUIP AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_EQUIP,
        ID_COMPONENTE,
        QUANTIDADE_RECEITA
    FROM RECEITAEQUIP;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela STOCKCOMPONENTES
CREATE OR REPLACE FUNCTION fn_stockcomponentes_list()
RETURNS SETOF STOCKCOMPONENTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_ARMAZEM,
        ID_COMPONENTE,
        QUANTIDADE_STOCKCOMP
    FROM STOCKCOMPONENTES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela STOCKEQUIPAMENTOS
CREATE OR REPLACE FUNCTION fn_stockequipamentos_list()
RETURNS SETOF STOCKEQUIPAMENTOS AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_ARMAZEM,
        ID_EQUIP,
        QUANTIDADE_STOCKEQUIP
    FROM STOCKEQUIPAMENTOS;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela PRODUCAO_DIARIA
CREATE OR REPLACE FUNCTION fn_producaodiaria_list()
RETURNS SETOF PRODUCAO_DIARIA AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_PRODUCAO,
        DATA_PRODUCAO,
        ID_ARMAZEM
    FROM PRODUCAO_DIARIA;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela LOTES
CREATE OR REPLACE FUNCTION fn_lotes_list()
RETURNS SETOF LOTES AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_LOTE,
        ID_PRODUCAO,
        ID_TIPOEQUIP,
        QUANTIDADE_PRODUTOS,
        ID_ARMAZEM,
        ID_FUNCIONARIO
    FROM LOTES;
END;
$$
LANGUAGE plpgsql;

-- Função para listar todos os registros da tabela NIVELACESSO_PGESTAO
CREATE OR REPLACE FUNCTION fn_nivelacesso_pgestao_list()
RETURNS SETOF NIVELACESSO_PGESTAO AS
$$
BEGIN
    RETURN QUERY SELECT 
        ID_NIVEL,
        NOME_NIVEL,
        DESC_NIVEL
    FROM NIVELACESSO_PGESTAO;
END;
$$
LANGUAGE plpgsql;