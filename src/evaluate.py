"""
Script COMPLETO para avaliar prompts otimizados.

Este script:
1. Carrega dataset de avaliação de arquivo .jsonl (datasets/bug_to_user_story.jsonl)
2. Cria/atualiza dataset no LangSmith
3. Puxa prompts otimizados do LangSmith Hub
4. Executa avaliação de cada prompt contra o dataset
5. Calcula métricas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
6. Exibe relatório final formatado
"""

import os
import sys
import json
import time
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import check_env_vars, format_score, print_section_header, get_llm as get_configured_llm
from metrics import evaluate_f1_score, evaluate_clarity, evaluate_precision

load_dotenv()


def get_llm():
    return get_configured_llm(temperature=0)


def load_dataset_from_jsonl(jsonl_path: str) -> List[Dict[str, Any]]:
    """Carrega o dataset de avaliação a partir de um arquivo .jsonl."""
    examples = []
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                examples.append({
                    "input": data["inputs"]["bug_report"],
                    "output": data["outputs"]["reference"]
                })
        return examples
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return []


def create_langsmith_dataset(client: Client, dataset_name: str, examples: List[Dict[str, Any]]):
    """Cria ou atualiza o dataset no LangSmith."""
    try:
        # Verificar se dataset existe
        if client.has_dataset(dataset_name=dataset_name):
            print(f"   ✓ Dataset '{dataset_name}' já existe, usando existente")
            return
        
        # Criar dataset
        dataset = client.create_dataset(dataset_name=dataset_name)
        
        # Adicionar exemplos
        for example in examples:
            client.create_example(
                inputs={"bug_report": example["input"]},
                outputs={"reference": example["output"]},
                dataset_id=dataset.id
            )
        print(f"   ✓ Dataset '{dataset_name}' criado com {len(examples)} exemplos")
    except Exception as e:
        print(f"⚠️ Erro ao configurar dataset LangSmith: {e}")


def evaluate_prompt_on_example(prompt_template, example, llm):
    """Executa o prompt para um único exemplo."""
    try:
        chain = prompt_template | llm
        response = chain.invoke({"bug_report": example["input"]})
        return {
            "question": example["input"],
            "answer": response.content,
            "reference": example["output"]
        }
    except Exception as e:
        print(f"      ❌ Erro na geração: {e}")
        return {"answer": None, "question": example["input"], "reference": example["output"]}


def evaluate_prompt(prompt_name: str, dataset_name: str, examples: List[Dict[str, Any]]):
    """Realiza a avaliação completa de um prompt."""
    print(f"\n🔍 Avaliando: {prompt_name}")
    
    try:
        # Puxar prompt do Hub
        print(f"   Puxando prompt do LangSmith Hub: {prompt_name}")
        prompt_template = hub.pull(prompt_name)
        print("   ✓ Prompt carregado com sucesso")
        
        llm = get_llm()
        
        f1_scores = []
        clarity_scores = []
        precision_scores = []
        
        print("   Dataset: 15 exemplos")
        print("   Avaliando exemplos (MODO SAFE)...", flush=True)

        for i, example in enumerate(examples, 1):
            # Atraso de 20 segundos para evitar 429 no Modo Free
            time.sleep(20) 
            
            try:
                result = evaluate_prompt_on_example(prompt_template, example, llm)
            except Exception as e:
                print(f"      ⚠️  Erro fatal no exemplo {i}: {e}", flush=True)
                result = {"answer": None, "question": example.get("input", ""), "reference": example.get("output", "")}

            if result["answer"]:
                print(f"      [{i}/{len(examples)}] Gerado. Calculando métricas...", flush=True)
                
                # Atrasos entre chamadas de métricas para respeitar RPM
                f1 = evaluate_f1_score(result["question"], result["answer"], result["reference"])
                time.sleep(5)
                clarity = evaluate_clarity(result["question"], result["answer"], result["reference"])
                time.sleep(5)
                precision = evaluate_precision(result["question"], result["answer"], result["reference"])

                print(f"      [{i}/{len(examples)}] F1:{f1['score']:.2f} Clarity:{clarity['score']:.2f} Precision:{precision['score']:.2f}", flush=True)

                f1_scores.append(f1["score"])
                clarity_scores.append(clarity["score"])
                precision_scores.append(precision["score"])
            else:
                f1_scores.append(0.0)
                clarity_scores.append(0.0)
                precision_scores.append(0.0)
                print(f"      [{i}/{len(examples)}] ❌ Falha na geração", flush=True)

        # Calcular médias
        avg_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0.0
        avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.0
        avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0.0
        
        avg_helpfulness = (avg_clarity + avg_precision) / 2
        avg_correctness = (avg_f1 + avg_precision) / 2
        
        overall_avg = (avg_helpfulness + avg_correctness + avg_f1 + avg_clarity + avg_precision) / 5

        print("\n" + "="*50)
        print(f"Prompt: {prompt_name}")
        print("="*50)
        
        print("\nMétricas Derivadas:")
        print(f"  - Helpfulness: {format_score(avg_helpfulness)}")
        print(f"  - Correctness: {format_score(avg_correctness)}")
        
        print("\nMétricas Base:")
        print(f"  - F1-Score: {format_score(avg_f1)}")
        print(f"  - Clarity: {format_score(avg_clarity)}")
        print(f"  - Precision: {format_score(avg_precision)}")
        
        print("\n" + "-"*50)
        print(f"📊 MÉDIA GERAL: {overall_avg:.4f}")
        print("-"*50)
        
        passed = (avg_helpfulness >= 0.9 and avg_correctness >= 0.9 and 
                 avg_f1 >= 0.9 and avg_clarity >= 0.9 and avg_precision >= 0.9)
        
        if passed:
            print("\n✅ STATUS: APROVADO")
        else:
            print("\n❌ STATUS: REPROVADO")
            
        return {
            "prompt_name": prompt_name,
            "passed": passed,
            "average": overall_avg,
            "metrics": {
                "helpfulness": avg_helpfulness,
                "correctness": avg_correctness,
                "f1_score": avg_f1,
                "clarity": avg_clarity,
                "precision": avg_precision
            }
        }

    except Exception as e:
        print(f"❌ Erro ao avaliar prompt {prompt_name}: {e}")
        return {"prompt_name": prompt_name, "passed": False, "average": 0.0}


def main():
    """Função principal"""
    print_section_header("AVALIAÇÃO DE PROMPTS OTIMIZADOS")

    # Verificar variáveis de ambiente
    required_vars = ["LANGSMITH_API_KEY", "GOOGLE_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    client = Client()
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    
    jsonl_path = "datasets/bug_to_user_story.jsonl"
    examples = load_dataset_from_jsonl(jsonl_path)
    
    if not examples:
        return 1
    
    create_langsmith_dataset(client, "mba-ia-prompt-engineering-eval", examples)

    prompts_to_evaluate = [
        f"{username}/bug_to_user_story_v2",
    ]

    for prompt_id in prompts_to_evaluate:
        evaluate_prompt(prompt_id, "mba-ia-prompt-engineering-eval", examples)

if __name__ == "__main__":
    sys.exit(main())
