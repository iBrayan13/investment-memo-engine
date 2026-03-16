# Investment Memo Engine

A FastAPI-based backend service for generating investment memos using AI-powered workflows with LangGraph.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Backend](#running-the-backend)
- [API Reference](#api-reference)
- [Memo Object Structure](#memo-object-structure)
- [Project Structure](#project-structure)

## Features

- 🚀 FastAPI-based REST API
- 🤖 AI-powered memo generation using LangGraph workflows
- 📄 DOCX document generation
- 🔄 Background task processing for async memo generation
- 🔧 Multiple LLM provider support (OpenAI, Anthropic, DeepSeek, OpenRouter)

## Requirements

- Python 3.10+
- pip (Python package manager)

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/iBrayan13/investment-memo-engine.git
cd investment-memo-engine
```

2. **Create a virtual environment (recommended):**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env.dev` file in the root directory with the following variables:

```env
# Environment (DEV, TESTING, PROD)
ENV=DEV

# Server Configuration
HOST=127.0.0.1
PORT=7070

# LLM API Keys (at least one is required)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

> **Note:** At least one LLM API key must be provided for the application to start.

### Environment Files

- `.env.dev` - Development environment
- `.env.test` - Testing environment
- `.env.prod` - Production environment

## Running the Backend

### Development Mode

```bash
python main.py
```

The server will start at `http://127.0.0.1:7070` by default.

### Using Uvicorn directly

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 7070
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 7070 --workers 4
```

---

## API Reference

Base URL: `http://localhost:7070`

### Memos

All memo-related endpoints are prefixed with `/memo`.

---

#### List All Memos

Retrieves a list of all generated memos.

```http
GET /memo/
```

**Response**

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved memos |

**Example Response (200 OK):**

```json
{
  "data": [
    {
      "memo_id": "memo-1710523200",
      "status": "completed",
      "status_message": "Memorando generado exitosamente",
      "memo_object": {
        "investment_memo": {
          "project_name": "Torre Santa Fe",
          "location": "Bogotá, Colombia",
          "asset_type": "Residential Tower",
          "acquisition_price": {
            "base": 3500000000.0,
            "max_with_contingent": 4200000000.0
          },
          "deal_structure": "Joint Venture 70/30",
          "risks": [
            {
              "risk_description": "Riesgo de licencias ambientales",
              "severity": "HIGH",
              "mitigation_strategy": "Contratar consultor ambiental especializado"
            }
          ],
          "financials": {
            "base_purchase_price_millions_cop": 3500.0,
            "total_potential_land_cost": {
              "minimum": 2800.0,
              "maximum": 3200.0
            },
            "legal_expense_fund": {
              "amount_millions_cop": 150.0,
              "purpose": "Gastos legales y notariales"
            },
            "closing_costs": {
              "notary_fees": "0.5%",
              "registration_fees": "0.3%",
              "transfer_taxes": "1.5%"
            }
          },
          "development_plan": "Construcción de torre residencial de 25 pisos con 200 unidades"
        },
        "prepared_by": "Vertex Capital Group - Deal Team",
        "date": "2024-03-15",
        "equity_required": "1,200",
        "total_project_cost": "4,800",
        "recommendation": "MÁS DD",
        "executive_summary": "Torre Santa Fe es un Residential Tower ubicado en Bogotá, Colombia. Estructura del deal: Joint Venture 70/30. Costo total del proyecto: 4,800 MM COP. Equity requerido: 1,200 MM COP. IRR base proyectado: 18%. Riesgo principal: Riesgo de licencias ambientales.",
        "highlights": [
          "Ubicación: Bogotá, Colombia",
          "Tipo de activo: Residential Tower",
          "IRR base: 18% | Equity Multiple: 2.1x",
          "Riesgo crítico: Riesgo de licencias ambientales"
        ],
        "location_description": "Bogotá, Colombia",
        "asset": {
          "area_m2": "Por determinar",
          "units": "N/A",
          "zoning": "Por confirmar",
          "year_built": "Nuevo – greenfield",
          "status": "En desarrollo",
          "occupancy": "0% – pre-construcción"
        },
        "market_fundamentals": "Demanda creciente en el norte de Bogotá, vacancia del 8%, absorción anual de 500 unidades",
        "comparables": [
          {
            "project": "Torre 93",
            "location": "Chapinero, Bogotá",
            "rent_m2": "COP 45,000",
            "cap_rate": "6.5%",
            "year": "2022"
          }
        ],
        "competitive_advantages": "Ubicación premium, diseño arquitectónico innovador, eficiencia energética",
        "budget": {
          "land": "3,500",
          "land_pct": "72.9%",
          "hard_costs": "800",
          "hard_costs_pct": "16.7%",
          "soft_costs": "200",
          "soft_costs_pct": "4.2%",
          "contingency": "150",
          "contingency_pct": "3.1%",
          "financing_costs": "100",
          "financing_costs_pct": "2.1%",
          "legal_pct": "1.0%",
          "other": "50",
          "other_pct": "1.0%",
          "total": "4,800"
        },
        "financing": {
          "senior_debt_amount": "3,600",
          "senior_debt_terms": "Tasa 12%, plazo 5 años, amortización bullet",
          "equity_amount": "1,200",
          "equity_terms": "70% LP / 30% GP, preferred return 8%"
        },
        "income": {
          "gross_potential": "480",
          "gross_pct": "100%",
          "vacancy": "48",
          "vacancy_pct": "10%",
          "egi": "432",
          "egi_pct": "90%",
          "opex": "173",
          "opex_pct": "36%",
          "noi": "259",
          "noi_pct": "54%"
        },
        "returns": {
          "irr_bear": "14%",
          "irr_base": "18%",
          "irr_bull": "22%",
          "em_bear": "1.8x",
          "em_base": "2.1x",
          "em_bull": "2.5x",
          "coc_bear": "9%",
          "coc_base": "12%",
          "coc_bull": "15%"
        },
        "structure": {
          "gp_capital": "360",
          "gp_terms": "30% participación, promote 20%",
          "lp_capital": "840",
          "lp_terms": "70% participación, preferred return 8%",
          "preferred_return": "8%",
          "promote_carry": "20%",
          "capital_calls_timeline": "Q1 2024: 40%, Q3 2024: 30%, Q1 2025: 30%",
          "governance": "Comité de inversión con 3 miembros GP, 2 miembros LP"
        },
        "dd": {
          "legal": "En proceso - pendiente revisión de títulos",
          "technical": "Completado - estudio de suelos favorable",
          "environmental": "Pendiente - requiere licencia ambiental",
          "zoning": "Aprobado - uso residencial de densidad media",
          "financial": "En revisión - modelo financiero preliminar",
          "adverse_possession": "No identificado"
        },
        "rationale": [
          "Estructura de deal: Joint Venture 70/30",
          "IRR base proyectado: 18% vs benchmark mercado 14-16%",
          "Riesgo principal identificado y con plan de mitigación definido",
          "Plan de desarrollo estructurado: Construcción de torre residencial de 25 pisos con 200 unidades..."
        ],
        "conditions": [
          "Aprobación de licencia ambiental",
          "Confirmación de financiamiento bancario",
          "Firma de JV agreement"
        ],
        "next_steps": "1. Completar DD legal (adverse possession). 2. Auditoría tributaria. 3. Confirmar modelo financiero con datos de mercado. 4. Presentar resultado al comité en 30 días."
      },
      "memo_file_path": "memo/memo-1710523200.docx"
    },
    {
      "memo_id": "memo-1710523300",
      "status": "in_progress",
      "status_message": "Analizando presupuesto y estructura de financiamiento.",
      "memo_object": {},
      "memo_file_path": null
    },
    {
      "memo_id": "memo-1710523400",
      "status": "started",
      "status_message": "Iniciando generación del memorando",
      "memo_object": {},
      "memo_file_path": null
    }
  ]
}
```

**Response when no memos exist:**

```json
{
  "data": []
}
```

---

#### Get Memo by ID

Retrieves a specific memo by its ID.

```http
GET /memo/{memo_id}
```

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memo_id` | string | Yes | The unique identifier of the memo |

**Response**

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved memo |
| `404 Not Found` | Memo not found |

**Example Response (200 OK - Completed Memo):**

```json
{
  "data": {
    "memo_id": "memo-1710523200",
    "status": "completed",
    "status_message": "Memorando generado exitosamente",
    "memo_object": {
      "investment_memo": {
        "project_name": "Torre Santa Fe",
        "location": "Bogotá, Colombia",
        "asset_type": "Residential Tower",
        "acquisition_price": {
          "base": 3500000000.0,
          "max_with_contingent": 4200000000.0
        },
        "deal_structure": "Joint Venture 70/30",
        "risks": [
          {
            "risk_description": "Riesgo de licencias ambientales",
            "severity": "HIGH",
            "mitigation_strategy": "Contratar consultor ambiental especializado"
          }
        ],
        "financials": {
          "base_purchase_price_millions_cop": 3500.0,
          "total_potential_land_cost": {
            "minimum": 2800.0,
            "maximum": 3200.0
          },
          "legal_expense_fund": {
            "amount_millions_cop": 150.0,
            "purpose": "Gastos legales y notariales"
          },
          "closing_costs": {
            "notary_fees": "0.5%",
            "registration_fees": "0.3%",
            "transfer_taxes": "1.5%"
          }
        },
        "development_plan": "Construcción de torre residencial de 25 pisos con 200 unidades"
      },
      "prepared_by": "Vertex Capital Group - Deal Team",
      "date": "2024-03-15",
      "equity_required": "1,200",
      "total_project_cost": "4,800",
      "recommendation": "MÁS DD",
      "executive_summary": "Torre Santa Fe es un Residential Tower ubicado en Bogotá, Colombia. Estructura del deal: Joint Venture 70/30. Costo total del proyecto: 4,800 MM COP. Equity requerido: 1,200 MM COP. IRR base proyectado: 18%. Riesgo principal: Riesgo de licencias ambientales.",
      "highlights": [
        "Ubicación: Bogotá, Colombia",
        "Tipo de activo: Residential Tower",
        "IRR base: 18% | Equity Multiple: 2.1x",
        "Riesgo crítico: Riesgo de licencias ambientales"
      ],
      "location_description": "Bogotá, Colombia",
      "asset": {
        "area_m2": "Por determinar",
        "units": "N/A",
        "zoning": "Por confirmar",
        "year_built": "Nuevo – greenfield",
        "status": "En desarrollo",
        "occupancy": "0% – pre-construcción"
      },
      "market_fundamentals": "Demanda creciente en el norte de Bogotá, vacancia del 8%, absorción anual de 500 unidades",
      "comparables": [
        {
          "project": "Torre 93",
          "location": "Chapinero, Bogotá",
          "rent_m2": "COP 45,000",
          "cap_rate": "6.5%",
          "year": "2022"
        }
      ],
      "competitive_advantages": "Ubicación premium, diseño arquitectónico innovador, eficiencia energética",
      "budget": {
        "land": "3,500",
        "land_pct": "72.9%",
        "hard_costs": "800",
        "hard_costs_pct": "16.7%",
        "soft_costs": "200",
        "soft_costs_pct": "4.2%",
        "contingency": "150",
        "contingency_pct": "3.1%",
        "financing_costs": "100",
        "financing_costs_pct": "2.1%",
        "legal_pct": "1.0%",
        "other": "50",
        "other_pct": "1.0%",
        "total": "4,800"
      },
      "financing": {
        "senior_debt_amount": "3,600",
        "senior_debt_terms": "Tasa 12%, plazo 5 años, amortización bullet",
        "equity_amount": "1,200",
        "equity_terms": "70% LP / 30% GP, preferred return 8%"
      },
      "income": {
        "gross_potential": "480",
        "gross_pct": "100%",
        "vacancy": "48",
        "vacancy_pct": "10%",
        "egi": "432",
        "egi_pct": "90%",
        "opex": "173",
        "opex_pct": "36%",
        "noi": "259",
        "noi_pct": "54%"
      },
      "returns": {
        "irr_bear": "14%",
        "irr_base": "18%",
        "irr_bull": "22%",
        "em_bear": "1.8x",
        "em_base": "2.1x",
        "em_bull": "2.5x",
        "coc_bear": "9%",
        "coc_base": "12%",
        "coc_bull": "15%"
      },
      "structure": {
        "gp_capital": "360",
        "gp_terms": "30% participación, promote 20%",
        "lp_capital": "840",
        "lp_terms": "70% participación, preferred return 8%",
        "preferred_return": "8%",
        "promote_carry": "20%",
        "capital_calls_timeline": "Q1 2024: 40%, Q3 2024: 30%, Q1 2025: 30%",
        "governance": "Comité de inversión con 3 miembros GP, 2 miembros LP"
      },
      "dd": {
        "legal": "En proceso - pendiente revisión de títulos",
        "technical": "Completado - estudio de suelos favorable",
        "environmental": "Pendiente - requiere licencia ambiental",
        "zoning": "Aprobado - uso residencial de densidad media",
        "financial": "En revisión - modelo financiero preliminar",
        "adverse_possession": "No identificado"
      },
      "rationale": [
        "Estructura de deal: Joint Venture 70/30",
        "IRR base proyectado: 18% vs benchmark mercado 14-16%",
        "Riesgo principal identificado y con plan de mitigación definido",
        "Plan de desarrollo estructurado: Construcción de torre residencial de 25 pisos con 200 unidades..."
      ],
      "conditions": [
        "Aprobación de licencia ambiental",
        "Confirmación de financiamiento bancario",
        "Firma de JV agreement"
      ],
      "next_steps": "1. Completar DD legal (adverse possession). 2. Auditoría tributaria. 3. Confirmar modelo financiero con datos de mercado. 4. Presentar resultado al comité en 30 días."
    },
    "memo_file_path": "memo/memo-1710523200.docx"
  }
}
```

**Example Response (200 OK - In Progress Memo):**

```json
{
  "data": {
    "memo_id": "memo-1710523300",
    "status": "in_progress",
    "status_message": "Analizando presupuesto y estructura de financiamiento.",
    "memo_object": {},
    "memo_file_path": null
  }
}
```

**Example Response (200 OK - Started Memo):**

```json
{
  "data": {
    "memo_id": "memo-1710523400",
    "status": "started",
    "status_message": "Iniciando generación del memorando",
    "memo_object": {},
    "memo_file_path": null
  }
}
```

**Example Response (200 OK - Failed Memo):**

```json
{
  "data": {
    "memo_id": "memo-1710523500",
    "status": "failed",
    "status_message": "Error: Workflow failed",
    "memo_object": {},
    "memo_file_path": null
  }
}
```

**Example Response (404 Not Found):**

```json
{
  "detail": "Memo not found"
}
```

---

#### Download Memo DOCX File

Downloads the generated DOCX file for a specific memo.

```http
GET /memo/docx/{memo_id}
```

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memo_id` | string | Yes | The unique identifier of the memo |

**Response**

| Status Code | Description |
|-------------|-------------|
| `200 OK` | DOCX file downloaded successfully |
| `404 Not Found` | Memo not found or DOCX file not generated |

**Response Headers (200 OK):**
- `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- `Content-Disposition: attachment; filename="{memo_id}.docx"`

**Example Usage:**

```bash
# Download memo DOCX file
curl -O -J "http://localhost:8080/memo/docx/memo-1710523200"
```

**Notes:**
- This endpoint returns the actual DOCX file as a binary stream
- The file is only available if the memo status is `completed`
- If the memo exists but `memo_file_path` is `null`, returns 404 Not Found

---

#### Delete Memo

Deletes a specific memo by its ID.

```http
DELETE /memo/{memo_id}
```

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memo_id` | string | Yes | The unique identifier of the memo |

**Response**

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Memo deleted successfully |
| `404 Not Found` | Memo not found |

**Example Response (200 OK):**

```json
{
  "message": "Memo deleted successfully"
}
```

**Example Response (404 Not Found):**

```json
{
  "detail": "Memo not found"
}
```

---

#### Generate Memo

Initiates the generation of a new investment memo. This is an asynchronous operation that runs in the background.

```http
POST /memo/generate
```

**Request Body**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `raw_inputs` | array | No | `[]` | Array of raw input data for memo generation |

**Example Request:**

```json
{
  "raw_inputs": [
    {
      "type": "property_overview",
      "data": {
        "project_name": "Torre Santa Fe",
        "location": "Bogotá, Colombia",
        "asset_type": "Residential Tower"
      }
    },
    {
      "type": "deal_structure",
      "data": {
        "structure": "Joint Venture 70/30",
        "acquisition_price": "COP $3,500 MM"
      }
    }
  ]
}
```

**Response**

| Status Code | Description |
|-------------|-------------|
| `201 Created` | Memo generation started successfully |

**Example Response (201 Created):**

```json
{
  "memo_id": "memo-1710523200",
  "message": "Memo generation started in the background"
}
```

---

### Memo Status Values

The `status` field in memo objects can have the following values:

| Status | Description | `memo_object` | `memo_file_path` |
|--------|-------------|---------------|------------------|
| `started` | Memo generation has been initiated | `{}` (empty object) | `null` |
| `in_progress` | Memo is currently being generated | `{}` (empty object) | `null` |
| `completed` | Memo generation completed successfully | Full memo object | Path to DOCX file |
| `failed` | Memo generation failed | `{}` (empty object) | `null` |

**Important:** The `memo_object` field is only populated when the status is `completed`. For all other statuses (`started`, `in_progress`, `failed`), it remains an empty object `{}`.

---

## Memo Object Structure

The complete `memo_object` structure when status is `completed`:

```typescript
{
  "memo_id": string,           // Unique identifier (e.g., "memo-1710523200")
  "status": string,            // One of: "started", "in_progress", "completed", "failed"
  "status_message": string,    // Detailed status message in Spanish
  "memo_object": object,       // The generated memo content (empty {} unless status=completed)
  "memo_file_path": string | null  // Path to generated DOCX file, null if not yet generated
}
```

### MemoRequest Structure (memo_object when completed)

```typescript
{
  "investment_memo": {
    "project_name": string,
    "location": string,
    "asset_type": string,
    "acquisition_price": {
      "base": number,
      "max_with_contingent": number
    },
    "deal_structure": string,
    "risks": [
      {
        "risk_description": string,
        "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
        "mitigation_strategy": string
      }
    ],
    "financials": {
      "base_purchase_price_millions_cop": number,
      "total_potential_land_cost": {
        "minimum": number,
        "maximum": number
      },
      "legal_expense_fund": {
        "amount_millions_cop": number,
        "purpose": string
      },
      "closing_costs": {
        "notary_fees": string,
        "registration_fees": string,
        "transfer_taxes": string
      }
    },
    "development_plan": string
  },
  "prepared_by": string,
  "date": string,
  "equity_required": string,
  "total_project_cost": string,
  "recommendation": "INVERTIR" | "PASAR" | "MÁS DD",
  "executive_summary": string,
  "highlights": string[],
  "location_description": string,
  "asset": {
    "area_m2": string,
    "units": string,
    "zoning": string,
    "year_built": string,
    "status": string,
    "occupancy": string
  },
  "market_fundamentals": string,
  "comparables": [
    {
      "project": string,
      "location": string,
      "rent_m2": string,
      "cap_rate": string,
      "year": string
    }
  ],
  "competitive_advantages": string,
  "budget": {
    "land": string,
    "land_pct": string,
    "hard_costs": string,
    "hard_costs_pct": string,
    "soft_costs": string,
    "soft_costs_pct": string,
    "contingency": string,
    "contingency_pct": string,
    "financing_costs": string,
    "financing_costs_pct": string,
    "legal_pct": string,
    "other": string,
    "other_pct": string,
    "total": string
  },
  "financing": {
    "senior_debt_amount": string,
    "senior_debt_terms": string,
    "equity_amount": string,
    "equity_terms": string
  },
  "income": {
    "gross_potential": string,
    "gross_pct": string,
    "vacancy": string,
    "vacancy_pct": string,
    "egi": string,
    "egi_pct": string,
    "opex": string,
    "opex_pct": string,
    "noi": string,
    "noi_pct": string
  },
  "returns": {
    "irr_bear": string,
    "irr_base": string,
    "irr_bull": string,
    "em_bear": string,
    "em_base": string,
    "em_bull": string,
    "coc_bear": string,
    "coc_base": string,
    "coc_bull": string
  },
  "structure": {
    "gp_capital": string,
    "gp_terms": string,
    "lp_capital": string,
    "lp_terms": string,
    "preferred_return": string,
    "promote_carry": string,
    "capital_calls_timeline": string,
    "governance": string
  },
  "dd": {
    "legal": string,
    "technical": string,
    "environmental": string,
    "zoning": string,
    "financial": string,
    "adverse_possession": string
  },
  "rationale": string[],
  "conditions": string[],
  "next_steps": string
}
```

---

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** `http://localhost:7070/docs`
- **ReDoc:** `http://localhost:7070/redoc`

---

## Project Structure

```
investment-memo-engine/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── memos.json              # Memos storage file
├── memo/
│   └── memo_template.docx  # DOCX template for memos
├── src/
│   ├── core/
│   │   ├── logging.py      # Logging configuration
│   │   └── settings.py     # Application settings
│   ├── langg/
│   │   ├── graph.py        # LangGraph workflow definition
│   │   ├── nodes.py        # Workflow nodes
│   │   └── state.py        # State management
│   ├── models/
│   │   ├── manager.py      # Memo and StatusEnum models
│   │   ├── router.py       # Request/Response models
│   │   ├── langg.py        # MemoRequest and related models
│   │   └── pipeline_langg.py # Pipeline models (ExtractedEntities, etc.)
│   ├── routes/
│   │   └── memo.py         # Memo API routes
│   └── services/
│       ├── docx_service.py # DOCX generation service
│       ├── memos_manager.py# Memos persistence
│       └── pchain/         # Prompt chain utilities
└── .env.dev                # Development environment variables
```

## Workflow Overview

The memo generation follows this LangGraph workflow:

1. **merge_inputs** - Merge raw input data
2. **extract_entities** - Extract key entities using LLM
3. **normalize_data** - Normalize data (currency conversion, etc.)
4. **budget_agent** - Analyze budget and financing
5. **income_agent** - Analyze income and returns
6. **risk_agent** - Analyze risks and due diligence
7. **build_memo** - Assemble final memo from typed models
8. **build_memo_docx** - Generate DOCX document

## License

This project is open source and available under the [MIT License](LICENSE).
