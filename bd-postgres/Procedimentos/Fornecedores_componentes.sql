-- Create
CREATE OR REPLACE PROCEDURE sp_Fornecedores_componentes_create(p_ID_COMPONENTE INT4, p_ID_FORNECEDOR INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO FORNECEDORES_COMPONENTES(ID_COMPONENTE, ID_FORNECEDOR)
    VALUES (p_ID_COMPONENTE, p_ID_FORNECEDOR);
    RAISE NOTICE 'Fornecedor componente criado';
END;
$$;



-- Update
CREATE OR REPLACE PROCEDURE sp_Fornecedores_componentes_update(p_ID_COMPONENTE INT4, p_ID_FORNECEDOR INT4, p_ID_COMPONENTE_novo INT4, p_ID_FORNECEDOR_novo INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE FORNECEDORES_COMPONENTES
    SET ID_COMPONENTE = p_ID_COMPONENTE_novo, ID_FORNECEDOR = p_ID_FORNECEDOR_novo
    WHERE ID_COMPONENTE = p_ID_COMPONENTE AND ID_FORNECEDOR = p_ID_FORNECEDOR;
    RAISE NOTICE 'Fornecedor componente atualizado';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Fornecedores_componentes_delete(p_ID_COMPONENTE INT4, p_ID_FORNECEDOR INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM FORNECEDORES_COMPONENTES
    WHERE ID_COMPONENTE = p_ID_COMPONENTE AND ID_FORNECEDOR = p_ID_FORNECEDOR;
    RAISE NOTICE 'Fornecedor componente eliminado';
END;
$$;

