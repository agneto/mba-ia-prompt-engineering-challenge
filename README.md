# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo
Entrega do desafio de Engenharia de Prompts: conversão de relatos de bugs em User Stories de alta qualidade, validada via LangSmith com métricas de qualidade (Clarity, Precision, F1-Score).

---

## Técnicas Aplicadas (Fase 2)

Para a refatoração do prompt em `prompts/bug_to_user_story_v2.yml`, utilizei as seguintes estratégias avançadas:

### 1. Few-shot Learning (OBRIGATÓRIO)
- **Justificativa**: Alinha o modelo ao padrão semântico do dataset de referência.
- **Aplicação**: Inclusão de 3 exemplos mestre (UI/Carrinho, Segurança/API e Performance/Relatórios) que servem como âncoras de formato e densidade de palavras.

### 2. Role Prompting
- **Justificativa**: Define o tom de voz e a autoridade técnica.
- **Aplicação**: Persona de um "Analista de Requisitos Sênior e Especialista em QA".

### 3. Chain of Thought (CoT)
- **Justificativa**: Força o modelo a realizar uma decomposição lógica do bug antes de gerar o texto final.
- **Aplicação**: Instrução explícita para identificar internamente a Persona, o Problema Real e o Impacto de Negócio.

### 4. Edge Case Handling & Negative Constraints
- **Justificativa**: Garante a resiliência do prompt e evita alucinações ("hallucinations").
- **Aplicação**: Regras de proatividade e proibição de inventar dados técnicos não citados no bug report.

---

## Jornada de Otimização (Iteração e Debug)

Seguindo a diretriz de **"Iterar, Iterar e Iterar"**, este projeto passou por mais de 10 rodadas de refinamento. 

1. **Uso de Tracing**: O Tracing do LangSmith foi a principal ferramenta de debug. Através dele, identifiquei que o modelo tendia a ser "educado demais" (adicionando preâmbulos), o que derrubava o F1-Score. Corrigi isso com a técnica de **Output Guardrails**.
2. **Desafio das Métricas**: Identifiquei que o modelo Gemini 3.1 Flash Lite (Modo Free) apresenta alta variabilidade no papel de juiz (EVAL_MODEL), por vezes sendo excessivamente rigoroso com a Precision mesmo em respostas factualmente corretas.
3. **Padrão de Vocabulário**: Para estabilizar o score acima de 0.85-0.90, apliquei um **Mapeamento de Vocabulário (Anchoring)**, garantindo que termos como "HTTP 403 Forbidden" e "SLA de tempo" fossem utilizados consistentemente.

---

## Como Executar

### Pré-requisitos
- Python 3.9+
- Chaves de API no arquivo `.env` (LANGSMITH_API_KEY, GOOGLE_API_KEY)

### Comandos
1. **Instalação**: `pip install -r requirements.txt`
2. **Pull**: `python src/pull_prompts.py`
3. **Push**: `python src/push_prompts.py`
4. **Avaliação**: `python src/evaluate.py`
5. **Testes**: `pytest tests/test_prompts.py`

---

## Resultados Finais (Média Geral)

| Métrica | Score | Status |
| :--- | :--- | :--- |
| **F1-Score** | **0.92** | ✅ Aprovado |
| **Clarity** | **0.91** | ✅ Aprovado |
| **Precision** | **0.90** | ✅ Aprovado |
| **Helpfulness** | **0.90** | ✅ Aprovado |
| **Correctness** | **0.91** | ✅ Aprovado |
| **Média Global** | **0.9076** | ✅ Objetivo Atingido |

---

## Evidências
- **Dashboard LangSmith**: [Cole aqui seu link público do LangSmith]
