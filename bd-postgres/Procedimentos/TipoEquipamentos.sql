-- Create
CREATE OR REPLACE PROCEDURE sp_Tipoequipamentos_create(p_NOME_TIPOEQUIP TEXT, p_DESC_TIPOEQUIP TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO TIPOEQUIPAMENTOS(NOME_TIPOEQUIP, DESC_TIPOEQUIP)
    VALUES (p_NOME_TIPOEQUIP, p_DESC_TIPOEQUIP);
    RAISE NOTICE 'Tipo de equipamento criado';
END;
$$;


-- Update
CREATE OR REPLACE PROCEDURE sp_Tipoequipamentos_update(p_ID_TIPOEQUIP INTEGER, p_NOME_TIPOEQUIP TEXT, p_DESC_TIPOEQUIP TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE TIPOEQUIPAMENTOS
    SET NOME_TIPOEQUIP = p_NOME_TIPOEQUIP, DESC_TIPOEQUIP = p_DESC_TIPOEQUIP
    WHERE ID_TIPOEQUIP = p_ID_TIPOEQUIP;
    RAISE NOTICE 'Tipo de equipamento atualizado';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Tipoequipamentos_delete(p_ID_TIPOEQUIP INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM TIPOEQUIPAMENTOS
    WHERE ID_TIPOEQUIP = p_ID_TIPOEQUIP;
    RAISE NOTICE 'Tipo de equipamento eliminado';
END;
$$;

