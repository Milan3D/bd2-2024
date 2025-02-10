import json
import logging
import traceback

from bson import ObjectId
from django.db import DatabaseError, connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from .models import acesso_pgestao
from .modelsextra import Equipamentos
from django.db import connection
from decimal import Decimal 
from django.contrib import messages
from .utils import LocalStorage
from datetime import datetime
from django.utils import timezone

from .models_mongo import User
from .models_mongo import Equipment
from .models_mongo import Purchase
from django.conf import settings



logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def homepage(request):
    # Recuperar id_nivel da sessão usando LocalStorage
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")
    return render(request, 'homepage.html', {'id_nivel': id_nivel})

def homepage_utilizador(request):
    return render(request, 'utilizadores/homepage.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('id_utilpgestao')  # This is the email field
        password = request.POST.get('password_pgestao')

        # Step 1: Retrieve all funcionarios and check for the email
        funcionarios = []
        with connection.cursor() as cursor:
            try:
                cursor.execute('SELECT * FROM public.fn_funcionarios_list()')
                resultados = cursor.fetchall()

                for resultado in resultados:
                    funcionario = {
                        'ID_FUNCIONARIO': resultado[0],
                        'NOME': resultado[1],
                        'DATANASC': resultado[2],
                        'NIF': resultado[3],
                        'EMAIL': resultado[4],
                        'CONTACTO': resultado[5],
                        'MORADA': resultado[6],
                        'CARGO': resultado[7],
                    }
                    funcionarios.append(funcionario)

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                funcionarios = []

        # Step 2: Check if the email exists in the funcionarios list
        funcionario = next((f for f in funcionarios if f['EMAIL'] == email), None)

        if funcionario:
            # Step 3: Use id_funcionario to check the acesso_pgestao table
            user = acesso_pgestao.objects.filter(
                id_utilpgestao=funcionario['ID_FUNCIONARIO'],  # Corrected to use id_utilpgestao
                password_pgestao=password
            ).first()  # Assuming acesso_pgestao is the model for acesso_pgestao

            if user:
                # Authentication successful
                print(f"Utilizador autenticado: {user.id_utilpgestao} - Nível {user.id_nivel}")

                # Store id_nivel and name in session
                LocalStorage.set_id_nivel(request, user.id_nivel)
                request.session['user_name'] = funcionario['NOME']  # Store the user's name in the session
                print(f"User name stored in session: {request.session['user_name']}")  # Debugging line

                return redirect('homepage')
            else:
                messages.add_message(request, messages.ERROR, 'Credenciais inválidas. Tente novamente.')
        else:
            messages.add_message(request, messages.ERROR, 'Email não encontrado. Tente novamente.')

    return render(request, 'index.html')
#---------------------------------------------------------------------------------------------------------------------

def equipamentos(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    
    with connection.cursor() as cursor:
        try:
            # Get equipment list with joined data
            print("Fetching equipment list with joined data...")
            cursor.execute('''
                SELECT e.*, t.nome_tipoequip, m.nome_mo 
                FROM public.fn_equipamentos_list() e
                LEFT JOIN public.fn_tipoequipamentos_list() t ON e.id_tipoequip = t.id_tipoequip
                LEFT JOIN public.fn_maodeobra_list() m ON e.id_mo = m.id_mo
            ''')
            resultados = cursor.fetchall()
            print(f"Equipment results with joined data: {resultados}")
            
            # Get all tipo_equipamento options for dropdowns
            cursor.execute('SELECT * FROM public.fn_tipoequipamentos_list()')
            tipos_equipamento = cursor.fetchall()
            
            # Get all mao_obra options for dropdowns
            cursor.execute('SELECT * FROM public.fn_maodeobra_list()')
            maos_obra = cursor.fetchall()
            
            equipamentos = []
            for resultado in resultados:
                equipamento = {
                    'ID_EQUIP': resultado[0],
                    'ID_TIPOEQUIP': resultado[1],
                    'ID_MO': resultado[2],
                    'NOME_EQUIP': resultado[3],
                    'DESC_EQUIP': resultado[4],
                    'CUSTO_EQUIP': resultado[5],
                    'TIPO_EQUIPAMENTO_NOME': resultado[6] if len(resultado) > 6 else 'N/A',
                    'MAO_OBRA_NOME': resultado[7] if len(resultado) > 7 else 'N/A'
                }
                equipamentos.append(equipamento)

        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            equipamentos = []
            tipos_equipamento = []
            maos_obra = []

    context = {
        'equipamentos': equipamentos,
        'tem_permissao': tem_permissao,
        'tipos_equipamento': tipos_equipamento,
        'maos_obra': maos_obra,
    }
    return render(request, 'equipamentos.html', context)

@csrf_exempt  # Only if you're having CSRF issues
def adicionar_equipamento(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            print(f"Received data for new equipment: {dados}")  # Debug print
            
            with connection.cursor() as cursor:
                cursor.execute('''
                    CALL sp_Equipamentos_create(%s, %s, %s, %s, %s)
                ''', [
                    dados['idTipoEquip'],
                    dados['idMo'],
                    dados['nomeEquip'],
                    dados['descEquip'],
                    dados['custoEquip']
                ])
                
                connection.commit()
                print("Equipment added successfully!")  # Debug print
                
                return JsonResponse({
                    'mensagem': 'Equipamento adicionado com sucesso',
                    'refresh': True
                })
                
        except Exception as e:
            print(f"Error adding equipment: {str(e)}")  # Debug print
            return JsonResponse({
                'erro': f'Erro ao adicionar equipamento: {str(e)}'
            }, status=500)
            
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def excluir_equipamento(request, id):
    if request.method == 'POST':
        try:
            print(f"Attempting to delete equipment with ID: {id}")
            
            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Equipamentos_delete(%s)', [id])
                connection.commit()
                print(f"Equipment {id} deleted successfully!")
                
                return JsonResponse({
                    'mensagem': 'Equipamento excluído com sucesso',
                    'refresh': True
                })
                
        except Exception as e:
            print(f"Error deleting equipment: {str(e)}")
            return JsonResponse({
                'erro': f'Erro ao excluir equipamento: {str(e)}'
            }, status=500)
            
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt  # Only if you're having CSRF issues
def editar_equipamento(request, id):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            print(f"Received data: {dados}")  # Debug print
            
            with connection.cursor() as cursor:
                cursor.execute('''
                    CALL sp_Equipamentos_update(%s, %s, %s, %s, %s, %s)
                ''', [
                    id,
                    dados['idTipoEquip'],
                    dados['idMo'],
                    dados['nomeEquip'],
                    dados['descEquip'],
                    dados['custoEquip']
                ])
                
                connection.commit()
                print("Equipment updated successfully!")  # Debug print
                
                return JsonResponse({
                    'mensagem': 'Equipamento atualizado com sucesso',
                    'refresh': True
                })
                
        except Exception as e:
            print(f"Error updating equipment: {str(e)}")  # Debug print
            return JsonResponse({
                'erro': f'Erro ao atualizar equipamento: {str(e)}'
            }, status=500)
            
    return JsonResponse({'erro': 'Método não permitido'}, status=405)
#---------------------------------------------------------------------------------------------------------------------



def encomendas(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            # Use SELECT para chamar a função e obter resultados
            cursor.execute('SELECT * FROM public.fn_encomendas_list()')

            # Obtenha todos os resultados
            resultados = cursor.fetchall()

            # Crie uma lista de dicionários a partir dos resultados
            encomendas = []
            for resultado in resultados:
                # Verifique se a tupla tem o número esperado de elementos
                if len(resultado) >= 3:
                    encomenda = {
                        'ID_ENCOMENDA': resultado[0],
                        'ID_GUIACOMPRAS': resultado[1],
                        'DATA_ENCOMENDA': resultado[2],
                        'ID_FUNCIONARIO': resultado[3],
                    }
                    encomendas.append(encomenda)
                else:
                    print(f"Comprimento de tupla inesperado: {len(resultado)}")

        except Exception as e:
            # Trate exceções (imprima ou registre o erro, trate conforme necessário)
            print(f"Tipo de exceção: {type(e)}")
            print(f"Mensagem de exceção: {str(e)}")
            encomendas = []

    context = {
        'encomendas': encomendas,
        'tem_permissao': tem_permissao,
}
    return render(request, 'encomendas.html', context)

# Adicionar uma nova encomenda
def adicionar_encomenda(request):
    if request.method == 'POST':
        id_guiacompras = int(request.POST.get('id_guiacompras'))
        data_encomenda = request.POST.get('data_encomenda')
        id_funcionario = int(request.POST.get('id_funcionario'))

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_encomendas_create(%s, %s, %s)', [id_guiacompras, data_encomenda, id_funcionario])
                connection.commit()
                print("Encomenda adicionada com sucesso!")

                return redirect('encomendas')

            except Exception as e:
                print(f"Tipo de exceção: {type(e)}")
                print(f"Mensagem de exceção: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar encomenda!")

    return HttpResponse("Erro ao adicionar encomenda!")

# Excluir uma encomenda
def eliminar_encomenda(request, id):
    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_encomendas_delete(%s)', [id])
            connection.commit()
            print("Encomenda eliminada com sucesso!")

            return redirect('encomendas')

        except Exception as e:
            print(f"Tipo de exceção: {type(e)}")
            print(f"Mensagem de exceção: {str(e)}")
            connection.rollback()
            print("Erro ao eliminar encomenda!")

    return HttpResponse("Erro ao eliminar encomenda!")

# Editar uma encomenda
def editar_encomenda(request, id):
    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)

            novoIdGuiaCompras = dados_json.get('idGuiaCompras')
            novaDataEncomenda_str = dados_json.get('dataEncomenda')
            novoIdFuncionario = dados_json.get('idFuncionario')

            # Converter a string da data para o formato adequado (assumindo que está no formato 'Feb. 5, 2024')
            novaDataEncomenda = datetime.strptime(novaDataEncomenda_str, '%b. %d, %Y').date()

            print(f"Encomenda: {id} {novoIdGuiaCompras} {novaDataEncomenda} {novoIdFuncionario}")

            # Lógica

            # Execute o procedimento armazenado para editar a encomenda
            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Encomendas_update(%s, %s, %s, %s)', [id, novoIdGuiaCompras, novaDataEncomenda, novoIdFuncionario])
                connection.commit()
                print("Encomenda editada com sucesso!")

                # Exemplo de retorno de uma resposta de sucesso
                response_data = {'mensagem': 'Encomenda editada com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'erro': 'Erro ao decodificar JSON'}, status=400)
        except ValueError as e:
            return JsonResponse({'erro': 'Erro ao converter a data'}, status=400)

    # Se não for uma solicitação POST, retorne uma resposta de erro
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

#-----------------------------------------------------------------------------------------------------------


def componentes(request):
    with connection.cursor() as cursor:
        try:
            print("Starting componentes view function...")
            
            # Using correct table name 'categoriacomponentes'
            cursor.execute("""
                SELECT c.*, cat.nome_catcomponentes 
                FROM componentes c
                LEFT JOIN categoriacomponentes cat ON c.id_catcomponentes = cat.id_catcomponentes
            """)
            resultados = cursor.fetchall()
            print(f"Query results: {resultados}")
            
            componentes = []
            for resultado in resultados:
                print(f"Processing row: {resultado}")
                componente = {
                    'ID_COMPONENTE': resultado[0],
                    'ID_CATCOMPONENTES': resultado[1],
                    'NOME_COMPONENTE': resultado[2],
                    'DESCRICAO_COMPONENTE': resultado[3],
                    'PRECOMEDIO_COMPONENTE': resultado[4],
                    'categoria': {
                        'NOME_CATCOMPONENTES': resultado[5] if resultado[5] else 'N/A'
                    }
                }
                componentes.append(componente)
                print(f"Added component: {componente}")

        except Exception as e:
            print(f"Error occurred: {type(e)}")
            print(f"Error message: {str(e)}")
            print(f"Error details:", e)
            componentes = []

    context = {
        'componentes': componentes,
    }
    print(f"Final context being sent to template: {context}")
    return render(request, 'componentes.html', context)

def adicionar_componente(request):
    if request.method == 'POST':
        id_catcomponentes = int(request.POST.get('id_catcomponentes'))
        nome_componente = request.POST.get('nome_componente')
        descricao_componente = request.POST.get('desc_componente')
        precomedio_componente_str = request.POST.get('preco_componente')
        precomedio_componente = Decimal(precomedio_componente_str) if precomedio_componente_str is not None else None

        print(precomedio_componente)

        

        with connection.cursor() as cursor:
            try:
                print(f"Componente: {id_catcomponentes} {nome_componente} {descricao_componente} {precomedio_componente}")
                cursor.execute('CALL sp_Componentes_create(%s, %s, %s, %s)', [id_catcomponentes, nome_componente, descricao_componente, precomedio_componente])
                connection.commit()
                print("Componente adicionado com sucesso!")

                return redirect('componentes')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar componente!")

    return HttpResponse("Erro ao adicionar componente!")

def eliminar_componente(request, id):
    with connection.cursor() as cursor:
        try:
            print("Componente: ", id)
            cursor.execute('CALL sp_Componentes_delete(%s)', [id])
            connection.commit()
            print("Componente eliminado com sucesso!")

            return redirect('componentes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao eliminar componente!")

    return HttpResponse("Erro ao eliminar componente!")

def editar_componente(request, id):
    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)

            novoCatComponente = dados_json.get('idCatComponente')
            novoNomeComponente = dados_json.get('nomeComponente')
            novaDescricaoComponente = dados_json.get('descComponente')
            novoPrecoMedioComponente = dados_json.get('precoComponente')

            print(f"Componente: {id} {novoCatComponente} {novoNomeComponente} {novaDescricaoComponente} {novoPrecoMedioComponente}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Componentes_update(%s, %s, %s, %s, %s)', [id, novoCatComponente, novoNomeComponente, novaDescricaoComponente, novoPrecoMedioComponente])
                connection.commit()
                print("Componente editado com sucesso!")

            response_data = {'mensagem': 'Componente editado com sucesso', 'refresh': True}
            return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'erro': 'Erro ao decodificar JSON'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)




#---------------------------------------------------------------------------------------------

def encomendas_componentes(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_encomendas_componentes_list()')
            resultados = cursor.fetchall()
            encomendas_componentes = []

            for resultado in resultados:
                if len(resultado) >= 4:
                    encomenda_componente = {
                        'ID_ENCOMENDA': resultado[0],
                        'ID_COMPONENTE': resultado[1],
                        'QUANTIDADE_EC': resultado[2],
                        'PRECOUNIDADE_EC': resultado[3],
                    }
                    encomendas_componentes.append(encomenda_componente)
                else:
                    print(f"Unexpected tuple length: {len(resultado)}")

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            encomendas_componentes = []

    context = {'encomendas_componentes': encomendas_componentes,
            'tem_permissao': tem_permissao,
}
    return render(request, 'encomenda_componentes.html', context)

def adicionar_encomenda_componente(request):
    if request.method == 'POST':
        id_encomenda = int(request.POST.get('id_encomenda'))
        id_componente = int(request.POST.get('id_componente'))
        quantidade_ec = int(request.POST.get('quantidade_ec'))
        precounidade_ec = int(request.POST.get('precounidade_ec'))

        print(f"Encomenda de componente: {id_encomenda} {id_componente} {quantidade_ec} {precounidade_ec}")

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Encomendas_componentes_create(%s, %s, %s, %s)',
                               [id_encomenda, id_componente, quantidade_ec, precounidade_ec])
                connection.commit()
                print("Encomenda de componente adicionada com sucesso!")

                return redirect('encomendas_componentes')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                print("Erro ao adicionar encomenda de componente!")
                return redirect('encomendas_componentes')

    return HttpResponse("Erro ao adicionar encomenda de componente!")

def eliminar_encomenda_componente(request, id_encomenda, id_componente):
    if id_encomenda is not None:
        id_encomenda = int(id_encomenda)
    if id_componente is not None:
        id_componente = int(id_componente)

    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_Encomendas_componentes_delete(%s, %s)', [id_encomenda, id_componente])
            connection.commit()
            print("Encomenda de componente eliminada com sucesso!")

            return redirect('encomendas_componentes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao eliminar encomenda de componente!")

    return HttpResponse("Erro ao eliminar encomenda de componente!")

def editar_encomenda_componente(request, id_encomenda, id_componente):
    if id_encomenda is not None:
        id_encomenda = int(id_encomenda)
    if id_componente is not None:
        id_componente = int(id_componente)

    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)
            nova_quantidade_ec= dados_json.get('quantidadeEc')
            novo_precounidade_ec_str =dados_json.get('precoUnidadeEc')
            novo_precounidade_ec = Decimal(novo_precounidade_ec_str) if novo_precounidade_ec_str is not None else None

            print(f"Encomenda de componente: {id_encomenda} {id_componente} {nova_quantidade_ec} {novo_precounidade_ec}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Encomendas_componentes_update(%s, %s, %s, %s)',
                               [id_encomenda, id_componente, nova_quantidade_ec, novo_precounidade_ec])
                connection.commit()
                print("Encomenda de componente editada com sucesso!")

                response_data = {'mensagem': 'Encomenda de componente editada com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'erro': 'Erro ao decodificar JSON'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)




#------------------------------------------------------------------------------


def armazens(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_armazem_list()')
            resultados = cursor.fetchall()
            armazens = []

            for resultado in resultados:
                armazem = {
                    'ID_ARMAZEM': resultado[0],
                    'NOME_ARMAZEM': resultado[1],
                    'MORADA_ARMAZEM': resultado[2],
                    'EMAIL_ARMAZEM': resultado[3],
                    'CONTACTO_ARMAZEM': resultado[4],
                    'ID_FUNCIONARIO': resultado[5],
                }
                armazens.append(armazem)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            armazens = []

    context = {'armazens': armazens,        'tem_permissao': tem_permissao,
}
    return render(request, 'armazens.html', context)

def adicionar_armazem(request):
    if request.method == 'POST':
        nome_armazem = request.POST.get('add_Nome_Armazem')
        morada_armazem = request.POST.get('add_Morada_Armazem')
        email_armazem = request.POST.get('add_Email_Armazem')
        contacto_armazem = request.POST.get('add_Contacto_Armazem')
        id_funcionario = request.POST.get('add_ID_Funcionario')

        print(f"Armazém: {nome_armazem} {morada_armazem} {email_armazem} {contacto_armazem} {id_funcionario}")

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Armazem_create(%s, %s, %s, %s, %s)',
                               [nome_armazem, morada_armazem, email_armazem, contacto_armazem, id_funcionario])
                connection.commit()
                print("Armazém adicionado com sucesso!")

                return redirect('armazens')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar o Armazém!")

    return HttpResponse("Erro ao adicionar o Armazém!")

def editar_armazem(request, id_armazem):
    if request.method == 'POST':
        if id_armazem is not None:
            id_armazem = int(id_armazem)
        try:
            data_json = json.loads(request.body)
            
            nome_armazem = data_json.get('nome_armazem')
            morada_armazem = data_json.get('morada_armazem')
            email_armazem = data_json.get('email_armazem')
            contacto_armazem = data_json.get('contacto_armazem')
            id_funcionario = data_json.get('id_funcionario')

            print(f"Armazém: {id_armazem} {nome_armazem} {morada_armazem} {email_armazem} {contacto_armazem} {id_funcionario}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Armazem_update(%s,%s, %s, %s, %s, %s)',
                               [id_armazem, nome_armazem, morada_armazem, email_armazem, contacto_armazem, id_funcionario])
                connection.commit()
                print("Armazém atualizado com sucesso!")

                return redirect('armazens')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")

    return HttpResponse("Erro ao atualizar o Armazém!")

def excluir_armazem(request, id_armazem):
    with connection.cursor() as cursor:
        if id_armazem is not None:
            id_armazem = int(id_armazem)
           
        try:
            cursor.execute('CALL sp_armazem_delete(%s)', [id_armazem])
            connection.commit()
            print("Armazém excluído com sucesso!")

            return redirect('armazens')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir o Armazém!")

    return HttpResponse("Erro ao excluir o Armazém!")





#-----------------------------------------------------------------------------------------------------------

def equipamento(request, id):
    return render(request, 'equipamento_detalhes.html')

#-----------------------------------------------------------------------------------------------------------


def categorias_componentes(request):
    # If it's an API request for the dropdown
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        with connection.cursor() as cursor:
            try:
                cursor.execute('SELECT * FROM public.fn_categoriacomponentes_list()')
                resultados = cursor.fetchall()
                print("Raw results:", resultados)  # Debug print
                
                categorias = []
                for resultado in resultados:
                    categoria = {
                        'id': resultado[0],
                        'nome': resultado[1]
                    }
                    categorias.append(categoria)
                    print("Added categoria:", categoria)  # Debug print
                
                print("Final categorias list:", categorias)  # Debug print
                return JsonResponse(categorias, safe=False)
            except Exception as e:
                print(f"Error fetching categorias for dropdown: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)

    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False

    with connection.cursor() as cursor:
        try:
            # Use SELECT to call the function and retrieve results
            cursor.execute('SELECT * FROM public.fn_categoriacomponentes_list()')

            # Retrieve all results
            resultados = cursor.fetchall()

            # Print the results
            for resultado in resultados:
                print(resultado)
            
            # Create a list of dictionaries from the results
            categorias_componentes = []
            for resultado in resultados:
                # Check if the tuple has the expected number of elements
                if len(resultado) >= 3:  # Assuming ID_CATCOMPONENTES is the first column
                    categoria_componente = {
                        'ID_CATCOMPONENTES': resultado[0],  # Change index if necessary
                        'NOME_CATCOMPONENTES': resultado[1],
                        'DESCRICAO_CATCOMPONENTES': resultado[2],
                    }
                    categorias_componentes.append(categoria_componente)
                else:
                    print(f"Unexpected tuple length: {len(resultado)}")

        except Exception as e:
            # Handle exceptions (print or log the error, handle as needed)
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            categorias_componentes = []

    context = {
        'categorias_componentes': categorias_componentes,
        'tem_permissao': tem_permissao,
    }
    return render(request, 'categorias_componentes.html', context)

def adicionar_categoria_componentes(request):
    if request.method == 'POST':
        nome_categoria = request.POST.get('nome_categoria')
        descricao_categoria = request.POST.get('descricao_categoria')

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_CATEGORIACOMPONENTES_create(%s, %s)', [nome_categoria, descricao_categoria])
                connection.commit()
                print("Categoria de componentes adicionada com sucesso!")

                return redirect('categorias_componentes')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar categoria de componentes!")

    return HttpResponse("Erro ao adicionar categoria de componentes!")

# View para editar uma Categoria de Componentes
def editar_categoria_componentes(request, id_categoria):
    if id_categoria is not None:
        id_categoria = int(id_categoria)

    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)
            nome_categoria = dados_json.get('nomeCategoria')	
            descricao_categoria = dados_json.get('descricaoCategoria')

            print(f"Categoria de componentes: {id_categoria} {nome_categoria} {descricao_categoria}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_CATEGORIACOMPONENTES_update(%s, %s, %s)',
                               [id_categoria, nome_categoria, descricao_categoria])
                connection.commit()
                print("Categoria de componentes atualizada com sucesso!")

                return redirect('categorias_componentes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")

    return HttpResponse("Erro ao atualizar categoria de componentes!")

# View para excluir uma Categoria de Componentes
def excluir_categoria_componentes(request, id_categoria):
    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_CATEGORIACOMPONENTES_delete(%s)', [id_categoria])
            connection.commit()
            print("Categoria de componentes excluída com sucesso!")

            return redirect('categorias_componentes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir categoria de componentes!")

    return HttpResponse("Erro ao excluir categoria de componentes!")

#-----------------------------------------------------------------------------------------------------------


def stock_equipamentos(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_stockequipamentos_list()')
            resultados = cursor.fetchall()
            stock_equipamentos = []
             
            print(resultados)

            for resultado in resultados:
                stock_equipamento = {
                    'ID_ARMAZEM': resultado[0],
                    'ID_EQUIP': resultado[1],
                    'QUANTIDADE_STOCKEQUIP': resultado[2],
                }
                stock_equipamentos.append(stock_equipamento)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            stock_equipamentos = []

    context = {'stock_equipamentos': stock_equipamentos,
            'tem_permissao': tem_permissao,
}
    return render(request, 'equipamento_stock.html', context)

def adicionar_stock_equipamento(request):
    if request.method == 'POST':
        id_armazem = int(request.POST.get('id_armazem'))
        id_equip = int(request.POST.get('id_equip'))
        quantidade_stockequip = int(request.POST.get('quantidade_stockequip'))

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Stockequipamentos_create(%s, %s, %s)',
[id_armazem, id_equip, quantidade_stockequip])
                connection.commit()
                print("stock de equipamento adicionado com sucesso!")
                return redirect('stock_equipamentos')

            

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                print("Erro ao adicionar stock de equipamento!")

    return HttpResponse("Erro ao adicionar stock de equipamento!")

def editar_stock_equipamento(request, id_armazem, id_equip):
    if id_armazem is not None:
        id_armazem = int(id_armazem)
    if id_equip is not None:
        id_equip = int(id_equip)

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)

            nova_quantidade_stockequip_str = json_data.get('quantidadeStockequip')
            nova_quantidade_stockequip = int(nova_quantidade_stockequip_str) if nova_quantidade_stockequip_str is not None else None

            print(f"Stock de equipamento: {id_armazem} {id_equip} {nova_quantidade_stockequip}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Stockequipamentos_update(%s, %s, %s)',
                               [id_armazem, id_equip, nova_quantidade_stockequip])
                connection.commit()
                print("stock de equipamento editado com sucesso!")

                response_data = {'mensagem': 'stock de equipamento editado com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'erro': 'Erro ao atualizar o stock de equipamento'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

def excluir_stock_equipamento(request, id_armazem, id_equip):
    if id_armazem is not None:
        id_armazem = int(id_armazem)
    if id_equip is not None:
        id_equip = int(id_equip)

    print("Stock de equipamento: ", id_armazem, id_equip)
    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_Stockequipamentos_delete(%s, %s)', [id_armazem, id_equip])
            connection.commit()
            print("stock de equipamento excluído com sucesso!")

            return redirect('stock_equipamentos')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir stock de equipamento!")

    return HttpResponse("Erro ao excluir stock de equipamento!")


#-----------------------------------------------------------------------------------------------------------


def fornecedores(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_fornecedores_list()')
            resultados = cursor.fetchall()
            fornecedores = []

            for resultado in resultados:
                fornecedor = {
                    'ID_FORNECEDOR': resultado[0],
                    'NOME_FORNECEDOR': resultado[1],
                    'MORADA_FORNECEDOR': resultado[2],
                    'EMAIL_FORNECEDOR': resultado[3],
                    'CONTACTO_FORNECEDOR': resultado[4],
                }
                fornecedores.append(fornecedor)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            fornecedores = []

    context = {'fornecedores': fornecedores,
            'tem_permissao': tem_permissao,
}
    return render(request, 'fornecedores.html', context)

# View para adicionar um fornecedor
def adicionar_fornecedor(request):
    if request.method == 'POST':
        nome_fornecedor = request.POST.get('nome_fornecedor')
        morada_fornecedor = request.POST.get('morada_fornecedor')
        email_fornecedor = request.POST.get('email_fornecedor')
        contacto_fornecedor_str = request.POST.get('contacto_fornecedor')

        contacto_fornecedor = Decimal(contacto_fornecedor_str) if contacto_fornecedor_str is not None else None

        print(f"Fornecedor: {nome_fornecedor} {morada_fornecedor} {email_fornecedor} {contacto_fornecedor}")
       
        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_fornecedores_create(%s, %s, %s, %s)',
                               [nome_fornecedor, morada_fornecedor, email_fornecedor, contacto_fornecedor])
                connection.commit()
                print("Fornecedor adicionado com sucesso!")

                return redirect('fornecedores')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar fornecedor!")

    return HttpResponse("Erro ao adicionar fornecedor!")

# View para editar um fornecedor
def editar_fornecedor(request, id):
    if id is not None:
        id = int(id)

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)

            nome_fornecedor = json_data.get('nomeFornecedor')
            morada_fornecedor = json_data.get('moradaFornecedor')
            email_fornecedor = json_data.get('emailFornecedor')
            contacto_fornecedor_str = json_data.get('contactoFornecedor')

            contacto_fornecedor = Decimal(contacto_fornecedor_str) if contacto_fornecedor_str is not None else None

            print(f"Fornecedor: {id} {nome_fornecedor} {morada_fornecedor} {email_fornecedor} {contacto_fornecedor}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Fornecedores_update(%s, %s, %s, %s, %s)',
                               [id, nome_fornecedor, morada_fornecedor, email_fornecedor, contacto_fornecedor])
                connection.commit()
                print("Fornecedor editado com sucesso!")

                response_data = {'mensagem': 'Fornecedor editado com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'erro': 'Erro ao atualizar o fornecedor'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

# View para excluir um fornecedor
def excluir_fornecedor(request, id):
    with connection.cursor() as cursor:
        print("Fornecedor: ", id)
        try:
            cursor.execute('CALL sp_Fornecedores_delete(%s)', [id])
            connection.commit()
            print("Fornecedor excluído com sucesso!")

            return redirect('fornecedores')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir fornecedor!")

    return HttpResponse("Erro ao excluir fornecedor!")



#-----------------------------------------------------------------------------------------------------------
def fornecedores_componentes(request):

    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_fornecedores_componentes_list()')
            resultados = cursor.fetchall()
            fornecedores_componentes = []

            for resultado in resultados:
                fornecedor_componente = {
                    'ID_COMPONENTE': resultado[0],
                    'ID_FORNECEDOR': resultado[1],
                }
                fornecedores_componentes.append(fornecedor_componente)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            fornecedores_componentes = []

    context = {'fornecedores_componentes': fornecedores_componentes,
            'tem_permissao': tem_permissao,
}
    return render(request, 'fornecedores_componentes.html', context)

def adicionar_fornecedor_componente(request):
    if request.method == 'POST':
        id_componente = int(request.POST.get('id_componente'))
        id_fornecedor = int(request.POST.get('id_fornecedor'))

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Fornecedores_componentes_create(%s, %s)',
                               [id_componente, id_fornecedor])
                connection.commit()
                print("Fornecedor componente adicionado com sucesso!")

                return redirect('fornecedores_componentes')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar fornecedor componente!")

    return HttpResponse("Erro ao adicionar fornecedor componente!")

def editar_fornecedor_componente(request, id_componente, id_fornecedor):
    if id_componente is not None:
        id_componente = int(id_componente)
    if id_fornecedor is not None:
        id_fornecedor = int(id_fornecedor)

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)

            nova_id_componente_str = json_data.get('id_componente_novo')
            nova_id_fornecedor_str = json_data.get('id_fornecedor_novo')
            nova_id_componente = int(nova_id_componente_str) if nova_id_componente_str is not None else None
            nova_id_fornecedor = int(nova_id_fornecedor_str) if nova_id_fornecedor_str is not None else None

            print(f"Fornecedor componente: {id_componente} {id_fornecedor} {nova_id_componente} {nova_id_fornecedor}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Fornecedores_componentes_update(%s, %s, %s, %s)',
                               [id_componente, id_fornecedor, nova_id_componente, nova_id_fornecedor])
                connection.commit()

            response_data = {'mensagem': 'fornecedor componente editado com sucesso'}
            print("Fornecedor componente editado com sucesso!")
            return JsonResponse(response_data)

        except Exception as e:
            print(traceback.format_exc())  # Imprime a exceção específica
            return JsonResponse({'erro': 'Erro ao atualizar o fornecedor componente'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

def excluir_fornecedor_componente(request, id_componente, id_fornecedor):
    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_Fornecedores_componentes_delete(%s, %s)', [id_componente, id_fornecedor])
            connection.commit()
            print("Fornecedor componente excluído com sucesso!")

            return redirect('fornecedores_componentes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir fornecedor componente!")

    return HttpResponse("Erro ao excluir fornecedor componente!")
#-----------------------------------------------------------------------------------------------------------
def funcionarios(request):

    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_funcionarios_list()')
            resultados = cursor.fetchall()
            funcionarios = []

            for resultado in resultados:
                funcionario = {
                    'ID_FUNCIONARIO': resultado[0],
                    'NOME': resultado[1],
                    'DATANASC': resultado[2],
                    'NIF': resultado[3],
                    'EMAIL': resultado[4],
                    'CONTACTO': resultado[5],
                    'MORADA': resultado[6],
                    'CARGO': resultado[7],
                }
                funcionarios.append(funcionario)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            funcionarios = []

    context = {'funcionarios': funcionarios,
            'tem_permissao': tem_permissao,
}
    return render(request, 'funcionarios.html', context)

# View para adicionar um funcionário
def adicionar_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        datanasc = request.POST.get('datanasc')
        nif = request.POST.get('nif')
        email = request.POST.get('email')
        contacto = request.POST.get('contacto')
        morada = request.POST.get('morada')
        cargo = request.POST.get('cargo')

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Funcionarios_create(%s, %s, %s, %s, %s, %s, %s)',
                               [nome, datanasc, nif, email, contacto, morada, cargo])
                connection.commit()
                print("Funcionário adicionado com sucesso!")

                return redirect('funcionarios')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar funcionário!")

    return HttpResponse("Erro ao adicionar funcionário!")

# View para editar um funcionário
def editar_funcionario(request, id_funcionario):
    if id_funcionario is not None:
        id_funcionario = int(id_funcionario)

    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)

            nome = dados_json.get('nome')
            datanasc_str = dados_json.get('datanasc')
            nif = dados_json.get('nif')
            email = dados_json.get('email')
            contacto = dados_json.get('contacto')
            morada = dados_json.get('morada')
            cargo = dados_json.get('cargo')

            datanasc = datetime.strptime(datanasc_str, '%Y-%m-%d').date()

            print(f"Funcionário: {id_funcionario} {nome} {datanasc} {nif} {email} {contacto} {morada} {cargo}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Funcionarios_update(%s, %s, %s, %s, %s, %s, %s, %s)',
                               [id_funcionario, nome, datanasc, nif, email, contacto, morada, cargo])
                connection.commit()
                print("Funcionário editado com sucesso!")

                response_data = {'mensagem': 'Funcionário editado com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'erro': 'Erro ao atualizar o funcionário'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

# View para excluir um funcionário
def excluir_funcionario(request, id_funcionario):
    with connection.cursor() as cursor:
        if id_funcionario is not None:
            id_funcionario = int(id_funcionario)
        try:
            cursor.execute('CALL sp_funcionarios_delete(%s)', [id_funcionario])
            connection.commit()
            print("Funcionário excluído com sucesso!")

            return redirect('funcionarios')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir funcionário!")

    return HttpResponse("Erro ao excluir funcionário!")
#-----------------------------------------------------------------------------------------------------------
def lotes(request):
 
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
     
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_lotes_list()')
            resultados = cursor.fetchall()
            lotes = []

            for resultado in resultados:
                lote = {
                    'ID_LOTE': resultado[0],
                    'ID_PRODUCAO': resultado[1],
                    'ID_TIPOEQUIP': resultado[2],
                    'QUANTIDADE_PRODUTOS': resultado[3],
                    'ID_ARMAZEM': resultado[4],
                    'ID_FUNCIONARIO': resultado[5],
                }
                lotes.append(lote)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            lotes = []

    context = {'lotes': lotes,        'tem_permissao': tem_permissao,
}
    return render(request, 'lotes.html', context)

def adicionar_lote(request):
        if request.method == 'POST':
            id_producao_str = request.POST.get('add_ID_Producao')
            id_tipoEquip_str = request.POST.get('add_ID_tipoEquip')
            quantidade_produtos_str = request.POST.get('add_Quantidade_Produtos')
            id_armazem_str = request.POST.get('add_ID_Armazem')
            id_funcionario_str = request.POST.get('add_ID_Funcionario')

        # Verifique se os campos obrigatórios estão presentes
        if id_producao_str and id_tipoEquip_str and quantidade_produtos_str and id_armazem_str and id_funcionario_str:
            # Converta para inteiros
            id_producao = int(id_producao_str)
            id_tipoEquip = int(id_tipoEquip_str)
            quantidade_produtos = int(quantidade_produtos_str)
            id_armazem = int(id_armazem_str)
            id_funcionario = int(id_funcionario_str)

            print(f"Lote: {id_producao} {id_tipoEquip} {quantidade_produtos} {id_armazem} {id_funcionario}")

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_lotes_create(%s, %s, %s, %s, %s)',
                               [id_producao, id_tipoEquip, quantidade_produtos, id_armazem, id_funcionario])
                connection.commit()
                print("Lote adicionado com sucesso!")

                return redirect('lotes')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar lote!")

        return HttpResponse("Erro ao adicionar lote!")

def editar_lote(request, id_lote):
    print(f"ID do lote a editar: {id_lote}")

    if request.method == 'POST':
        #print("Recebido POST")
        try:
            id_producao_str = request.POST.get('id_producao')
            id_tipoequip_str = request.POST.get('id_tipoEquip')
            quantidade_produtos_str = request.POST.get('quantidade_produtos')
            id_armazem_str = request.POST.get('id_armazem')
            id_funcionario_str = request.POST.get('id_funcionario')

            print(f"Valores recebidos: {id_producao_str}, {id_tipoequip_str}, {quantidade_produtos_str}, {id_armazem_str}, {id_funcionario_str}")

            # Converta para inteiros
            id_producao = int(id_producao_str)
            id_tipoequip = int(id_tipoequip_str)
            quantidade_produtos = int(quantidade_produtos_str)
            id_armazem = int(id_armazem_str)
            id_funcionario = int(id_funcionario_str)

            print(f"Valores recebidos: {id_lote}, {id_producao}, {id_tipoequip}, {quantidade_produtos}, {id_armazem}, {id_funcionario}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_lotes_update(%s, %s, %s, %s, %s, %s)',
                               [id_lote, id_producao, id_tipoequip, quantidade_produtos, id_armazem, id_funcionario])
                connection.commit()

            print("Lote editado com sucesso!")
            response_data = {'mensagem': 'Lote editado com sucesso', 'refresh': True}
            return JsonResponse(response_data)

        except ValueError as ve:
            return JsonResponse({'erro': f'Erro ao converter valores: {ve}'}, status=400)
        except Exception as e:
            return JsonResponse({'erro': f'Erro ao editar o lote: {e}'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)


def eliminar_lote(request, id_lote):
    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_Lotes_delete(%s)', [id_lote])
            connection.commit()
            print("Lote excluído com sucesso!")

            return redirect('lotes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir lote!")

    return HttpResponse("Erro ao excluir lote!")
#-----------------------------------------------------------------------------------------------------------

def adicionar_maode_obra(request):

    if request.method == 'POST':
        nome_mo = request.POST.get('nome_maodeobra')
        desc_mo = request.POST.get('desc_maodeobra')
        custo_mo = request.POST.get('custo_maodeobra')

        print(f"Mão de obra: {nome_mo} {desc_mo} {custo_mo}")

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_maodeobra_create(%s, %s, %s)',
                               [nome_mo, desc_mo, custo_mo])
                connection.commit()
                print("Mão de obra adicionada com sucesso!")

                return redirect('maodeobra')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar mão de obra!")

    return HttpResponse("Erro ao adicionar mão de obra!")

# list
def maodeobra(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_maodeobra_list()')
            resultados = cursor.fetchall()
            maodeobras = []

            for resultado in resultados:
                maodeobra = {
                    'ID_MO': resultado[0],
                    'NOME_MO': resultado[1],
                    'DESC_MO': resultado[2],
                    'CUSTO_MO': resultado[3],
                }
                maodeobras.append(maodeobra)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            maodeobras = []

    context = {'maodeobras': maodeobras,
            'tem_permissao': tem_permissao,
}
    return render(request, 'maodeobra.html', context)

# Update
def editar_maodeobra(request, id_mo):
    if request.method == 'POST':
        if id_mo is not None:
            id_mo = int(id_mo)

        try:
            novo_nome_mo_str = request.POST.get('nomeMaodeObra')
            novo_nome_mo = novo_nome_mo_str if novo_nome_mo_str is not None else None
            nova_desc_mo = request.POST.get('descMaodeObra')
            novo_custo_mo_str = request.POST.get('custoMaodeObra')
            novo_custo_mo = Decimal(novo_custo_mo_str) if novo_custo_mo_str is not None else None

            print(f"Valores recebidos: {id_mo}, {novo_nome_mo}, {nova_desc_mo}, {novo_custo_mo}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_maodeobra_update(%s, %s, %s, %s)',
                               [id_mo, novo_nome_mo, nova_desc_mo, novo_custo_mo])
                connection.commit()
                print("Mão de obra editada com sucesso!")

                return redirect('maodeobra')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            return redirect('maodeobra')
        

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

# Delete
def excluir_maodeobra(request, id_mo):
    with connection.cursor() as cursor:
        if id_mo is not None:
            id_mo = int(id_mo)
        try:
            cursor.execute('CALL sp_Maodeobra_delete(%s)', [id_mo])
            connection.commit()
            print("Mão de obra excluída com sucesso!")

            return redirect('maodeobra')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir mão de obra!")

    return HttpResponse("Erro ao excluir mão de obra!") 

#-----------------------------------------------------------------------------------------------------------
def producao_diaria(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False

    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_producaodiaria_list()')
            resultados = cursor.fetchall()
            producoes_diarias = []

            print(f"Resultados: {resultados}")

            for resultado in resultados:
                producao_diaria = {
                    'ID_PRODUCAO': resultado[0],
                    'DATA_PRODUCAO': resultado[1],
                    'ID_ARMAZEM': resultado[2],
                }
                producoes_diarias.append(producao_diaria)

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            producoes_diarias = []

    context = {
        'producoes_diarias': producoes_diarias,
        'tem_permissao': tem_permissao,
    }
    return render(request, 'producao_diaria.html', context)

def adicionar_producao_diaria(request):
    if request.method == 'POST':
        data_producao = request.POST.get('data_producao')
        id_armazem = int(request.POST.get('id_armazem'))

        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Producao_diaria_create(%s, %s)', [data_producao, id_armazem])
                connection.commit()
                print("Produção diária adicionada com sucesso!")

                return redirect('producao_diaria')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar produção diária!")

    return HttpResponse("Erro ao adicionar produção diária!")

def editar_producao_diaria(request, id_producao):
    if id_producao is not None:
        id_producao = int(id_producao)

    if request.method == 'POST':
        try:
            # Recupera o corpo da requisição como JSON
            data = json.loads(request.body)
            
            data_producao_str = data.get('dataProducao')

            print(f"Data de produção: {data_producao_str}")
            id_armazem = data.get('idArmazem')
            
            # Convertendo a data para datetime
            data_producao = datetime.strptime(data_producao_str, '%Y-%m-%d').date()

            print(f"Produção diária: {id_producao} {data_producao} {id_armazem}")

            with connection.cursor() as cursor:
                cursor.execute('CALL sp_producao_diaria_update(%s, %s, %s)', [id_producao, data_producao, id_armazem])
                connection.commit()
                print("Produção diária atualizada com sucesso!")

                response_data = {'mensagem': 'Produção diária atualizada com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except Exception as e:
            print(traceback.format_exc())  # Imprime a exceção específica
            return JsonResponse({'erro': 'Erro ao atualizar a produção diária'}, status=400)

    return JsonResponse({'erro': 'Método não permitido'}, status=405)
def excluir_producao_diaria(request, id_producao):
    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_Producao_diaria_delete(%s)', [id_producao])
            connection.commit()
            print("Produção diária excluída com sucesso!")

            return redirect('producao_diaria')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao excluir produção diária!")

    return HttpResponse("Erro ao excluir produção diária!")

#-----------------------------------------------------------------------------------------------------------

def stockcomponentes(request):

    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False

    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_stockcomponentes_list()')
            resultados = cursor.fetchall()
            
            stockcomponentes = []
            for resultado in resultados:
                if len(resultado) >= 3:
                    stockcomponente = {
                        'ID_ARMAZEM': resultado[0],
                        'ID_COMPONENTE': resultado[1],
                        'QUANTIDADE_STOCKCOMP': resultado[2],
                    }
                    stockcomponentes.append(stockcomponente)
                else:
                    print(f"Unexpected tuple length: {len(resultado)}")

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            stockcomponentes = []

    context = {
        'stockcomponentes': stockcomponentes,
        'tem_permissao': tem_permissao,
    }
    return render(request, 'stockcomponentes.html', context)

def adicionar_stockcomponente(request):
    if request.method == 'POST':
        id_armazem = int(request.POST.get('id_armazem'))
        id_componente = int(request.POST.get('id_componente'))
        quantidade_stockcomp = int(request.POST.get('quantidade_stockcomp'))


        print (f"Stock componente: {id_armazem} {id_componente} {quantidade_stockcomp}")
        with connection.cursor() as cursor:
            try:
                cursor.execute('CALL sp_Stockcomponentes_create(%s, %s, %s)', [id_armazem, id_componente, quantidade_stockcomp])
                connection.commit()
                print("Stock componente adicionado com sucesso!")

                return redirect('stockcomponentes')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar stock componente!")

    return HttpResponse("Erro ao adicionar stock componente!")

def eliminar_stockcomponente(request, id_armazem, id_componente):
    if id_armazem is not None:
        id_armazem = int(id_armazem)
    if id_componente is not None:
        id_componente = int(id_componente)
        

    with connection.cursor() as cursor:
        try:
            cursor.execute('CALL sp_Stockcomponentes_delete(%s, %s)', [id_armazem, id_componente])
            connection.commit()
            print("Stock componente eliminado com sucesso!")

            return redirect('stockcomponentes')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao eliminar stock componente!")

    return HttpResponse("Erro ao eliminar stock componente!")

def editar_stockcomponente(request, id_armazem, id_componente):
    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)

            nova_quantidade_stockcomp = dados_json.get('quantidade_stockcomp')

            print(f"Stock componente: {id_armazem} {id_componente} {nova_quantidade_stockcomp}")

            # Execute o procedimento armazenado para editar o stock componente
            with connection.cursor() as cursor:
                cursor.execute('CALL sp_stockcomponentes_update(%s, %s, %s)', [id_armazem, id_componente, nova_quantidade_stockcomp])
                connection.commit()
                print("Stock componente editado com sucesso!")

                # Exemplo de retorno de uma resposta de sucesso
                response_data = {'mensagem': 'Stock componente editado com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'erro': 'Erro ao decodificar JSON'}, status=400)

    # Se não for uma solicitação POST, retorne uma resposta de erro
    return JsonResponse({'erro': 'Método não permitido'}, status=405)


#-----------------------------------------------------------------------------------------------------------

def tipoequipamentos(request):

    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")

    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False

    with connection.cursor() as cursor:
        try:
            # Use SELECT to call the function and retrieve results
            cursor.execute('SELECT * FROM public.fn_tipoequipamentos_list()')

            # Retrieve all results
            resultados = cursor.fetchall()

            # Print the results
            for resultado in resultados:
                print(resultado)

            # Create a list of dictionaries from the results
            tipoequipamentos = []
            for resultado in resultados:
                # Check if the tuple has the expected number of elements
                if len(resultado) >= 2:
                    tipoequipamento = {
                        'ID_TIPOEQUIP': resultado[0],
                        'nome': resultado[1],
                        'descricao': resultado[2],
                    }
                    tipoequipamentos.append(tipoequipamento)
                else:
                    print(f"Unexpected tuple length: {len(resultado)}")

        except Exception as e:
            # Handle exceptions (print or log the error, handle as needed)
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            tipoequipamentos = []

    context = {
        'tipoequipamentos': tipoequipamentos,
        'tem_permissao': tem_permissao,
    }
    return render(request, 'tipoequipamentos.html', context)

# View para adicionar um novo tipo de equipamento
def adicionar_tipoequipamento(request):
    if request.method == 'POST':
        nome_tipoequip = request.POST.get('nome_tipoequip')
        desc_tipoequip = request.POST.get('desc_tipoequip')

        with connection.cursor() as cursor:
            try:
                print(f"Tipo de Equipamento : {nome_tipoequip} {desc_tipoequip}")
                cursor.execute('CALL sp_Tipoequipamentos_create(%s, %s)', [nome_tipoequip, desc_tipoequip])
                connection.commit()
                print("Tipo de equipamento adicionado com sucesso!")

                return redirect('tipoequipamentos')

            except Exception as e:
                print(f"Exception type: {type(e)}")
                print(f"Exception message: {str(e)}")
                connection.rollback()
                print("Erro ao adicionar tipo de equipamento!")

    return HttpResponse("Erro ao adicionar tipo de equipamento!")

# View para editar um tipo de equipamento existente
def editar_tipoequipamento(request, id_tipoequip):
    if id_tipoequip is not None:
        id_tipoequip = int(id_tipoequip)


    if request.method == 'POST':
        try:
            dados_json = json.loads(request.body)

            novoNomeTipoEquip = dados_json.get('nomeTipoEquipamento')
            novaDescTipoEquip = dados_json.get('descTipoEquipamento')

            print(f"Tipo de Equipamento : {novoNomeTipoEquip} {novaDescTipoEquip}")

            # Lógica para editar o tipo de equipamento

            # Execute o procedimento armazenado para editar o tipo de equipamento
            with connection.cursor() as cursor:
                cursor.execute('CALL sp_Tipoequipamentos_update(%s, %s, %s)', [id_tipoequip, novoNomeTipoEquip, novaDescTipoEquip])
                # Confirme a transação
                connection.commit()
                print("Tipo de equipamento editado com sucesso!")

                # Exemplo de retorno de uma resposta de sucesso
                response_data = {'mensagem': 'Tipo de equipamento editado com sucesso', 'refresh': True}
                return JsonResponse(response_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'erro': 'Erro ao decodificar JSON'}, status=400)

    # Se não for uma solicitação POST, retorne uma resposta de erro
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

# View para excluir um tipo de equipamento existente
def eliminar_tipoequipamento(request, id_tipoequip):
    with connection.cursor() as cursor:
        try:
            print("Tipo de Equipamento : ", id_tipoequip)
            cursor.execute('CALL sp_Tipoequipamentos_delete(%s)', [id_tipoequip])

            connection.commit()
            print("Tipo de equipamento eliminado com sucesso!")

            return redirect('tipoequipamentos')

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            connection.rollback()
            print("Erro ao eliminar tipo de equipamento!")

    return HttpResponse("Erro ao eliminar tipo de equipamento!")



#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------


def user(request):
        # Substitua esta lista com os dados reais da sua base de dados
    utilizadores = [
        {'id': 1, 'nome': 'João Silva', 'email': 'joao@example.com', 'telefone': '(123) 456-7890', 'nif': '123456789'},
        # Adicione mais utilizadores conforme necessário
    ]
    context = {'utilizadores': utilizadores}
    return render(request, 'users.html', context)

def editar_user(request, id):
    exemplo_utilizador = {
        'id': id,
        'nome': 'Utilizador Exemplo',
        'email': 'exemplo@example.com',
        'telefone': '(123) 456-7890',
        'nif': '123456789'
    }

    if request.method == 'POST':
        {}


    context = {'utilizador': exemplo_utilizador}
    return render(request, 'editar_user.html', context)




def cliente(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")
    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
        
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM public.fn_clientes_list()')

            resultados = cursor.fetchall()

            clientes = []

            for resultado in resultados:
                if len(resultado) >= 7:
                    cliente = {
                        'id': resultado[0],
                        'nome': resultado[1],
                        'datanasc': resultado[2],
                        'morada': resultado[3],
                        'nif': resultado[4],
                        'email': resultado[5],
                        'contacto': resultado[6],
                    }
                    clientes.append(cliente)
                else:
                    print(f"Unexpected tuple length: {len(resultado)}")

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            clientes = []

    context = {
        'clientes': clientes,
        'tem_permissao': tem_permissao,  # Certifique-se de definir tem_permissao
    }
    return render(request, 'cliente.html', context)

def adicionar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        datanasc = request.POST.get('datanasc')
        morada = request.POST.get('morada')
        nif = request.POST.get('nif')
        email = request.POST.get('email')
        contacto = request.POST.get('contacto')

        with connection.cursor() as cursor:
            cursor.execute('CALL sp_Clientes_create(%s, %s, %s, %s, %s, %s)',
                           [nome, datanasc, morada, nif, email, contacto])
            connection.commit()

        return redirect('cliente')

    return HttpResponse("Erro ao adicionar cliente!")

def editar_cliente(request, id):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        datanasc = request.POST.get('datanasc')
        morada = request.POST.get('morada')
        nif = request.POST.get('nif')
        email = request.POST.get('email')
        contacto = request.POST.get('contacto')

        with connection.cursor() as cursor:
            cursor.execute('CALL sp_Clientes_update(%s, %s, %s, %s, %s, %s, %s)',
                           [id, nome, datanasc, morada, nif, email, contacto])
            connection.commit()

        return redirect('cliente')

    return HttpResponse("Erro ao editar cliente!")

def excluir_cliente(request, id):
    if id is not None:
        id = int(id)

    with connection.cursor() as cursor:
        cursor.execute('CALL sp_Clientes_delete(%s)', [id])
        connection.commit()

    return redirect('cliente')


def fatura(request):
    id_nivel = LocalStorage.get_id_nivel(request)
    print(f"ID do nível recuperado da sessão: {id_nivel}")
    if id_nivel == 1:
        tem_permissao = True
    else:
        tem_permissao = False
        
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM faturas')

            resultados = cursor.fetchall()

            faturas = []

            for resultado in resultados:
                if len(resultado) >= 5:
                    fatura = {
                        'id_fatura': resultado[0],
                        'id_guiavendas': resultado[1],
                        'id_cliente': resultado[2],
                        'preco_fatura': resultado[3],
                        'data_fatura': resultado[4],
                    }
                    faturas.append(fatura)
                else:
                    print(f"Unexpected tuple length: {len(resultado)}")

        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {str(e)}")
            faturas = []

    context = {
        'faturas': faturas,
        'tem_permissao': tem_permissao,  # Certifique-se de definir tem_permissao
    }
    return render(request, 'fatura.html', context)

def adicionar_fatura(request):
    if request.method == 'POST':
        id_guiavendas = request.POST.get('id_guiavendas')
        id_cliente = request.POST.get('id_cliente')
        preco_fatura = request.POST.get('preco_fatura')
        data_fatura = request.POST.get('data_fatura')

        with connection.cursor() as cursor:
            cursor.execute('CALL sp_Faturas_create(%s, %s, %s, %s)',
                           [id_guiavendas, id_cliente, preco_fatura, data_fatura])
            connection.commit()

        return redirect('fatura')

    return HttpResponse("Erro ao adicionar fatura!")

def editar_fatura(request, id):
    if request.method == 'POST':
        id_guiavendas = request.POST.get('id_guiavendas')
        id_cliente = request.POST.get('id_cliente')
        preco_fatura = request.POST.get('preco_fatura')
        data_fatura = request.POST.get('data_fatura')

        with connection.cursor() as cursor:
            cursor.execute('CALL sp_Faturas_update(%s, %s, %s, %s, %s)',
                           [id, id_guiavendas, id_cliente, preco_fatura, data_fatura])
            connection.commit()

        return redirect('fatura')

    return HttpResponse("Erro ao editar fatura!")

def excluir_fatura(request, id):
    if id is not None:
        id = int(id)

    with connection.cursor() as cursor:
        cursor.execute('CALL sp_Faturas_delete(%s)', [id])
        connection.commit()

    return redirect('fatura')





def historico_user(request, id):
    exemplo_utilizador = {
        'id': id,
    }
    return render(request, 'historico_user.html', exemplo_utilizador)


def detalhes_encomenda (request, id):
    exemplo_encomenda = {
        'id': id,
    }
    return render(request, 'detalhes_encomenda.html', exemplo_encomenda)

def login_site_vendas(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting to log in with email: {email}")
        print(f"Password entered: {password}")  # Be cautious with logging passwords in production

        try:
            # Retrieve the user from the database using email
            user = User.objects.using('mongodb').get(email=email)
            print(f"User found: {user.username}")

            # Directly compare the password
            if password == user.password:  # Compare directly with the stored password
                print(f"Password for user {user.username} is correct.")
                request.session['username'] = user.username
                return redirect('homepage_site_vendas')
            else:
                print(f"Incorrect password for user with email {email}.")
                return HttpResponse('Usuário ou senha incorretos.')
        except User.DoesNotExist:
            print(f"User with email {email} does not exist.")
            return HttpResponse('Usuário ou senha incorretos.')
    else:
        print("GET request received for login.")
        return render(request, 'login_site_vendas.html')  


def criar_conta(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        nome = request.POST.get('nome')
        nif = request.POST.get('nif')
        telemovel = request.POST.get('telemovel')
        data_nascimento = request.POST.get('data_nascimento')
        morada = request.POST.get('morada')

        # Consulta no banco de dados MongoDB
        try:
            user = User.objects.using('mongodb').create(username=username, password=password, email=email, nome=nome, nif=nif, telemovel=telemovel, data_nascimento=data_nascimento, morada=morada)
            print(f"Usuário criado: {user.username}")
            return render(request, 'login_site_vendas.html')
        except User.DoesNotExist:
            return HttpResponse('Erro ao criar usuário.')
    else:
        return render(request, 'criar_conta.html')
    


def homepage_site_vendas(request):
    try:
        equipments = Equipment.objects.all()  # Ensure this retrieves the correct data
        logger.debug(f'Number of equipments found: {equipments.count()}')
    except Exception as e:
        logger.error(f'Error retrieving equipments: {e}')
        equipments = []  # Set to an empty list to avoid further errors

    context = {
        'equipments': equipments,
        'message': None,  # or any message you want to pass
        'message_tags': None,  # or any tags you want to pass
    }
    return render(request, 'homepage_site_vendas.html', context)

def comprar(request, nome_equip, preco_equip, total_equip):
    try:
        print("Entrou na função de visualização comprar")
        
        # Verifica se o usuário está logado
        if 'username' not in request.session:
            return HttpResponse('Erro: Usuário não autenticado.')
        print("Usuário autenticado")
        
        # Recupera o nome do usuário da sessão
        username = request.session['username']
        print(f"Nome de usuário: {username}")
        
        # Verifica se os parâmetros não estão vazios
        if not nome_equip or preco_equip is None or total_equip is None:
            return HttpResponse('Erro: Parâmetros inválidos.')
        print("Parâmetros válidos")
        
        # Converte preco_equip e total_equip para inteiros
        preco_equip = int(preco_equip)
        total_equip = int(total_equip)

        # Obtém a data e hora atual do servidor
        timestamp = timezone.now()
        # Converte a data para uma string formatada
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Timestamp: {timestamp_str}")

        if request.method == 'POST':
            # Confirmação de compra
            # Conectar ao MongoDB
            client = MongoClient('localhost', 27017)
            db = client['BD_2']
            compras_collection = db['compras']

            # Inserir a compra no MongoDB
            compra_data = {
                'username': username,
                'produto': nome_equip,
                'total': preco_equip * total_equip,
                'timestamp': timestamp_str
            }
            compra_id = compras_collection.insert_one(compra_data).inserted_id

            # Log para verificar se a compra foi salva corretamente
            print(f"Compra salva: {compra_id}")

               # Exibe mensagem de sucesso
        messages.success(request, 'Compra feita com sucesso!')

        # Redireciona o usuário para a página de compras ou alguma outra página
        return redirect('homepage_site_vendas')  # Substitua 'homepage_site_vendas' pelo nome da sua view de compras

    except Exception as e:
        # Exibe mensagem de erro, se necessário
        messages.error(request, f'Erro ao fazer a compra: {str(e)}')
        return HttpResponse(f'Erro: {str(e)}')
    

def purchase_history(request):
    username = request.session.get('username')
    if username:
        purchases = Purchase.objects.using('mongodb').filter(username=username)
        return render(request, 'purchase_history.html', {'purchases': purchases})
    else:
        return HttpResponse('Usuário não autenticado.')
    
def dashboard(request):
    # Ensure the user is authenticated and has the right permissions
    id_nivel = LocalStorage.get_id_nivel(request)
    if id_nivel != 1:  # Assuming 1 is the admin level
        return redirect('index')

    # Fetch stock equipment, components, and orders
    with connection.cursor() as cursor:
        # Total stock equipment
        cursor.execute('SELECT COUNT(*) FROM STOCKEQUIPAMENTOS')
        stock_equipamentos_count = cursor.fetchone()[0]

        # Total stock components
        cursor.execute('SELECT COUNT(*) FROM STOCKCOMPONENTES')
        stock_componentes_count = cursor.fetchone()[0]

        # Total orders
        cursor.execute('SELECT COUNT(*) FROM ENCOMENDAS')
        encomendas_count = cursor.fetchone()[0]

        # Fetch total sales from invoices
        cursor.execute('SELECT SUM(PRECO_FATURA) FROM FATURA')
        total_vendas = cursor.fetchone()[0] or 0

        # Fetch daily production data
        cursor.execute('SELECT COUNT(*) FROM PRODUCAO_DIARIA WHERE DATA_PRODUCAO = CURRENT_DATE')
        producao_diaria_count = cursor.fetchone()[0]

        # Fetch limited list of fornecedores, maodebra, funcionarios, and lotes
        cursor.execute('SELECT ID_FORNECEDOR, NOME_FORNECEDOR FROM FORNECEDORES LIMIT 10')
        fornecedores = cursor.fetchall()

        cursor.execute('SELECT ID_MO, NOME_MO, CUSTO_MO FROM MAODEOBRA LIMIT 10')
        maodebra = cursor.fetchall()

        cursor.execute('SELECT ID_FUNCIONARIO, NOME FROM FUNCIONARIOS LIMIT 10')
        funcionarios = cursor.fetchall()

        cursor.execute('SELECT ID_LOTE, ID_PRODUCAO, ID_TIPOEQUIP, QUANTIDADE_PRODUTOS, ID_ARMAZEM, ID_FUNCIONARIO FROM LOTES LIMIT 10')
        lotes = cursor.fetchall()

    context = {
        'stock_equipamentos_count': stock_equipamentos_count,
        'stock_componentes_count': stock_componentes_count,
        'encomendas_count': encomendas_count,
        'total_vendas': total_vendas,
        'producao_diaria_count': producao_diaria_count,
        'fornecedores': fornecedores,
        'maodebra': maodebra,
        'funcionarios': funcionarios,
        'lotes': lotes,
    }

    return render(request, 'dashboard.html', context)

def armazens_view(request):
    armazens = Armazem.objects.all()  # Fetch the list of armazéns
    funcionarios = Funcionario.objects.all()  # Fetch the list of funcionários
    return render(request, 'armazens.html', {'armazens': armazens, 'funcionarios': funcionarios})

def load_equipamentos_client(request):
    try:
        # Retrieve all equipamentos from the database
        equipamentos = Equipamentos.objects.all()
        print(f"Retrieved {len(equipamentos)} equipamentos for client view.")
    except Exception as e:
        print(f"Error retrieving equipamentos: {str(e)}")
        equipamentos = []

    # Render the equipamentos in a client-side template
    return render(request, 'equipamentos_client.html', {'equipamentos': equipamentos})