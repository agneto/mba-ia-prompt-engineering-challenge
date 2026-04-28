"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def load_v2_prompt():
    """Carrega o prompt v2 do arquivo YAML."""
    file_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data["bug_to_user_story_v2"]

class TestPrompts:
    @pytest.fixture
    def prompt(self):
        return load_v2_prompt()

    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt
        assert len(prompt["system_prompt"].strip()) > 0

    def test_prompt_has_role_definition(self, prompt):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt["system_prompt"].lower()
        role_keywords = ["especialista", "product manager", "senior", "sênior", "gestão de produtos"]
        assert any(keyword in system_prompt for keyword in role_keywords), "Prompt deve definir uma persona"

    def test_prompt_mentions_format(self, prompt):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt["system_prompt"].lower()
        format_keywords = ["markdown", "user story", "como", "eu quero", "para que"]
        assert any(keyword in system_prompt for keyword in format_keywords), "Prompt deve mencionar formato Markdown ou User Story"

    def test_prompt_has_few_shot_examples(self, prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt["system_prompt"].lower()
        # Procura por palavras que indiquem exemplos
        example_keywords = ["exemplo", "few-shot", "ex:", "relato:", "story:"]
        assert any(keyword in system_prompt for keyword in example_keywords), "Prompt deve conter exemplos (Few-shot)"
        # Verificar se tem pelo menos 2 exemplos conforme o README sugere
        assert system_prompt.count("exemplo") >= 2

    def test_prompt_no_todos(self, prompt):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt["system_prompt"]
        assert "TODO" not in system_prompt
        assert "[ ]" not in system_prompt

    def test_minimum_techniques(self, prompt):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied", [])
        assert len(techniques) >= 2, "Pelo menos 2 técnicas de Prompt Engineering devem ser listadas nos metadados"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
