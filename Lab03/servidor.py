import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

tarefas = dict()
cont = 0

print("Servidor de tarefas pronto...")

while True:
    request = socket.recv_json()
    opcao = request["opcao"]
    dados = request["dados"]
    reply = "ERRO: função não escolhida"

    match opcao:
        case "adicionar":
            tarefas[cont] = dados
            reply = f"OK, tarefa adicionada com ID: {cont}"
            cont += 1
        
        case "listar":
            # Converte o dicionário de tarefas para uma string JSON para envio
            reply = json.dumps(tarefas)

        case "atualizar":
            id_tarefa = dados.get("id")
            # Verifica se o ID existe nas tarefas
            if id_tarefa in tarefas:
                tarefas[id_tarefa]["titulo"] = dados["titulo"]
                tarefas[id_tarefa]["desc"] = dados["desc"]
                reply = f"OK, tarefa {id_tarefa} atualizada."
            else:
                reply = f"ERRO: ID {id_tarefa} não encontrado."

        case "deletar":
            id_tarefa = dados.get("id")
            # Verifica se o ID existe e o remove
            if id_tarefa in tarefas:
                del tarefas[id_tarefa]
                reply = f"OK, tarefa {id_tarefa} deletada."
            else:
                reply = f"ERRO: ID {id_tarefa} não encontrado."
        
        case "buscar":
            id_tarefa = dados.get("id")
            # Busca a tarefa pelo ID e retorna em formato JSON
            if id_tarefa in tarefas:
                reply = json.dumps(tarefas[id_tarefa])
            else:
                reply = f"ERRO: ID {id_tarefa} não encontrado."

        case _ :
            reply = "ERRO: função não encontrada"

    # Envia a resposta de volta para o cliente
    socket.send_string(reply)