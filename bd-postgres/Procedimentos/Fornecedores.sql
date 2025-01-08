-- Create
CREATE OR REPLACE PROCEDURE sp_Fornecedores_create(p_NOME_FORNECEDOR TEXT, p_MORADA_FORNECEDOR TEXT, p_EMAIL_FORNECEDOR TEXT, p_CONTACTO_FORNECEDOR NUMERIC(9))
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO FORNECEDORES(NOME_FORNECEDOR, MORADA_FORNECEDOR, EMAIL_FORNECEDOR, CONTACTO_FORNECEDOR)
    VALUES (p_NOME_FORNECEDOR, p_MORADA_FORNECEDOR, p_EMAIL_FORNECEDOR, p_CONTACTO_FORNECEDOR);
    RAISE NOTICE 'Fornecedor criado';
END;
$$;

-- Read
CREATE OR REPLACE PROCEDURE sp_Fornecedores_read(p_ID_FORNECEDOR INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT NOME_FORNECEDOR, MORADA_FORNECEDOR, EMAIL_FORNECEDOR, CONTACTO_FORNECEDOR
    FROM FORNECEDORES
    WHERE ID_FORNECEDOR = p_ID_FORNECEDOR;
END;
$$;

-- Update
CREATE OR REPLACE PROCEDURE sp_Fornecedores_update(p_ID_FORNECEDOR INT4, p_NOME_FORNECEDOR TEXT, p_MORADA_FORNECEDOR TEXT, p_EMAIL_FORNECEDOR TEXT, p_CONTACTO_FORNECEDOR NUMERIC(9))
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE FORNECEDORES
    SET NOME_FORNECEDOR = p_NOME_FORNECEDOR, MORADA_FORNECEDOR = p_MORADA_FORNECEDOR, EMAIL_FORNECEDOR = p_EMAIL_FORNECEDOR, CONTACTO_FORNECEDOR = p_CONTACTO_FORNECEDOR
    WHERE ID_FORNECEDOR = p_ID_FORNECEDOR;
    RAISE NOTICE 'Fornecedor atualizado';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Fornecedores_delete(p_ID_FORNECEDOR INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM FORNECEDORES
    WHERE ID_FORNECEDOR = p_ID_FORNECEDOR;
    RAISE NOTICE 'Fornecedor eliminado';
END;
$$;

