#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar a conexão e operações do MongoDB
"""

from model.tarefa_model import TarefaModel
from bson import ObjectId

def testar_conexao_mongodb():
    """Testa a conexão e operações básicas com MongoDB"""
    print("=== Teste de Conexão e Operações MongoDB ===")
    
    # Inicializa o modelo
    model = TarefaModel()
    
    # Verifica se está conectado
    if model.mongo_context.is_connected():
        print("✅ Conectado ao MongoDB com sucesso!")
        print(f"📊 Banco: {model.mongo_context.database_name}")
        print(f"📋 Coleção: {model.mongo_context.collection_name}")
    else:
        print("❌ Não foi possível conectar ao MongoDB")
        return
    
    # Limpa dados existentes para teste limpo
    print("\n🧹 Limpando dados existentes...")
    if model.colecao is not None:
        model.colecao.delete_many({})
    
    # Teste 1: Adicionar tarefas
    print("\n📝 Teste 1: Adicionando tarefas...")
    tarefas_teste = [
        {"titulo": "Estudar Python", "descricao": "Revisar conceitos de POO", "status": "Pendente"},
        {"titulo": "Fazer exercícios", "descricao": "Completar lista de algoritmos", "status": "Pendente"},
        {"titulo": "Ler documentação", "descricao": "Estudar MongoDB e PyMongo", "status": "Concluída"},
        {"titulo": "Projeto final", "descricao": "Desenvolver aplicação completa", "status": "Pendente"}
    ]
    
    ids_inseridos = []
    for tarefa in tarefas_teste:
        resultado = model.adicionar(tarefa["titulo"], tarefa["descricao"], tarefa["status"])
        ids_inseridos.append(resultado.inserted_id)
        print(f"  ✅ Tarefa '{tarefa['titulo']}' adicionada com ID: {resultado.inserted_id}")
    
    # Teste 2: Listar todas as tarefas
    print("\n📋 Teste 2: Listando todas as tarefas...")
    todas_tarefas = model.listar()
    print(f"  📊 Total de tarefas: {len(todas_tarefas)}")
    for tarefa in todas_tarefas:
        print(f"  - {tarefa['titulo']} ({tarefa['status']})")
    
    # Teste 3: Filtrar por status
    print("\n🔍 Teste 3: Filtrando tarefas por status...")
    pendentes = model.listar("Pendente")
    concluidas = model.listar("Concluída")
    print(f"  📌 Tarefas pendentes: {len(pendentes)}")
    print(f"  ✅ Tarefas concluídas: {len(concluidas)}")
    
    # Teste 4: Buscar por ID
    print("\n🔎 Teste 4: Buscando tarefa por ID...")
    if ids_inseridos:
        primeiro_id = ids_inseridos[0]
        tarefa_encontrada = model.buscar_por_id(primeiro_id)
        if tarefa_encontrada:
            print(f"  ✅ Tarefa encontrada: {tarefa_encontrada['titulo']}")
        else:
            print("  ❌ Tarefa não encontrada")
    
    # Teste 5: Atualizar tarefa
    print("\n✏️ Teste 5: Atualizando tarefa...")
    if ids_inseridos:
        resultado = model.atualizar(
            ids_inseridos[0], 
            "Estudar Python - ATUALIZADO", 
            "Revisar conceitos de POO e MongoDB", 
            "Concluída"
        )
        if resultado.modified_count > 0:
            print(f"  ✅ Tarefa atualizada com sucesso")
        else:
            print("  ❌ Falha ao atualizar tarefa")
    
    # Teste 6: Excluir tarefa
    print("\n🗑️ Teste 6: Excluindo tarefa...")
    if len(ids_inseridos) > 1:
        resultado = model.excluir(ids_inseridos[-1])
        if resultado.deleted_count > 0:
            print(f"  ✅ Tarefa excluída com sucesso")
        else:
            print("  ❌ Falha ao excluir tarefa")
    
    # Verificação final
    print("\n📊 Estado final do banco:")
    tarefas_finais = model.listar()
    print(f"  📋 Total de tarefas restantes: {len(tarefas_finais)}")
    for tarefa in tarefas_finais:
        print(f"  - {tarefa['titulo']} ({tarefa['status']})")
    
    print("\n🎉 Todos os testes concluídos com sucesso!")

if __name__ == "__main__":
    testar_conexao_mongodb()