"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt leonanluppi/bug_to_user_story_v1 do LangSmith Hub
    e salva localmente em prompts/bug_to_user_story_v1.yml
    """
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return False

    try:
        prompt_name = "leonanluppi/bug_to_user_story_v1"
        print(f"📥 Fazendo pull do prompt: {prompt_name}...")

        # Pull do prompt do Hub
        prompt = hub.pull(prompt_name)

        # Extrair system e user prompts
        system_prompt = ""
        user_prompt = ""

        # O prompt retornado geralmente é um ChatPromptTemplate
        if hasattr(prompt, 'messages'):
            for msg in prompt.messages:
                # Verificar tipo de mensagem (System ou Human/User)
                msg_type = type(msg).__name__.lower()

                # Extrair o conteúdo/template
                content = ""
                if hasattr(msg, 'prompt') and hasattr(msg.prompt, 'template'):
                    content = msg.prompt.template
                elif hasattr(msg, 'template'):
                    content = msg.template
                elif hasattr(msg, 'content'):
                    content = msg.content

                if 'system' in msg_type:
                    system_prompt = content
                elif 'human' in msg_type or 'user' in msg_type:
                    user_prompt = content

        # Se não for ChatPromptTemplate, pode ser um PromptTemplate simples
        elif hasattr(prompt, 'template'):
            system_prompt = prompt.template

        # Estrutura para salvar no YAML
        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt inicial de baixa qualidade para conversão de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "tags": ["bug-analysis", "user-story", "v1-baseline"]
            }
        }

        # Salvar em YAML
        output_path = "prompts/bug_to_user_story_v1.yml"
        if save_yaml(prompt_data, output_path):
            print(f"✅ Prompt salvo com sucesso em: {output_path}")
            return True
        else:
            print(f"Falha ao salvar o prompt em YAML.")
            return False

    except Exception as e:
        print(f"Erro durante o pull: {str(e)}")
        return False


def main():
    """Função principal"""
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
