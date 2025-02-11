from django.contrib import admin
from django.urls import path
from BD_2 import views
from .views import logout_view

urlpatterns = [
    path('', view=views.index, name='index'),
    path('homepage/', view=views.homepage, name='homepage'),
    path('homepage_site_vendas/', view=views.homepage_site_vendas, name='homepage_site_vendas'),
    path('login/', view=views.login, name='login'),
    path('login_site_vendas/', view=views.login_site_vendas, name='login_site_vendas'),
    path('criar_conta/', view=views.criar_conta, name='criar_conta'),
    path('comprar/<str:nome_equip>/<str:preco_equip>/<str:total_equip>/',view=views.comprar , name='comprar'),
    path('purchase_history/', view=views.purchase_history, name='purchase_history'),

    path('equipamentos/', view=views.equipamentos, name='equipamentos'),
    path('adicionar_equipamento/', view=views.adicionar_equipamento, name='adicionar_equipamento'),
    path('eliminar_equipamento/<int:id>/', views.excluir_equipamento, name='eliminar_equipamento'),
    path('editar_equipamento/<int:id>/', view=views.editar_equipamento, name='editar_equipamento'),
    path('equipamento/<int:id>/', view=views.equipamento, name='equipamento'),

    path('componentes/', views.componentes, name='componentes'),
    path('adicionar_componente/', views.adicionar_componente, name='adicionar_componente'),
    path('editar_componente/<int:id>/', views.editar_componente, name='editar_componente'),
    path('eliminar_componente/<int:id>/', views.eliminar_componente, name='eliminar_componente'),

    path('encomendas/', views.encomendas, name='encomendas'),
    path('adicionar_encomenda/', views.adicionar_encomenda, name='adicionar_encomenda'),
    path('eliminar_encomenda/<int:id>/', views.eliminar_encomenda, name='eliminar_encomenda'),
    path('editar_encomenda/<int:id>/', views.editar_encomenda, name='editar_encomenda'),

    path('stock_equipamentos/', view=views.stock_equipamentos, name='stock_equipamentos'),
    path('adicionar_stock_equipamento/', views.adicionar_stock_equipamento, name='adicionar_stock_equipamento'),
    path('editar_stock_equipamento/<int:id_armazem>/<int:id_equip>/', views.editar_stock_equipamento, name='editar_stock_equipamento'),
    path('excluir_stock_equipamento/<int:id_armazem>/<int:id_equip>/', views.excluir_stock_equipamento, name='excluir_stock_equipamento'),

    path('stockcomponentes/', views.stockcomponentes, name='stockcomponentes'),
    path('adicionar_stockcomponente/', views.adicionar_stockcomponente, name='adicionar_stockcomponente'),
    path('editar_stockcomponente/<int:id_armazem>/<int:id_componente>/', views.editar_stockcomponente, name='editar_stockcomponente'),
    path('eliminar_stockcomponente/<int:id_armazem>/<int:id_componente>/', views.eliminar_stockcomponente, name='eliminar_stockcomponente'),

    path('tipoequipamentos/', views.tipoequipamentos, name='tipoequipamentos'),
    path('adicionar_tipoequipamento/', views.adicionar_tipoequipamento, name='adicionar_tipoequipamento'),
    path('editar_tipoequipamento/<int:id_tipoequip>/', views.editar_tipoequipamento, name='editar_tipoequipamento'),
    path('eliminar_tipoequipamento/<int:id_tipoequip>/', views.eliminar_tipoequipamento, name='eliminar_tipoequipamento'),



    path('encomendas_componentes/', views.encomendas_componentes, name='encomendas_componentes'),
    path('adicionar_encomenda_componente/', views.adicionar_encomenda_componente, name='adicionar_encomenda_componente'),
    path('editar_encomenda_componente/<int:id_encomenda>/<int:id_componente>/', views.editar_encomenda_componente, name='editar_encomenda_componente'),
    path('eliminar_encomenda_componente/<int:id_encomenda>/<int:id_componente>/', views.eliminar_encomenda_componente, name='eliminar_encomenda_componente'),


    path('categorias_componentes/', views.categorias_componentes, name='categorias_componentes'),
    path('editar_categoria_componentes/<int:id_categoria>/', views.editar_categoria_componentes, name='editar_categoria_componentes'),
    path('excluir_categoria_componentes/<int:id_categoria>/', views.excluir_categoria_componentes, name='excluir_categoria_componentes'),
    path('adicionar_categoria_componentes/', views.adicionar_categoria_componentes, name='adicionar_categoria_componentes'),

    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('adicionar_fornecedor/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('editar_fornecedor/<int:id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('excluir_fornecedor/<int:id>/', views.excluir_fornecedor, name='excluir_fornecedor'),

    path('fornecedores_componentes/', views.fornecedores_componentes, name='fornecedores_componentes'),
    path('adicionar_fornecedor_componente/', views.adicionar_fornecedor_componente, name='adicionar_fornecedor_componente'),
    path('editar_fornecedor_componente/<int:id_componente>/<int:id_fornecedor>/', views.editar_fornecedor_componente, name='editar_fornecedor_componente'),
    path('excluir_fornecedor_componente/<int:id_componente>/<int:id_fornecedor>/', views.excluir_fornecedor_componente, name='excluir_fornecedor_componente'),

    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('adicionar_funcionario/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('editar_funcionario/<int:id_funcionario>/', views.editar_funcionario, name='editar_funcionario'),
    path('excluir_funcionario/<int:id_funcionario>/', views.excluir_funcionario, name='excluir_funcionario'),

    path('armazens/', views.armazens, name='armazens'),
    path('adicionar_armazem/', views.adicionar_armazem, name='adicionar_armazem'),
    path('editar_armazem/<int:id_armazem>/', views.editar_armazem, name='editar_armazem'),
    path('excluir_armazem/<int:id_armazem>/', views.excluir_armazem, name='excluir_armazem'),


    path('lotes/', views.lotes, name='lotes'),
    path('adicionar_lote/', views.adicionar_lote, name='adicionar_lote'),
    path('editar_lote/<int:id_lote>/', views.editar_lote, name='editar_lote'),
    path('eliminar_lote/<int:id_lote>/', views.eliminar_lote, name='eliminar_lote'),

    path('maodeobra/', views.maodeobra, name='maodeobra'),
    path('adicionar_maode_obra/', views.adicionar_maode_obra, name='adicionar_maodeobra'),
    path('editar_maodeobra/<int:id_mo>/', views.editar_maodeobra, name='editar_maodeobra'),
    path('excluir_maodeobra/<int:id_mo>/', views.excluir_maodeobra, name='excluir_maodeobra'),

    path('producao_diaria/', views.producao_diaria, name='producao_diaria'),
    path('adicionar_producao_diaria/', views.adicionar_producao_diaria, name='adicionar_producao_diaria'),
    path('editar_producao_diaria/<int:id_producao>/', views.editar_producao_diaria, name='editar_producao_diaria'),
    path('excluir_producao_diaria/<int:id_producao>/', views.excluir_producao_diaria, name='excluir_producao_diaria'),


    path('user/', view=views.user, name='user'),
    path('editar_user/<int:id>/', view=views.editar_user, name='editar_user'),
    path('historico_user/<int:id>/', view=views.historico_user, name='historico_user'),
    path('detalhes_encomenda/<int:id>/', view=views.detalhes_encomenda, name='detalhes_encomenda'),

    path('cliente/', view=views.cliente, name='cliente'),
    path('editar_cliente/<int:id>/', view=views.editar_cliente, name='editar_cliente'),
    path('adicionar_cliente/', view=views.adicionar_cliente, name='adicionar_cliente'),
    path('excluir_cliente/<int:id>/', view=views.excluir_cliente, name='excluir_cliente'),

    path('fatura/', view=views.fatura, name='fatura'),
    path('adicionar_fatura/', view=views.adicionar_fatura, name='adicionar_fatura'),
    path('editar_fatura/<int:id>/', view=views.editar_fatura, name='editar_fatura'),
    path('excluir_fatura/<int:id>/', view=views.excluir_fatura, name='excluir_fatura'),


    path('homepage_utilizador/', view=views.homepage_utilizador, name='homepage_utilizador'),

    path('excluir_equipamento/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', logout_view, name='logout'),
]
