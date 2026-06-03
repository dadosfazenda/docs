"""Gera as páginas MDX das certidões (API comercial) + atualiza docs.json.
Roda na raiz do repo dadosfazenda-mintlify-docs."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(ROOT, "api-reference", "certidoes")
os.makedirs(OUTDIR, exist_ok=True)

# consult_key -> campos obrigatórios (espelha o catálogo)
FIELDS = {
    "apf_rural": ["cnpj_cpf"],
    "ccd_pf": ["cpf"],
    "ccd_pj": ["cnpj"],
    "cnd": ["cpf_cnpj", "uf"],
    "cndir": ["nirf"],
    "cndm": ["cpf_cnpj", "municipio_ibge"],
    "ibama_debitos": ["cpf_cnpj"],
    "ibama_embargos": ["cpf_cnpj"],
    "mpf": ["cpf_cnpj"],
    "tcu": ["cpf_cnpj"],
    "trf": ["cpf_cnpj", "regiao_trf"],
    "trt": ["cpf_cnpj", "regiao_trt"],
    "tse": ["cpf", "nome_completo", "data_nascimento"],
    "tst": ["cpf_cnpj"],
    "dap": ["cpf", "data_nascimento"],
    "cnj_improbidade": ["cpf", "nome_completo"],
    "lista_suja_trabalho_escravo": ["cpf_cnpj"],
    "titularidade_car": ["codigo_car"],
    "imoveis_por_titular": ["cpf_cnpj"],
    "processos_por_titular": ["cpf_cnpj"],
}

TITLES = {
    "apf_rural": "APF Rural",
    "ccd_pf": "CCD-PF — Certidão Conjunta de Débitos (PF)",
    "ccd_pj": "CCD-PJ — Certidão Conjunta de Débitos (PJ)",
    "cnd": "CND — Certidão Negativa de Débitos",
    "cndir": "CNDIR — Débitos do Imóvel Rural",
    "cndm": "CNDM — Certidão Negativa Municipal",
    "ibama_debitos": "IBAMA — Certidão Negativa de Débitos",
    "ibama_embargos": "IBAMA — Certidão Negativa de Embargos",
    "mpf": "MPF — Certidão Negativa",
    "tcu": "TCU — Certidão Negativa de Processo",
    "trf": "TRF — Certidão Cível/Eleitoral/Criminal",
    "trt": "TRT — Certidão Trabalhista",
    "tse": "TSE — Quitação Eleitoral",
    "tst": "TST — Débitos Trabalhistas",
    "dap": "DAP — Declaração de Aptidão ao Pronaf",
    "cnj_improbidade": "CNJ — Condenações por Improbidade",
    "lista_suja_trabalho_escravo": "Lista Suja — Trabalho Escravo",
    "titularidade_car": "Titularidade por CAR",
    "imoveis_por_titular": "Imóveis Rurais por Titular",
    "processos_por_titular": "Processos Judiciais por Titular",
}

DESCRIPTIONS = {
    "apf_rural": "Consulta a Autorização Provisória de Funcionamento (APF) de produtor rural.",
    "ccd_pf": "Certidão Conjunta de Débitos relativos a Tributos Federais e à Dívida Ativa da União (Pessoa Física).",
    "ccd_pj": "Certidão Conjunta de Débitos relativos a Tributos Federais e à Dívida Ativa da União (Pessoa Jurídica).",
    "cnd": "Certidão Negativa de Débitos por UF.",
    "cndir": "Certidão Negativa de Débitos do Imóvel Rural (ITR) pelo NIRF.",
    "cndm": "Certidão Negativa de Débitos Municipais.",
    "ibama_debitos": "Certidão de débitos no IBAMA.",
    "ibama_embargos": "Certidão de áreas embargadas no IBAMA.",
    "mpf": "Certidão negativa no Ministério Público Federal.",
    "tcu": "Certidão negativa de processos no Tribunal de Contas da União.",
    "trf": "Certidão cível, eleitoral ou criminal no Tribunal Regional Federal da região informada.",
    "trt": "Certidão no Tribunal Regional do Trabalho da região informada.",
    "tse": "Certidão de Quitação Eleitoral.",
    "tst": "Certidão Negativa de Débitos Trabalhistas (CNDT).",
    "dap": "Consulta a Declaração de Aptidão ao Pronaf (DAP).",
    "cnj_improbidade": "Consulta ao Cadastro Nacional de Condenações Cíveis por Ato de Improbidade Administrativa (CNJ).",
    "lista_suja_trabalho_escravo": "Verifica se o CPF/CNPJ consta no Cadastro de Empregadores (Lista Suja do Trabalho Escravo).",
    "titularidade_car": "Retorna a titularidade (proprietário) de um imóvel a partir do código CAR.",
    "imoveis_por_titular": "Lista os imóveis rurais (CARs) vinculados a um CPF/CNPJ.",
    "processos_por_titular": "Lista processos judiciais vinculados a um CPF/CNPJ.",
}

FIELD_META = {
    "cpf_cnpj": ("CPF ou CNPJ do titular (apenas dígitos).", "12345678000190"),
    "cnpj_cpf": ("CNPJ ou CPF do titular (apenas dígitos).", "12345678000190"),
    "cpf": ("CPF do titular (apenas dígitos, 11 caracteres).", "12345678909"),
    "cnpj": ("CNPJ do titular (apenas dígitos, 14 caracteres).", "12345678000190"),
    "uf": ("Sigla da UF (2 letras).", "MG"),
    "nirf": ("NIRF — código do imóvel rural na Receita Federal.", "1234567"),
    "municipio_ibge": ("Código IBGE do município (7 dígitos).", "3106200"),
    "regiao_trf": ("Número da região do TRF (1 a 6).", "1"),
    "regiao_trt": ("Número da região do TRT (1 a 24).", "3"),
    "nome_completo": ("Nome completo do titular.", "João da Silva"),
    "data_nascimento": ("Data de nascimento (AAAA-MM-DD).", "1980-05-15"),
    "codigo_car": ("Código SICAR do imóvel.", "MG-3111507-DBEB9FF072D2402FA066E8AF2F60CF71"),
}

BASE = "https://data.dadosfazenda.com.br"


def mdx(key: str) -> str:
    fields = FIELDS[key]
    title = TITLES[key]
    desc = DESCRIPTIONS[key]
    params = "\n\n".join(
        f'<ParamField body="{f}" type="string" required>\n  {FIELD_META[f][0]}\n</ParamField>'
        for f in fields
    )
    body_example = "{\n" + ",\n".join(f'    "{f}": "{FIELD_META[f][1]}"' for f in fields) + "\n  }"
    return f'''---
title: "{title}"
api: "POST /v1/certidoes/{key}"
description: "{desc}"
---

## Descrição

{desc}

A consulta é **síncrona**: a API processa e retorna os dados estruturados e,
quando houver, os arquivos oficiais (PDF) com **URL de download assinada
(validade de 30 minutos)**.

## Autenticação

Envie sua API key no header `Authorization: Bearer SEU_TOKEN`. Cada chamada
bem-sucedida consome **1 unidade** da cota mensal. Em erro de consulta a cota
é estornada.

## Parâmetros

{params}

## Resposta

<ResponseField name="certidao" type="string">
  Identificador da certidão consultada (`{key}`).
</ResponseField>

<ResponseField name="data" type="object">
  Payload estruturado do resultado (varia conforme a certidão).
</ResponseField>

<ResponseField name="arquivos" type="array">
  Lista de arquivos oficiais. Cada item traz `filename`, `content_type`,
  `kind`, `url` (assinada) e `expires_in` (segundos até expirar — 1800 = 30 min).
</ResponseField>

<RequestExample>

```bash cURL
curl -X POST "{BASE}/v1/certidoes/{key}" \\
  -H "Authorization: Bearer SEU_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{body_example}'
```

</RequestExample>

<ResponseExample>

```json 200 OK
{{
  "success": true,
  "message": "Success",
  "data": {{
    "certidao": "{key}",
    "data": {{ }},
    "arquivos": [
      {{
        "filename": "{key}.pdf",
        "content_type": "application/pdf",
        "kind": "official_pdf",
        "url": "{BASE}/storage/v1/object/sign/certidoes/...",
        "expires_in": 1800
      }}
    ]
  }}
}}
```

```json 401 — API key inválida
{{ "detail": "API key invalida." }}
```

```json 429 — cota mensal atingida
{{ "detail": "Limite mensal atingido. Reseta no proximo mes." }}
```

</ResponseExample>
'''


pages = []
for key in FIELDS:
    path = os.path.join(OUTDIR, f"{key}.mdx")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(mdx(key))
    pages.append(f"api-reference/certidoes/{key}")

# Atualiza docs.json: adiciona o grupo "Certidões" na tab API Reference
docs_path = os.path.join(ROOT, "docs.json")
docs = json.load(open(docs_path, encoding="utf-8"))
for tab in docs["navigation"]["tabs"]:
    if tab.get("tab") == "API Reference":
        # remove grupo Certidões antigo se existir (idempotente)
        tab["groups"] = [g for g in tab["groups"] if g.get("group") != "Certidões"]
        tab["groups"].append({"group": "Certidões", "pages": pages})
json.dump(docs, open(docs_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(docs_path, "a").write("\n")

print(f"gerados {len(pages)} MDX em api-reference/certidoes/")
print("docs.json: grupo 'Certidões' adicionado com", len(pages), "páginas")
