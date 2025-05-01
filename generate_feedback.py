import os
import json
from github import Github
from openai import OpenAI

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
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Modelo gratuito
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    for alerta in sonar_alerts:
        prompt = gerar_prompt(alerta)
        resposta = chamar_llm(prompt)
        comentar_no_pr(f"💡 Sugestão com base no alerta do Sonar:\n\n{resposta}")

if __name__ == "__main__":
    main()
