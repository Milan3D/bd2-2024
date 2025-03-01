-- Create
CREATE OR REPLACE PROCEDURE sp_Encomendas_componentes_create(p_ID_ENCOMENDA INT4, p_ID_COMPONENTE INT4, p_QUANTIDADE_EC INT4, p_PRECOUNIDADE_EC DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO ENCOMENDAS_COMPONENTES(ID_ENCOMENDA, ID_COMPONENTE, QUANTIDADE_EC, PRECOUNIDADE_EC)
    VALUES (p_ID_ENCOMENDA, p_ID_COMPONENTE, p_QUANTIDADE_EC, p_PRECOUNIDADE_EC);
    RAISE NOTICE 'Encomenda de componentes criada';
END;
$$;



-- Update
CREATE OR REPLACE PROCEDURE sp_Encomendas_componentes_update(p_ID_ENCOMENDA INTEGER, p_ID_COMPONENTE INTEGER, p_QUANTIDADE_EC INT4, p_PRECOUNIDADE_EC DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE ENCOMENDAS_COMPONENTES
    SET QUANTIDADE_EC = p_QUANTIDADE_EC, PRECOUNIDADE_EC = p_PRECOUNIDADE_EC
    WHERE ID_ENCOMENDA = p_ID_ENCOMENDA AND ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Encomenda de componentes atualizada';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Encomendas_componentes_delete(p_ID_ENCOMENDA INTEGER, p_ID_COMPONENTE INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM ENCOMENDAS_COMPONENTES
    WHERE ID_ENCOMENDA = p_ID_ENCOMENDA AND ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Encomenda de componentes eliminada';
END;
$$;

