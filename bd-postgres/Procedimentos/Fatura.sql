-- Create
CREATE OR REPLACE PROCEDURE sp_Fatura_create(p_ID_GUIAVENDAS INT4, p_ID_CLIENTE INT4, p_PRECO_FATURA DECIMAL(10,2), p_DATA_FATURA DATE)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO FATURA(ID_GUIAVENDAS, ID_CLIENTE, PRECO_FATURA, DATA_FATURA)
    VALUES (p_ID_GUIAVENDAS, p_ID_CLIENTE, p_PRECO_FATURA, p_DATA_FATURA);
    RAISE NOTICE 'Fatura criada';
END;
$$;

-- Read
CREATE OR REPLACE PROCEDURE sp_Fatura_read(p_ID_FATURA INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT ID_GUIAVENDAS, ID_CLIENTE, PRECO_FATURA, DATA_FATURA
    FROM FATURA
    WHERE ID_FATURA = p_ID_FATURA;
END;
$$;

-- Update
CREATE OR REPLACE PROCEDURE sp_Fatura_update(p_ID_FATURA INT4, p_ID_GUIAVENDAS INT4, p_ID_CLIENTE INT4, p_PRECO_FATURA DECIMAL(10,2), p_DATA_FATURA DATE)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE FATURA
    SET ID_GUIAVENDAS = p_ID_GUIAVENDAS, ID_CLIENTE = p_ID_CLIENTE, PRECO_FATURA = p_PRECO_FATURA, DATA_FATURA = p_DATA_FATURA
    WHERE ID_FATURA = p_ID_FATURA;
    RAISE NOTICE 'Fatura atualizada';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Fatura_delete(p_ID_FATURA INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM FATURA
    WHERE ID_FATURA = p_ID_FATURA;
    RAISE NOTICE 'Fatura eliminada';
END;
$$;

-- List
CREATE OR REPLACE PROCEDURE sp_Fatura_list()
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT ID_GUIAVENDAS, ID_CLIENTE, PRECO_FATURA, DATA_FATURA
    FROM FATURA;
END;
$$;
