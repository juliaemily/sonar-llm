import os
import json
import requests  # Adicionando a importação do requests
from github import Github
from huggingface_hub import InferenceClient

# Simulando alertas do Sonar
sonar_alerts = [
    {
        "file": "src/app.js",
        "line": 42,
        "message": "Use === instead of ==",
        "severity": "MAJOR",
        "code": "if (userInput == null) {\n  handleMissingInput();\n}"
    }
]

def gerar_prompt(alerta):
    return f"""
Arquivo: {alerta['file']}, linha {alerta['line']}

Alerta do Sonar:
"{alerta['message']}"

Código:
```javascript
{alerta['code']}
```

Explique tecnicamente o alerta e sugira como melhorar esse trecho de forma segura e moderna.
"""

def comentar_no_pr(mensagem):
    pr_number = os.environ.get("GITHUB_REF").split("/")[-1]
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    pr.create_issue_comment(mensagem)

def chamar_llm(prompt):
    # Cliente da Hugging Face usando o modelo LLaMA 3
    client = InferenceClient(
        repo_id="nvidia/Llama-3_1-Nemotron-Ultra-253B-v1",  # Substitua pelo ID correto do modelo LLaMA 3
        token=os.environ["HF_TOKEN"]
    )
    # Chama o modelo para gerar a resposta
    response = client.query(prompt)
    return response['generated_text']

def main():
    for alerta in sonar_alerts:
        prompt = gerar_prompt(alerta)
        resposta = chamar_llm(prompt)
        comentar_no_pr(f"💡 Sugestão com base no alerta do Sonar:\n\n{resposta}")

if __name__ == "__main__":
    main()
