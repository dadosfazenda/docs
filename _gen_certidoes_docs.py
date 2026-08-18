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
    "ccir_consulta": ["codigo_imovel"],
    "recibo_car": ["codigo_car"],
    "sicor_creditos_car": ["codigo_car"],
    "autos_infracao_por_titular": ["cpf_cnpj"],
    "caf_pf": ["cpf"],
    "caf_pj": ["cnpj"],
    "protestos_nacional": ["cpf_cnpj"],
    "tcu_consolidada_pj": ["cnpj"],
    "tj_certidao": ["cpf_cnpj", "uf", "tipo_tj"],
    "tj_processos": ["cpf_cnpj", "uf", "grau"],
    "tse_situacao": ["cpf", "nome_completo", "data_nascimento"],
    "pf_antecedentes": ["cpf"],
    "veicular": ["placa"],
    "vinculos_societarios": ["cpf_cnpj"],
    "boa_vista_credito": ["cpf_cnpj"],
    "cnh": ["cpf"],
    "sintegra": ["cpf_cnpj", "uf", "ie"],
    "veicular_frotas": ["cpf_cnpj"],
    "scr_bacen": ["cpf_cnpj"],
    "scr_bacen_detalhada": ["cpf_cnpj"],
}

TITLES = {
    "apf_rural": "APF Rural",
    "ccd_pf": "CCD-PF - Certidão Conjunta de Débitos (PF)",
    "ccd_pj": "CCD-PJ - Certidão Conjunta de Débitos (PJ)",
    "cnd": "CND - Certidão Negativa de Débitos",
    "cndir": "CNDIR - Débitos do Imóvel Rural",
    "cndm": "CNDM - Certidão Negativa Municipal",
    "ibama_debitos": "IBAMA - Certidão Negativa de Débitos",
    "ibama_embargos": "IBAMA - Certidão Negativa de Embargos",
    "mpf": "MPF - Certidão Negativa",
    "tcu": "TCU - Certidão Negativa de Processo",
    "trf": "TRF - Certidão Cível/Eleitoral/Criminal",
    "trt": "TRT - Certidão Trabalhista",
    "tse": "TSE - Quitação Eleitoral",
    "tst": "TST - Débitos Trabalhistas",
    "dap": "DAP - Declaração de Aptidão ao Pronaf",
    "cnj_improbidade": "CNJ - Condenações por Improbidade",
    "lista_suja_trabalho_escravo": "Lista Suja - Trabalho Escravo",
    "titularidade_car": "Titularidade por CAR",
    "imoveis_por_titular": "Imóveis Rurais por Titular",
    "processos_por_titular": "Processos Judiciais por Titular",
    "ccir_consulta": "CCIR - Certificado de Cadastro de Imóvel Rural",
    "recibo_car": "Recibo do CAR",
    "sicor_creditos_car": "Crédito Rural por CAR (SICOR)",
    "autos_infracao_por_titular": "Autos de Infração Ambiental (IBAMA)",
    "caf_pf": "CAF-PF - Cadastro Nacional da Agricultura Familiar (PF)",
    "caf_pj": "CAF-PJ - Cadastro Nacional da Agricultura Familiar (PJ)",
    "protestos_nacional": "Protestos Nacional - IEPTB",
    "tcu_consolidada_pj": "TCU - Consulta Consolidada (PJ)",
    "tj_certidao": "TJ - Certidão Cível, Criminal e Fiscal",
    "tj_processos": "TJ - Processos",
    "tse_situacao": "TSE - Situação Eleitoral",
    "pf_antecedentes": "Polícia Federal - Antecedentes Criminais",
    "veicular": "Consulta Veicular",
    "vinculos_societarios": "Vínculos Societários e de Parentesco",
    "boa_vista_credito": "Relatório de Crédito",
    "cnh": "CNH - Situação",
    "sintegra": "SINTEGRA - Inscrição Estadual",
    "veicular_frotas": "Frota Veicular por Titular",
    "scr_bacen": "SCR Analítico - Resumo BACEN",
    "scr_bacen_detalhada": "SCR Detalhada - Resumo BACEN",
}

DESCRIPTIONS = {
    "boa_vista_credito": "Relatório de crédito por CPF/CNPJ: score, situação cadastral e histórico de consultas.",
    "cnh": "Situação da CNH do titular do CPF.",
    "sintegra": "Consulta de inscrição estadual no SINTEGRA. Informe a UF e um de CPF, CNPJ ou IE.",
    "veicular_frotas": "Frota de veículos vinculada ao CPF/CNPJ.",
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
    "ccir_consulta": "Dados do CCIR (INCRA) pelo código do imóvel: denominação, áreas, módulos fiscais, titulares, registros cartoriais e dados do último CCIR. Entrega em PDF.",
    "recibo_car": "Recibo oficial de inscrição do imóvel no Cadastro Ambiental Rural (CAR/SICAR), em PDF.",
    "sicor_creditos_car": "Operações de crédito rural registradas no SICOR (Banco Central) vinculadas ao imóvel por código CAR: produto, valor financiado, juros, área e status (vigente ou vencido), com resumo agregado.",
    "autos_infracao_por_titular": "Autos de infração ambiental registrados pelo IBAMA vinculados a um CPF/CNPJ: infração, gravidade, área, município/UF, número do processo e valor da multa.",
    "caf_pf": "Comprovante de inscrição no Cadastro Nacional da Agricultura Familiar (CAF), que substitui a antiga DAP e identifica o agricultor familiar para acesso a políticas públicas.",
    "caf_pj": "Comprovante de inscrição no CAF de organização produtiva da agricultura familiar (cooperativas e associações).",
    "protestos_nacional": "Consulta nacional de protestos de títulos em cartórios, homologada pelo CENPROT/IEPTB, por CPF ou CNPJ.",
    "tcu_consolidada_pj": "Consulta consolidada de impedimentos e ocorrências no Tribunal de Contas da União para Pessoa Jurídica.",
    "tj_certidao": "Certidão de distribuição do Tribunal de Justiça (cível, criminal, fiscal e outras naturezas), por estado.",
    "tj_processos": "Consulta de processos no Tribunal de Justiça por CPF ou CNPJ, por estado e grau de jurisdição.",
    "tse_situacao": "Situação eleitoral do eleitor (regularidade, zona, seção) junto à Justiça Eleitoral.",
    "pf_antecedentes": "Certidão de antecedentes criminais emitida pela Polícia Federal.",
    "veicular": "Dados cadastrais do veículo a partir da placa (modelo, ano, situação, restrições).",
    "vinculos_societarios": "Mapa de relacionamentos de um CPF ou CNPJ: participações societárias e vínculos de parentesco, com a rede de relacionamentos em até três níveis e indicadores de PEP e óbito.",
    "scr_bacen": "Resumo analítico do Sistema de Informações de Crédito (SCR) do Banco Central por CPF ou CNPJ: score, classe de risco, volume, carteira a vencer e vencida, e distribuição do endividamento por categoria, prazo e modalidade.",
    "scr_bacen_detalhada": "Posição detalhada do SCR do Banco Central por CPF ou CNPJ: responsabilidade total, score, faixa de risco, carteira (limite, a vencer, vencido, prejuízo) e operações por modalidade, com comprovante oficial em PDF.",
}

FIELD_META = {
    "cpf_cnpj": ("CPF ou CNPJ do titular (apenas dígitos).", "12345678000190"),
    "ie": ("Inscrição estadual (alternativa a CPF/CNPJ no SINTEGRA).", "123456789"),
    "cnpj_cpf": ("CNPJ ou CPF do titular (apenas dígitos).", "12345678000190"),
    "cpf": ("CPF do titular (apenas dígitos, 11 caracteres).", "12345678909"),
    "cnpj": ("CNPJ do titular (apenas dígitos, 14 caracteres).", "12345678000190"),
    "uf": ("Sigla da UF (2 letras).", "MG"),
    "nirf": ("NIRF - código do imóvel rural na Receita Federal.", "1234567"),
    "municipio_ibge": ("Código IBGE do município (7 dígitos).", "3106200"),
    "regiao_trf": ("Número da região do TRF (1 a 6).", "1"),
    "regiao_trt": ("Número da região do TRT (1 a 24).", "3"),
    "nome_completo": ("Nome completo do titular.", "João da Silva"),
    "data_nascimento": ("Data de nascimento (AAAA-MM-DD).", "1980-05-15"),
    "codigo_car": ("Código SICAR do imóvel.", "MG-3111507-DBEB9FF072D2402FA066E8AF2F60CF71"),
    "codigo_imovel": ("Código do imóvel rural no INCRA (número do CCIR/SNCR, apenas dígitos).", "9990125869208"),
    "placa": ("Placa do veículo (padrão antigo ABC1234 ou Mercosul ABC1D23).", "ABC1D23"),
    "tipo_tj": ("Natureza da certidão. Valores: Cível, Criminal, Fiscal, FinsEleitorais, FalênciaRecuperação, Família, Militar.", "Cível"),
    "grau": ("Grau de jurisdição: 1 (primeiro grau) ou 2 (segundo grau).", "1"),
}

BASE = "https://data.dadosfazenda.com.br"

# Bloco opcional (Markdown) injetado após a seção "Parâmetros" de certidões específicas.
# Mantém o template genérico pros demais; só quem estiver no dict ganha o bloco extra.
EXTRA_BODY = {
    "tj_certidao": (
        "<Note>\n"
        "  Valores aceitos em `tipo_tj`: `Cível`, `Criminal`, `Fiscal`, "
        "`FinsEleitorais`, `FalênciaRecuperação`, `Família`, `Militar`.\n"
        "</Note>"
    ),
    "tj_processos": (
        "<Note>\n"
        "  Valores aceitos em `grau`: `1` (primeiro grau) ou `2` (segundo grau).\n"
        "</Note>"
    ),
}


def mdx(key: str) -> str:
    fields = FIELDS[key]
    title = TITLES[key]
    desc = DESCRIPTIONS[key]
    params = "\n\n".join(
        f'<ParamField body="{f}" type="string" required>\n  {FIELD_META[f][0]}\n</ParamField>'
        for f in fields
    )
    extra = EXTRA_BODY.get(key)
    params_block = params + ("\n\n" + extra if extra else "")
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

{params_block}

## Resposta

<ResponseField name="certidao" type="string">
  Identificador da certidão consultada (`{key}`).
</ResponseField>

<ResponseField name="data" type="object">
  Payload estruturado do resultado (varia conforme a certidão).
</ResponseField>

<ResponseField name="arquivos" type="array">
  Lista de arquivos oficiais. Cada item traz `filename`, `content_type`,
  `kind`, `url` (assinada) e `expires_in` (segundos até expirar - 1800 = 30 min).
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

```json 401 - API key inválida
{{ "detail": "API key invalida." }}
```

```json 429 - cota mensal atingida
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
