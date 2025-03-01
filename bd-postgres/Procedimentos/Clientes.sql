-- Create
CREATE OR REPLACE PROCEDURE sp_Clientes_create(p_NOME_CLIENTE TEXT, p_DATANASC_CLIENTE DATE, p_MORADA_CLIENTE TEXT, p_NIF_CLIENTE INT4, p_EMAIL_CLIENTE TEXT, p_CONTACTO_CLIENTE NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO CLIENTES(NOME_CLIENTE, DATANASC_CLIENTE, MORADA_CLIENTE, NIF_CLIENTE, EMAIL_CLIENTE, CONTACTO_CLIENTE)
    VALUES (p_NOME_CLIENTE, p_DATANASC_CLIENTE, p_MORADA_CLIENTE, p_NIF_CLIENTE, p_EMAIL_CLIENTE, p_CONTACTO_CLIENTE);
    RAISE NOTICE 'Cliente criado';
END;
$$;


-- Update
CREATE OR REPLACE PROCEDURE sp_Clientes_update(p_ID_CLIENTE INTEGER, p_NOME_CLIENTE TEXT, p_DATANASC_CLIENTE DATE, p_MORADA_CLIENTE TEXT, p_NIF_CLIENTE INT4, p_EMAIL_CLIENTE TEXT, p_CONTACTO_CLIENTE NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE CLIENTES
    SET NOME_CLIENTE = p_NOME_CLIENTE, DATANASC_CLIENTE = p_DATANASC_CLIENTE, MORADA_CLIENTE = p_MORADA_CLIENTE, NIF_CLIENTE = p_NIF_CLIENTE, EMAIL_CLIENTE = p_EMAIL_CLIENTE, CONTACTO_CLIENTE = p_CONTACTO_CLIENTE
    WHERE ID_CLIENTE = p_ID_CLIENTE;
    RAISE NOTICE 'Cliente atualizado';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Clientes_delete(p_ID_CLIENTE INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM CLIENTES
    WHERE ID_CLIENTE = p_ID_CLIENTE;
    RAISE NOTICE 'Cliente eliminado';
END;
$$;

