-- Create
CREATE OR REPLACE PROCEDURE sp_Componentes_create(p_ID_CATCOMPONENTES INT4, p_NOME_COMPONENTE TEXT, p_DESCRICAO_COMPONENTE TEXT, p_PRECOMEDIO_COMPONENTE DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO COMPONENTES(ID_CATCOMPONENTES, NOME_COMPONENTE, DESCRICAO_COMPONENTE, PRECOMEDIO_COMPONENTE)
    VALUES (p_ID_CATCOMPONENTES, p_NOME_COMPONENTE, p_DESCRICAO_COMPONENTE, p_PRECOMEDIO_COMPONENTE);
    RAISE NOTICE 'Componente criado';
END;
$$;

-- Read
CREATE OR REPLACE PROCEDURE sp_Componentes_read(p_ID_COMPONENTE INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT ID_CATCOMPONENTES, NOME_COMPONENTE, DESCRICAO_COMPONENTE, PRECOMEDIO_COMPONENTE
    FROM COMPONENTES
    WHERE ID_COMPONENTE = p_ID_COMPONENTE;
END;
$$;

-- Update
CREATE OR REPLACE PROCEDURE sp_Componentes_update(p_ID_COMPONENTE INTEGER, p_ID_CATCOMPONENTES INT4, p_NOME_COMPONENTE TEXT, p_DESCRICAO_COMPONENTE TEXT, p_PRECOMEDIO_COMPONENTE DECIMAL)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE COMPONENTES
    SET ID_CATCOMPONENTES = p_ID_CATCOMPONENTES, NOME_COMPONENTE = p_NOME_COMPONENTE, DESCRICAO_COMPONENTE = p_DESCRICAO_COMPONENTE, PRECOMEDIO_COMPONENTE = p_PRECOMEDIO_COMPONENTE
    WHERE ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Componente atualizado';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Componentes_delete(p_ID_COMPONENTE INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM COMPONENTES
    WHERE ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Componente eliminado';
END;
$$;

