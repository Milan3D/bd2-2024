-- Create
CREATE OR REPLACE PROCEDURE sp_Stockcomponentes_create(p_ID_ARMAZEM INT4, p_ID_COMPONENTE INT4, p_QUANTIDADE_STOCKCOMP INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO STOCKCOMPONENTES(ID_ARMAZEM, ID_COMPONENTE, QUANTIDADE_STOCKCOMP)
    VALUES (p_ID_ARMAZEM, p_ID_COMPONENTE, p_QUANTIDADE_STOCKCOMP);
    RAISE NOTICE 'Stock componente criado';
END;
$$;

-- Read
CREATE OR REPLACE PROCEDURE sp_Stockcomponentes_read(p_ID_ARMAZEM INT4, p_ID_COMPONENTE INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT QUANTIDADE_STOCKCOMP
    FROM STOCKCOMPONENTES
    WHERE ID_ARMAZEM = p_ID_ARMAZEM AND ID_COMPONENTE = p_ID_COMPONENTE;
END;
$$;

-- Update
CREATE OR REPLACE PROCEDURE sp_Stockcomponentes_update(p_ID_ARMAZEM INT4, p_ID_COMPONENTE INT4, p_QUANTIDADE_STOCKCOMP INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE STOCKCOMPONENTES
    SET QUANTIDADE_STOCKCOMP = p_QUANTIDADE_STOCKCOMP
    WHERE ID_ARMAZEM = p_ID_ARMAZEM AND ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Stock componente atualizado';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Stockcomponentes_delete(p_ID_ARMAZEM INT4, p_ID_COMPONENTE INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM STOCKCOMPONENTES
    WHERE ID_ARMAZEM = p_ID_ARMAZEM AND ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Stock componente eliminado';
END;
$$;

-- List
CREATE OR REPLACE PROCEDURE sp_Stockcomponentes_list()
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT ID_ARMAZEM, ID_COMPONENTE, QUANTIDADE_STOCKCOMP
    FROM STOCKCOMPONENTES;
END;
$$;
