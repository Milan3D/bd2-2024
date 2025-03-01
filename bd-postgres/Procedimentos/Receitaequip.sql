-- Create
CREATE OR REPLACE PROCEDURE sp_Receitaequip_create(p_ID_EQUIP INT4, p_ID_COMPONENTE INT4, p_QUANTIDADE_RECEITA INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO RECEITAEQUIP(ID_EQUIP, ID_COMPONENTE, QUANTIDADE_RECEITA)
    VALUES (p_ID_EQUIP, p_ID_COMPONENTE, p_QUANTIDADE_RECEITA);
    RAISE NOTICE 'Receita equipamento criada';
END;
$$;

-- Read
CREATE OR REPLACE PROCEDURE sp_Receitaequip_read(p_ID_EQUIP INT4, p_ID_COMPONENTE INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT QUANTIDADE_RECEITA
    FROM RECEITAEQUIP
    WHERE ID_EQUIP = p_ID_EQUIP AND ID_COMPONENTE = p_ID_COMPONENTE;
END;
$$;

-- Update
CREATE OR REPLACE PROCEDURE sp_Receitaequip_update(p_ID_EQUIP INT4, p_ID_COMPONENTE INT4, p_QUANTIDADE_RECEITA INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE RECEITAEQUIP
    SET QUANTIDADE_RECEITA = p_QUANTIDADE_RECEITA
    WHERE ID_EQUIP = p_ID_EQUIP AND ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Receita equipamento atualizada';
END;
$$;

-- Delete
CREATE OR REPLACE PROCEDURE sp_Receitaequip_delete(p_ID_EQUIP INT4, p_ID_COMPONENTE INT4)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM RECEITAEQUIP
    WHERE ID_EQUIP = p_ID_EQUIP AND ID_COMPONENTE = p_ID_COMPONENTE;
    RAISE NOTICE 'Receita equipamento eliminada';
END;
$$;

-- List
CREATE OR REPLACE PROCEDURE sp_Receitaequip_list()
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT ID_EQUIP, ID_COMPONENTE, QUANTIDADE_RECEITA
    FROM RECEITAEQUIP;
END;
$$;
