import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

def imprimir_tarefa(id, tarefa):
    print("-------------------------")
    print(f"ID: {id}")
    print(f"  Título: {tarefa['titulo']}")
    print(f"  Descrição: {tarefa['desc']}")
    print("-------------------------")

opcao = input("Entre com a opção (adicionar, listar, atualizar, deletar, buscar, sair): ")
while opcao != "sair":
    match opcao:
        case "adicionar":
            titulo = input("Entre com a tarefa: ")
            descricao = input("Entre com a descrição da tarefa: ")

            request = {
                "opcao": "adicionar",
                "dados": {
                    "titulo": titulo,
                    "desc": descricao
                }
            }
            socket.send_json(request)
            reply = socket.recv_string()
            print(reply, flush=True)

        case "listar":
            request = {"opcao": "listar", "dados": {}}
            socket.send_json(request)
            reply = socket.recv_string()
            
            # Converte a string JSON recebida de volta para um dicionário Python
            tarefas = json.loads(reply)
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                print("\n=== LISTA DE TAREFAS ===")
                # Itera sobre o dicionário e imprime cada tarefa
                for id, tarefa in tarefas.items():
                    imprimir_tarefa(id, tarefa)

        case "atualizar":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para atualizar: "))
                titulo = input("Entre com o novo título: ")
                descricao = input("Entre com a nova descrição: ")

                request = {
                    "opcao": "atualizar",
                    "dados": {
                        "id": id_tarefa,
                        "titulo": titulo,
                        "desc": descricao
                    }
                }
                socket.send_json(request)
                reply = socket.recv_string()
                print(reply, flush=True)
            except ValueError:
                print("ERRO: O ID precisa ser um número.")

        case "deletar":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para deletar: "))
                request = {
                    "opcao": "deletar",
                    "dados": {"id": id_tarefa}
                }
                socket.send_json(request)
                reply = socket.recv_string()
                print(reply, flush=True)
            except ValueError:
                print("ERRO: O ID precisa ser um número.")

        case "buscar":
            try:
                id_tarefa = int(input("Digite o ID da tarefa para buscar: "))
                request = {
                    "opcao": "buscar",
                    "dados": {"id": id_tarefa}
                }
                socket.send_json(request)
                reply = socket.recv_string()
                
                # Verifica se a resposta não é um erro
                if reply.startswith("ERRO"):
                    print(reply)
                else:
                    # Converte a tarefa recebida e a imprime
                    tarefa = json.loads(reply)
                    imprimir_tarefa(id_tarefa, tarefa)
            except ValueError:
                print("ERRO: O ID precisa ser um número.")
            except json.JSONDecodeError:
                print("ERRO ao processar a resposta do servidor.")

        case _:
            print("Opção não encontrada")

    print("\n")
    opcao = input("Entre com a opção (adicionar, listar, atualizar, deletar, buscar, sair): ")