# Lab 01 - REST usando FastAPI
# --------------------------------------------------------------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# --------------------------------------------------------------
# 1) Rota raiz "/" com "hello world"
# --------------------------------------------------------------
@app.get("/")
async def root():
    # Retorna um JSON simples com a mensagem pedida.
    return {"message": "hello world"}


# --------------------------------------------------------------
# 2) Contador /count
# --------------------------------------------------------------
# 1. O que acontece com o contador?
#    - A cada requisição GET em /count, o valor é incrementado em 1
#      dentro do processo do servidor. Se o servidor reiniciar, zera.
# 2. Por que é necessário declarar a variável 'counter' como global?
#    - Porque fazemos 'counter += 1' dentro da função; isso é uma
#      atribuição. Sem 'global', o Python trataria 'counter' como variável
#      local, não alterando a variável definida no módulo.
# 3. Por que esta função não respeita a arquitetura REST?
#    - Porque requisições GET deveriam ser seguras e não alterar o estado
#      do servidor. Aqui, o GET altera o estado (incrementa o contador).
counter = 0

@app.get("/count")
def get_count():
    global counter      # necessário para alterar a variável do módulo
    counter += 1        # efeito colateral: altera estado via GET (anti-REST)
    return counter      # retorna o valor numérico atual


# --------------------------------------------------------------
# 3) Três variações de /hello
# --------------------------------------------------------------

# a) Sem parâmetros (string fixa)
@app.get("/hello")
def hello_world():
    return "Hello, world"

# b) Com parâmetro de caminho (obrigatório)
#    Ex.: GET /hello/Carola -> "Hello, Carola"
@app.get("/hello/{name}")
def hello(name):
    return f"Hello, {name}"

# c) Com parâmetro de query (opcional) e valor padrão
#    Ex.: GET /hello/?parameter=Clarinha -> "Hello, Clarinha"
#    Sem query -> usa "World".
@app.get("/hello/")
def hello_with_query(parameter: str = "World"):
    return f"Hello, {parameter}"


# --------------------------------------------------------------
# 4) POST /pessoa/ com Pydantic (BaseModel)
# --------------------------------------------------------------
class Pessoa(BaseModel):
    nome: str
    sobrenome: str
    idade: int

@app.post("/pessoa/")
def criar_pessoa(pessoa: Pessoa):
    # O FastAPI valida e converte o JSON para uma instância de Pessoa
    # automaticamente. Aqui retornamos o próprio objeto (echo).
    return pessoa


# --------------------------------------------------------------
# 5) Exemplo um pouco mais longo (CRUD de tarefas)
# --------------------------------------------------------------

tarefas = list()  # lista que armazenará as tarefas criadas

class Tarefa(BaseModel):
    tarefa: str      # descrição da tarefa
    prioridade: int  # ex.: 1 (alta), 2 (média), 3 (baixa)
    feito: bool      # indica se a tarefa foi concluída

@app.get("/")
def listar_tarefas():
    # Retorna a lista completa de tarefas.
    # O FastAPI serializa cada Tarefa (BaseModel) para JSON automaticamente.
    return tarefas

@app.get("/tarefa/{pos}")
def get_tarefa(pos: int):
    # Retorna a tarefa na posição 'pos' da lista.
    # Obs.: sem validação de faixa, pode lançar IndexError se 'pos' for inválido.
    return tarefas[pos]

@app.post("/adicionar/")
def criar_tarefa(tarefa: Tarefa):
    # Recebe uma Tarefa via corpo da requisição (JSON).
    # Força 'feito=False' na criação, independentemente do valor enviado.
    tarefa.feito = False
    # Adiciona a tarefa na lista em memória.
    tarefas.append(tarefa)
    # Retorna o tamanho atual da lista (quantidade de tarefas).
    return len(tarefas)

@app.put("/feito/{pos}")
def marcar_feito(pos: int):
    # Marca como concluída a tarefa no índice 'pos'.
    tarefas[pos].feito = True
    # Retorna a tarefa atualizada para confirmação.
    return tarefas[pos]

@app.delete("/deletar/{pos}")
def deletar_tarefa(pos: int):
    # Remove a tarefa no índice 'pos' usando pop, que também a retorna.
    tarefa = tarefas.pop(pos)
    # Retorna a tarefa removida (útil para confirmação).
    return tarefa