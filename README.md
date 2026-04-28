# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Entrega do desafio técnico de Engenharia de Prompts para conversão de bugs em User Stories de alta qualidade, atingindo notas > 0.9 em todas as métricas de avaliação.

---

## Técnicas Aplicadas (Fase 2)

Para a refatoração do prompt em `prompts/bug_to_user_story_v2.yml`, utilizei a combinação das seguintes técnicas avançadas:

### 1. Few-shot Learning (OBRIGATÓRIO)
- **Justificativa**: Esta técnica é a espinha dorsal da similaridade semântica (F1-Score). Ao fornecer exemplos de bugs simples, de segurança e de performance, o modelo aprende o nível de detalhe e o vocabulário técnico exato esperado pelo dataset de referência.
- **Exemplo Prático**: Inclusão de 3 exemplos mestre (UI/Carrinho, Segurança/Vazamento e Performance/Relatório).

### 2. Role Prompting
- **Justificativa**: Define a autoridade e o tom de voz do modelo. Ao agir como um "Engenheiro de Requisitos Sênior", a LLM tende a gerar respostas mais assertivas, focadas no valor de negócio e com terminologia ágil correta.
- **Exemplo Prático**: `Você é um Engenheiro de Requisitos Sênior especializado em metodologias Ágeis e QA.`

### 3. Chain of Thought (CoT)
- **Justificativa**: Força o modelo a realizar um processo analítico interno antes de gerar a resposta final. Isso garante que IDs, logs e condições de erro não sejam ignorados em bugs complexos.
- **Exemplo Prático**: Seção `### PROCESSO DE RACIOCÍNIO` com passos de identificação de persona, extração técnica e mapeamento de valor.

### 4. Edge Case Handling (Tratamento de Exceções)
- **Justificativa**: Prompts de produção precisam lidar com entradas incompletas. Estas instruções garantem que, mesmo em relatos vagos, o output permaneça estruturado e útil para o time de desenvolvimento.
- **Exemplo Prático**: Regras específicas para "Relatos Vagos" e "Erros Críticos" dentro do System Prompt.

---

## Resultados Finais (Meta 0.9+)

### Configuração de Execução
- **Modelo Principal**: `gemini-3.1-flash-lite-preview`
- **Estratégia**: Uso do modelo 3.1 para maximizar a cota gratuita (500 req/dia) sem perda de qualidade estrutural.

---

## Como Executar

### Pré-requisitos
- Python 3.9+
- Chave de API do Google Gemini no `.env`

### Comandos
1. **Pull**: `python src/pull_prompts.py`
2. **Push**: `python src/push_prompts.py`
3. **Avaliação**: `python src/evaluate.py`
4. **Testes**: `pytest tests/test_prompts.py`
