"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_id: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub.

    Args:
        prompt_id: ID do prompt (ex: bug_to_user_story_v2)
        prompt_data: Dados do prompt carregados do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurado no .env")
        return False

    full_repo_name = f"{username}/{prompt_id}"
    print(f"📤 Fazendo push do prompt para: {full_repo_name}...")

    try:
        # Criar template de chat
        # No nosso YAML, temos system_prompt e user_prompt
        messages = []
        if prompt_data.get("system_prompt"):
            messages.append(("system", prompt_data["system_prompt"]))
        if prompt_data.get("user_prompt"):
            messages.append(("human", prompt_data["user_prompt"]))

        if not messages:
            print(f"❌ Erro: Nenhum prompt (system ou user) encontrado para {prompt_id}")
            return False

        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Push para o Hub
        # is_public=True torna o prompt público
        hub.push(
            repo_full_name=full_repo_name,
            object=prompt_template,
            new_repo_description=prompt_data.get("description", ""),
            new_repo_is_public=True
        )

        print(f"✅ Push realizado com sucesso!")
        print(f"🔗 Veja seu prompt em: https://smith.langchain.com/hub/{full_repo_name}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push para o LangSmith: {str(e)}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    if not prompt_data.get("system_prompt"):
        errors.append("system_prompt está faltando ou vazio")

    if not prompt_data.get("user_prompt"):
        errors.append("user_prompt está faltando ou vazio")

    # Verifica se tem pelo menos 2 técnicas aplicadas (meta-requisito do desafio)
    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}")

    # Verifica se usou few-shot (obrigatório)
    has_few_shot = any("few-shot" in t.lower() for t in techniques)
    if not has_few_shot:
        errors.append("Técnica 'Few-shot Learning' é obrigatória")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH HUB")

    # Verificar variáveis de ambiente
    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    # Carregar prompts otimizados
    prompts_file = "prompts/bug_to_user_v2.yml"
    all_prompts = load_yaml(prompts_file)

    if not all_prompts:
        print(f"❌ Erro ao carregar {prompts_file}")
        return 1

    success_count = 0
    total_count = 0

    for prompt_id, prompt_data in all_prompts.items():
        total_count += 1
        print(f"\nProcessando prompt: {prompt_id}")

        # Validar
        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print(f"❌ Prompt inválido:")
            for err in errors:
                print(f"   - {err}")
            continue

        # Push
        if push_prompt_to_langsmith(prompt_id, prompt_data):
            success_count += 1

    print_section_header("RESUMO DO PUSH")
    print(f"Sucesso: {success_count}/{total_count}")

    return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
