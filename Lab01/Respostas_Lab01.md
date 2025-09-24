# Respostas do Lab 01 — FastAPI

## 1) Endpoint `/count`
**1. O que acontece com o contador?**  
A cada requisição **GET** a `/count`, o valor é **incrementado em 1** no **processo do servidor** que está rodando. Se reiniciar o servidor, o contador **zera**. Com várias instâncias/processos, cada um tem seu próprio valor (não é compartilhado).

**2. Por que é necessário declarar `global counter`?**  
Porque dentro da função fazemos `counter += 1`, que é **atribuição**. Sem `global`, o Python trataria `counter` como **variável local**, e não alteraria a variável do **módulo**.

**3. Por que a função não respeita a arquitetura REST?**  
Em REST, `GET` deve ser **seguro** (não muda estado) e **idempotente**. Aqui, o `GET /count` **muda o estado do servidor** (incrementa), logo **não é RESTful**.

---

## 2) Diferença entre as três rotas `/hello`
### a) `GET /hello`
Sem parâmetros; sempre retorna a **mesma string**: `"Hello, world"`.

### b) `GET /hello/{name}`
Recebe **parâmetro de caminho** obrigatório (`name`). Ex.: `/hello/Carola` → `"Hello, Carola"`.

### c) `GET /hello/` com query param
Recebe **parâmetro de query** opcional (`parameter`) com **valor padrão `"World"`**.  
Ex.: `/hello/?parameter=Clarinha` → `"Hello, Clarinha"`; sem query → `"Hello, World"`.

---

## 3) `POST /pessoa/` (checagem)
O endpoint recebe um JSON compatível com o modelo `Pessoa` (campos: `nome`, `sobrenome`, `idade`) e retorna o próprio objeto (**echo**) após validação pelo Pydantic.  
Exemplo de body:
```json
{ "nome": "Bia", "sobrenome": "Silva", "idade": 22 }
```

---

## 4) Exemplo “um pouco mais longo” (CRUD de tarefas)
- `GET /` → lista todas as tarefas.  
- `GET /tarefa/{pos}` → retorna a tarefa do índice `pos`.  
- `POST /adicionar/` → cria tarefa e **força `feito = false`**.  
- `PUT /feito/{pos}` → marca tarefa `pos` como concluída.  
- `DELETE /deletar/{pos}` → remove e **retorna** a tarefa apagada.