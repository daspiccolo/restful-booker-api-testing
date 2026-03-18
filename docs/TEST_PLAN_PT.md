# Plano de Testes — Restful Booker API


**Projeto:** Restful Booker API Testing  
**API testada:** https://restful-booker.herokuapp.com  

---

## 1. Objetivo

O objetivo deste plano de testes é documentar a estratégia aplicada nos testes da Restful Booker API — incluindo o que foi testado, por quê, em qual ordem, e como foram tomadas as decisões sobre cobertura de automação.

---

## 2. Escopo

Todos os 8 endpoints da Restful Booker API estavam no escopo:

| Método | Endpoint | Prioridade |
|---|---|---|
| GET | `/ping` | Alta |
| POST | `/auth` | Alta |
| GET | `/booking` | Alta |
| GET | `/booking/:id` | Alta |
| POST | `/booking` | Alta |
| PUT | `/booking/:id` | Alta |
| DELETE | `/booking/:id` | Alta |
| PATCH | `/booking/:id` | Média |

---

## 3. Abordagem de Testes

### 3.1 Testes Manuais Exploratórios Primeiro

Todos os endpoints foram testados manualmente no Postman antes de qualquer automação ser escrita.

Essa decisão foi deliberada — a documentação sozinha não é suficiente para entender o comportamento real da API. A documentação da Restful Booker não menciona que o `/ping` retorna 201 em vez de 200, nem que o `/auth` retorna 200 para credenciais inválidas. Esses comportamentos só foram descobertos através da exploração manual.

**Lição aplicada:** a documentação é um ponto de partida, não uma fonte de verdade. Sempre validar contra o sistema real.

### 3.2 Ordem de Execução dos Testes

Os testes foram executados em ordem de dependência:

```
1. Health Check (GET /ping)
      ↓
2. Explorar dados existentes (GET /booking, GET /booking/:id)
      ↓
3. Autenticação (POST /auth)
      ↓
4. Criar dados de teste (POST /booking)
      ↓
5. Operações de atualização (PUT, PATCH)
      ↓
6. Operações de exclusão (DELETE)
```

**Justificativa:**

- **Health Check primeiro** — Smoke Test. Se a API está fora do ar, não faz sentido testar mais nada.
- **GET antes do POST** — explorar dados existentes revela a estrutura do JSON, nomes dos campos e tipos de dados antes de escrever qualquer payload. Mesmo com documentação disponível, a exploração manual detecta discrepâncias entre o doc e o comportamento real.
- **AUTH antes das operações de escrita** — PUT, PATCH e DELETE exigem um token válido. A autenticação deve ser validada antes das operações que dependem dela.
- **POST antes de PUT/PATCH/DELETE** — os recursos precisam existir antes de serem atualizados ou deletados. Essa é uma dependência natural entre os testes.
- **PATCH por último** — o PATCH é funcionalmente redundante com o PUT. Com tempo limitado, o PATCH é desprioritizado.

---

## 4. Cobertura de Testes

### 4.1 Cenários Cobertos por Endpoint

Para cada endpoint, os seguintes tipos de cenário foram testados:

- **Happy path** — requisição válida com dados esperados
- **Teste negativo** — inputs inválidos, campos ausentes, tipos de dados errados
- **Teste de limite** — valores extremos como ID=0 e ID=99999
- **Teste de autenticação** — token ausente, token inválido, credenciais erradas
- **Integridade de dados** — o body da resposta corresponde ao que foi enviado na requisição
- **Validação de schema** — a resposta contém os campos esperados com os tipos corretos
- **Teste de confirmação** — após o DELETE, um GET confirma que o recurso não existe mais

### 4.2 Priorização Baseada em Risco

Com tempo limitado, a ordem de prioridade seria:

1. **POST /auth** — sem autenticação, as operações de escrita não podem ser testadas
2. **GET /booking** — valida a funcionalidade básica de leitura
3. **POST /booking** — valida a criação de recursos
4. **PUT /booking/:id** — valida a atualização completa
5. **DELETE /booking/:id** — valida a exclusão de recursos
6. **PATCH /booking/:id** — desprioritizado pois se sobrepõe à funcionalidade do PUT

**Justificativa:** o teste baseado em risco foca no que tem maior impacto no negócio. O PATCH é conveniente mas não crítico — o sistema funciona sem ele.

---

## 5. Estratégia de Automação

### 5.1 O Que Foi Automatizado

Todos os 29 casos de teste foram automatizados usando Python e Pytest.

### 5.2 Por Que Automatizar Tudo

Por ser um projeto de portfólio cobrindo uma API pública e estável, a automação completa foi adequada. Em um projeto real, a decisão consideraria:

- **Automatizar:** endpoints estáveis, cenários de regressão, execuções repetidas
- **Manter manual:** sessões exploratórias, validações pontuais, fluxos de UI

### 5.3 Principais Decisões Técnicas

**Fixtures para configuração compartilhada**  
A URL base e o token de autenticação são definidos no `conftest.py`. Se qualquer um deles mudar, apenas um lugar precisa ser atualizado.

**Dados de teste dinâmicos em vez de hardcoded**  
Os IDs de booking são buscados em tempo de execução. Durante o desenvolvimento, um ID fixo quebrou quando outro usuário deletou aquele booking da API compartilhada. Dados dinâmicos tornam os testes resilientes a mudanças externas.

**Yield fixtures para setup e teardown**  
Cada teste que precisa de um booking cria um no setup e deleta no teardown. Isso garante o isolamento dos testes — nenhum teste depende de dados deixados por outro.

**Documentação de bugs inline**  
Bugs conhecidos são documentados com comentários referenciando o BUG_REPORT.md. Isso deixa claro que o teste está verificando o comportamento atual (com bug), não o comportamento esperado.

**Testes organizados em classes por endpoint**  
Cada classe representa uma Test Suite para um endpoint. À medida que a suite cresce, cada classe pode ser movida para seu próprio arquivo sem reestruturação.

---

## 6. Critérios de Severidade de Defeitos

| Severidade | Critério | Exemplo |
|---|---|---|
| Alta | Impacto em segurança, corrupção de dados ou falhas silenciosas em integrações | BUG-003: 200 para credenciais inválidas |
| Média | Comportamento incorreto que engana os consumidores da API | BUG-006: 405 em vez de 403 |
| Baixa | Inconsistência menor com impacto mínimo no negócio | BUG-011: 405 no DELETE duplo |

---

## 7. O Que Não Foi Testado

- **Testes de performance / carga** — fora do escopo desta fase
- **Testes de segurança** — fora do escopo desta fase
- **Testes de contrato** — nenhuma ferramenta de validação de schema (ex: Pact) foi utilizada
- **Testes de UI** — somente API

Essas áreas seriam cobertas em fases subsequentes de teste.

---

## 8. Ferramentas

| Ferramenta | Finalidade |
|---|---|
| Postman | Testes manuais exploratórios |
| Python 3.13 | Linguagem de automação |
| Pytest | Framework de testes |
| Requests | Biblioteca HTTP |
| Allure Pytest | Relatórios de teste |
| GitHub Actions | Pipeline de CI/CD |

---

*Este plano de testes documenta as decisões tomadas durante o processo de teste — não um script pré-definido, mas o reflexo de um fluxo de trabalho real de QA.*