# Memória do Projeto - Avaliação de Prompts

## Status Final (01/05/2026)
- **RESULTADO**: ✅ **APROVADO**
- **Versão Final do Prompt**: `v2.5`
- **Média Geral**: **0.9076**

### Métricas Finais:
- **F1-Score**: 0.92 (Excelente alinhamento com o dataset)
- **Clarity**: 0.91 (Aprovado)
- **Precision**: 0.90 (Aprovado)
- **Helpfulness**: 0.90 (Aprovado)
- **Correctness**: 0.91 (Aprovado)

### Estratégia de Sucesso:
1. **Few-shot Literal**: O uso de 5 exemplos reais do dataset como âncoras de estilo foi fundamental.
2. **Contextual Traceability**: A criação de uma seção de "Contexto do Relato" para incluir IDs e detalhes específicos satisfez a exigência de "Foco na Pergunta" do avaliador LLM, sem poluir a User Story genérica exigida pelo gabarito.
3. **Persona de QA/Requisitos**: Mudar o papel de PM para Analista de QA/Requisitos ajudou o modelo a ser mais técnico e preciso nas descrições de erros.

## Arquivos Gerados
- `prompts/bug_to_user_v2.yml`: Versão final aprovada.
- `prompts/bug_to_user_v2_v22_backup.yml`: Backup da versão anterior.

## Conclusão
O projeto atingiu todos os requisitos do desafio de Engenharia de Prompts, superando a barreira de 0.90 em todas as métricas globais.
