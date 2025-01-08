INSERT INTO CATEGORIACOMPONENTES (NOME_CATCOMPONENTES, DESCRICAO_CATCOMPONENTES) VALUES
('Processadores', 'Execução de instruções.'),
('Memórias RAM', 'Armazenamento temporário de dados.'),
('Armazenamento SSD', 'Acesso rápido aos dados.'),
('Placas Gráficas', 'Processamento e renderização gráfica.'),
('Discos Rígidos', 'Armazenamento de dados persistentes.'),
('Placas-Mãe', 'Comunicação entre componentes.'),
('Fontes de Alimentação', 'Fornecimento de energia.'),
('Gabinetes', 'Alojamento dos componentes.'),
('Sistemas de Refrigeração', 'Manutenção da temperatura.'),
('Periféricos', 'Expansão de funcionalidades.');

INSERT INTO COMPONENTES (ID_CATCOMPONENTES, NOME_COMPONENTE, DESCRICAO_COMPONENTE, PRECOMEDIO_COMPONENTE) VALUES
(1, 'AMD Ryzen 7 3700X', 'Processador de alto desempenho com 8 núcleos e 16 threads.', 329.99),
(2, 'Corsair Vengeance LPX 16GB', 'Memória RAM DDR4 com velocidade de 3200MHz.', 79.99),
(3, 'Samsung 970 EVO Plus SSD 1TB', 'SSD NVMe M.2 com leitura de até 3500MB/s e escrita de até 3300MB/s.', 189.99),
(4, 'NVIDIA GeForce RTX 3080', 'Placa gráfica com arquitetura Ampere, 10GB de memória GDDR6X.', 699.99),
(5, 'Seagate Barracuda 2TB', 'Disco rígido interno de 3.5 polegadas com 7200 RPM.', 54.99),
(6, 'Asus ROG Strix B450-F Gaming', 'Placa-mãe ATX para processadores AMD com soquete AM4.', 129.99),
(1, 'Intel Core i9-10900K', 'Processador da 10ª geração Intel Core com 10 núcleos e 20 threads.', 499.99),
(3, 'Kingston A400 SSD 480GB', 'SSD SATA 3 com velocidades de leitura e escrita de até 500MB/s e 450MB/s.', 54.99),
(6, 'MSI MAG B550 TOMAHAWK', 'Placa-mãe ATX para processadores AMD Ryzen de 3ª geração.', 179.99),
(2, 'G.Skill Trident Z RGB 32GB', 'Kit de memória RAM DDR4 com iluminação RGB e velocidade de 3200MHz.', 159.99);

INSERT INTO FORNECEDORES (NOME_FORNECEDOR, MORADA_FORNECEDOR, EMAIL_FORNECEDOR, CONTACTO_FORNECEDOR) VALUES
('Pomerol Partners', 'Oeiras, Lisboa', 'info@pomerolpartners.com', 210000000),
('Reachdesk', 'Lisboa', 'contacto@reachdesk.com', 210000001),
('Tamanna', 'Lisboa', 'geral@tamanna.com', 210000002),
('Retarus', 'Lisboa', 'info@retarus.pt', 210000003),
('Mollie', 'Lisboa', 'support@mollie.com', 210000004),
('InnoTech', 'Lisboa', 'info@innotech.com', 210000005),
('IBM Portugal', 'Lisboa', 'contacto@ibm.pt', 210000006),
('Cisco Portugal', 'Lisboa', 'info@cisco.pt', 210000007),
('SAS Institute Software', 'Lisboa', 'support@sas.com', 210000008),
('Pipedrive', 'Lisboa', 'info@pipedrive.com', 210000009);

INSERT INTO FORNECEDORES_COMPONENTES (ID_COMPONENTE, ID_FORNECEDOR) VALUES
(1, 7),
(1, 6),
(2, 10),
(2, 9),
(3, 6),
(4, 8),
(5, 9),
(6, 1),
(7, 2),
(8, 3),
(9, 4),
(10, 5),
(10, 1);

INSERT INTO FUNCIONARIOS (NOME, DATANASC, NIF, EMAIL, CONTACTO, MORADA, CARGO) VALUES
('Pedro Alves', '1970-01-01', 111111111, 'pedroalves@empresacomp.pt', 911111111, 'Rua da Empresa 1, Lisboa', 'Gerente'),
('Maria Costa', '1972-02-02', 222222222, 'mariacosta@empresacomp.pt', 922222222, 'Rua da Empresa 2, Lisboa', 'Secretária'),
('Joana Martins', '1974-03-03', 333333333, 'joanamartins@empresacomp.pt', 933333333, 'Rua da Empresa 3, Lisboa', 'Contabilista'),
('Rui Sousa', '1976-04-04', 444444444, 'ruisousa@empresacomp.pt', 944444444, 'Rua da Empresa 4, Lisboa', 'Técnico'),
('Carlos Silva', '1978-05-05', 555555555, 'carlossilva@empresacomp.pt', 955555555, 'Rua da Empresa 5, Lisboa', 'Técnico'),
('Ana Ferreira', '1980-06-06', 666666666, 'anaferreira@empresacomp.pt', 966666666, 'Rua da Empresa 6, Lisboa', 'Técnica'),
('Miguel Santos', '1982-07-07', 777777777, 'miguelsantos@empresacomp.pt', 977777777, 'Rua da Empresa 7, Lisboa', 'Técnico'),
('Sofia Oliveira', '1984-08-08', 888888888, 'sofiaoliveira@empresacomp.pt', 988888888, 'Rua da Empresa 8, Lisboa', 'Técnica'),
('Bruno Dias', '1986-09-09', 999999999, 'brunodias@empresacomp.pt', 999999999, 'Rua da Empresa 9, Lisboa', 'Técnico'),
('Sara Rodrigues', '1988-10-10', 123456789, 'sararodrigues@empresacomp.pt', 912345678, 'Rua da Empresa 10, Lisboa', 'Técnica');

INSERT INTO ARMAZEM (NOME_ARMAZEM, MORADA_ARMAZEM, EMAIL_ARMAZEM, CONTACTO_ARMAZEM, ID_FUNCIONARIO) VALUES
('Armazém Central', 'Rua Principal, Lisboa', 'armcentral@empresacomp.pt', 211234567, 1),
('Armazém Norte', 'Avenida da Liberdade, Porto', 'armnorte@empresacomp.pt', 221234567, 2),
('Armazém Sul', 'Praça do Comércio, Faro', 'armsul@empresacomp.pt', 281234567, 3),
('Armazém Este', 'Rua de Santa Catarina, Braga', 'armeste@empresacomp.pt', 253123456, 4),
('Armazém Oeste', 'Largo do Toural, Guimarães', 'armoeste@empresacomp.pt', 253123457, 5),
('Armazém Alentejo', 'Avenida da República, Évora', 'armalentejo@empresacomp.pt', 266123456, 6),
('Armazém Algarve', 'Marina de Vilamoura, Quarteira', 'armalgarve@empresacomp.pt', 289123456, 7),
('Armazém Madeira', 'Estrada Monumental, Funchal', 'armmadeira@empresacomp.pt', 291123456, 8),
('Armazém Açores', 'Rua da Esperança, Ponta Delgada', 'armacores@empresacomp.pt', 296123456, 9),
('Armazém Centro', 'Rua Sofia, Coimbra', 'armcentro@empresacomp.pt', 239123456, 10);

INSERT INTO GUIAREMESSACOMPRAS (ID_ARMAZEM, DATA_GUIACOMPRAS, ID_FUNCIONARIO) VALUES
(1, '2024-01-01', 1),
(2, '2024-01-01', 2),
(3, '2024-01-04', 3),
(1, '2024-01-04', 1),
(2, '2024-01-07', 2),
(3, '2024-01-07', 3),
(1, '2024-01-10', 1),
(2, '2024-01-10', 2),
(3, '2024-01-13', 3),
(1, '2024-01-13', 1);

INSERT INTO ENCOMENDAS (ID_GUIACOMPRAS, DATA_ENCOMENDA, ID_FUNCIONARIO) VALUES
(1, '2024-01-01', 1),
(2, '2024-01-01', 2),
(3, '2024-01-04', 3),
(4, '2024-01-04', 1),
(5, '2024-01-07', 2),
(6, '2024-01-07', 3),
(7, '2024-01-10', 1),
(8, '2024-01-10', 2),
(9, '2024-01-13', 3),
(10, '2024-01-13', 1);

INSERT INTO ENCOMENDAS_COMPONENTES (ID_ENCOMENDA, ID_COMPONENTE, QUANTIDADE_EC, PRECOUNIDADE_EC) VALUES
(1, 1, 10, 329.99),
(2, 2, 15, 79.99),
(3, 3, 20, 189.99),
(4, 4, 5, 699.99),
(5, 5, 8, 54.99),
(6, 6, 12, 129.99),
(7, 7, 6, 499.99),
(8, 8, 10, 54.99),
(9, 9, 4, 179.99),
(10, 10, 7, 159.99),
(1, 2, 20, 79.99),
(2, 3, 10, 189.99),
(3, 4, 3, 699.99),
(4, 5, 6, 54.99),
(5, 6, 8, 129.99),
(6, 7, 4, 499.99),
(7, 8, 12, 54.99),
(8, 9, 2, 179.99),
(9, 10, 5, 159.99),
(10, 1, 8, 329.99);

INSERT INTO STOCKCOMPONENTES (ID_ARMAZEM, ID_COMPONENTE, QUANTIDADE_STOCKCOMP) VALUES
(1, 1, 90),
(1, 2, 130),
(1, 3, 170),
(2, 4, 50),
(2, 5, 80),
(2, 6, 120),
(3, 7, 60),
(3, 8, 140),
(3, 9, 110),
(1, 10, 100);

INSERT INTO TIPOEQUIPAMENTOS (NOME_TIPOEQUIP, DESC_TIPOEQUIP) VALUES
('Computador Desktop', 'Para uso profissional e pessoal'),
('Computador Gaming', 'Para jogos de alta performance'),
('Workstation', 'Para tarefas de computação intensiva');

INSERT INTO MAODEOBRA (NOME_MO, DESC_MO, CUSTO_MO) VALUES
('Montagem Básica', 'Montagem de desktops', 50.00),
('Montagem Avançada', 'Montagem de PCs gaming', 80.00),
('Montagem Especializada', 'Montagem de workstations', 120.00);

INSERT INTO EQUIPAMENTOS (ID_TIPOEQUIP, ID_MO, NOME_EQUIP, DESC_EQUIP, CUSTO_EQUIP) VALUES
(1, 1, 'HP Pavilion TG01', 'Desktop versátil', 899.99),
(2, 2, 'Asus ROG Strix', 'Gaming alto desempenho', 1999.99),
(3, 3, 'Dell Precision 5820', 'Workstation confiável', 2499.99),
(1, 1, 'Lenovo IdeaCentre 5', 'Desktop familiar', 579.99),
(2, 2, 'Acer Predator Orion', 'Gaming potente', 2999.99),
(1, 1, 'Dell Inspiron 3881', 'Desktop compacto', 649.99),
(2, 2, 'MSI Trident A Plus', 'Gaming compacto', 1599.99),
(1, 1, 'Apple Mac Mini M1', 'Desktop pequeno', 799.99),
(2, 2, 'HP Omen 30L', 'Gaming avançado', 2299.99),
(1, 1, 'Asus Vivo V222', 'All-in-One prático', 1049.99);

INSERT INTO STOCKEQUIPAMENTOS (ID_ARMAZEM, ID_EQUIP, QUANTIDADE_STOCKEQUIP) VALUES
(1, 1, 20),
(1, 2, 15),
(1, 3, 10),
(2, 4, 25),
(2, 5, 10),
(2, 6, 5),
(3, 7, 30),
(3, 8, 20),
(3, 9, 15),
(1, 10, 12);

INSERT INTO CLIENTES (NOME_CLIENTE, DATANASC_CLIENTE, MORADA_CLIENTE, NIF_CLIENTE, EMAIL_CLIENTE, CONTACTO_CLIENTE) VALUES
('João Silva', '1980-05-21', 'Rua das Flores 123, Lisboa', 298765432, 'joaosilva@gmail.com', 912345678),
('Ana Sousa', '1975-08-30', 'Avenida da República 456, Porto', 123456789, 'anasousa@sapo.pt', 931234567),
('Miguel Fernandes', '1982-11-15', 'Praceta do Comércio 789, Coimbra', 234567890, 'miguelfernandes@sapo.pt', 920123456),
('Sofia Gomes', '1978-02-27', 'Largo do Rossio 321, Faro', 345678901, 'sofiagomes@gmail.com', 939876543),
('Ricardo Pereira', '1985-07-09', 'Rua de Santo António 654, Braga', 456789012, 'ricardopereira@outlook.com', 918765432),
('Marta Carvalho', '1983-12-20', 'Alameda dos Oceanos 987, Viseu', 567890123, 'martacarvalho@gmail.com', 927654321),
('Luís Santos', '1976-03-14', 'Calçada da Graça 246, Évora', 678901234, 'luissantos@gmail.com', 936543210),
('Carla Oliveira', '1981-09-05', 'Rua da Liberdade 135, Setúbal', 789012345, 'carlaoliveira@gmail.com', 925432109),
('Francisco Costa', '1979-01-22', 'Avenida dos Aliados 864, Aveiro', 890123456, 'franciscocosta@sapo.pt', 914321098),
('Teresa Pinto', '1984-04-17', 'Praça do Município 579, Funchal', 901234567, 'teresapinto@gmail.com', 932109876);

INSERT INTO GUIAREMESSAVENDAS (ID_ARMAZEM, DATA_GUIAVENDAS, ID_FUNCIONARIO) VALUES
(1, '2024-01-11', 4),
(2, '2024-01-11', 1),
(3, '2024-01-11', 8),
(1, '2024-01-12', 5),
(2, '2024-01-12', 9),
(3, '2024-01-12', 3),
(1, '2024-01-13', 6),
(2, '2024-01-13', 2),
(3, '2024-01-13', 7),
(1, '2024-01-14', 10);

INSERT INTO FATURA (ID_GUIAVENDAS, ID_CLIENTE, PRECO_FATURA, DATA_FATURA) VALUES
(1, 1, 899.99, '2024-01-11'),
(2, 2, 1999.99, '2024-01-11'),
(3, 3, 2499.99, '2024-01-11'),
(4, 4, 579.99, '2024-01-12'),
(5, 5, 2999.99, '2024-01-12'),
(6, 6, 649.99, '2024-01-12'),
(7, 7, 1599.99, '2024-01-13'),
(8, 8, 799.99, '2024-01-13'),
(9, 9, 2299.99, '2024-01-13'),
(10, 10, 1049.99, '2024-01-14');

INSERT INTO EQUIPAMENTOS_FATURA (ID_FATURA, ID_EQUIP, QUANTIDADE_EQUIPFATURA) VALUES
(1, 1, 1),
(1, 2, 2),
(2, 3, 1),
(2, 4, 1),
(3, 5, 1),
(4, 6, 2),
(5, 7, 1),
(5, 8, 1),
(5, 9, 1),
(6, 10, 3),
(7, 2, 1),
(7, 3, 1),
(8, 4, 1),
(9, 5, 2),
(9, 6, 1),
(10, 7, 1),
(10, 1, 1);

INSERT INTO RECEITAEQUIP (ID_EQUIP, ID_COMPONENTE, QUANTIDADE_RECEITA) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 1),
(2, 1, 1),
(2, 2, 2),
(2, 3, 1),
(3, 1, 1),
(3, 2, 2),
(3, 3, 1),
(4, 1, 1),
(4, 2, 2),
(4, 3, 1),
(5, 1, 1),
(5, 2, 2),
(5, 3, 1),
(6, 1, 1),
(6, 2, 2),
(6, 3, 1),
(7, 1, 1),
(7, 2, 2),
(7, 3, 1),
(8, 1, 1),
(8, 2, 2),
(8, 3, 1),
(9, 1, 1),
(9, 2, 2),
(9, 3, 1),
(10, 1, 1),
(10, 2, 2),
(10, 3, 1);

INSERT INTO NIVELACESSO_PGESTAO (NOME_NIVEL, DESC_NIVEL) VALUES
('Administrador', 'Acesso total ao sistema de gestão'),
('Consultor', 'Acesso limitado a visualização no sistema de gestão');

INSERT INTO ACESSO_PGESTAO (ID_FUNCIONARIO, ID_NIVEL, PASSWORD_PGESTAO) VALUES
(1, 1, 'admin123'),
(2, 1, 'admin123'),
(3, 1, 'admin456'),
(4, 2, 'password123'),
(5, 1, 'password456'),
(6, 2, 'password789'),
(7, 1, 'password321'),
(8, 2, 'password654'),
(9, 2, 'password987'),
(10, 2, 'password147');

INSERT INTO PRODUCAO_DIARIA (DATA_PRODUCAO, ID_ARMAZEM) VALUES
('2024-01-15', 1),
('2024-01-15', 2),
('2024-01-15', 3),
('2024-01-16', 1),
('2024-01-16', 2),
('2024-01-16', 3),
('2024-01-17', 1),
('2024-01-17', 2),
('2024-01-17', 3),
('2024-01-18', 1);

INSERT INTO LOTES (ID_PRODUCAO, ID_TIPOEQUIP, QUANTIDADE_PRODUTOS, ID_ARMAZEM, ID_FUNCIONARIO) VALUES
(1, 1, 10, 1, 4),
(2, 2, 5, 2, 5),
(3, 3, 3, 3, 6),
(4, 1, 8, 1, 7),
(5, 2, 6, 2, 8),
(6, 3, 4, 3, 9),
(7, 1, 12, 1, 10),
(8, 2, 7, 2, 4),
(9, 3, 5, 3, 5),
(10, 1, 9, 1, 6);
