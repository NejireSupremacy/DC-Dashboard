# Mexico Data Center Intelligence Dashboard

A Streamlit dashboard for exploring recent data center research with a focus on Mexico. The project combines market, operations, energy, security, and emerging technology signals into a multi-page app designed for an academic final project and practical decision support.

## Overview

The dashboard organizes recent industry research into five sections:

1. **Operations**: Uptime tier benchmarks and enterprise MAC process categories.
2. **Energy**: PUE benchmarks, hyperscaler efficiency, and facility energy breakdown.
3. **Security**: TIA-942, ISO 27001, and physical security controls.
4. **Market**: Mexico capacity, operators, and deployment trends.
5. **Emerging Tech**: AI-era infrastructure shifts, cooling, power, and roadmap signals.

The home page also includes a **Source Explorer** that lets you filter the research catalog by page, and the energy page includes an **interactive PUE calculator**.

## Tech Stack

- Python 3.11+
- Streamlit
- Pandas
- Plotly
- Docker
- Terraform + AWS ECS/Fargate

## Project Structure

```text
dc-dashboard/
|-- app.py
|-- requirements.txt
|-- Dockerfile
|-- data/
|   |-- operations.json
|   |-- energy.json
|   |-- security.json
|   |-- market.json
|   `-- emerging_tech.json
|-- pages/
|   |-- 01_operations.py
|   |-- 02_energy.py
|   |-- 03_security.py
|   |-- 04_market.py
|   `-- 05_emerging_tech.py
|-- utils/
|   |-- __init__.py
|   |-- charts.py
|   `-- data_loader.py
`-- infra/
    |-- main.tf
    |-- variables.tf
    |-- outputs.tf
    `-- terraform.tfvars
```

## How It Works

- Each dashboard page reads from a local JSON file in [`data/`](data).
- Shared loading logic lives in [`utils/data_loader.py`](utils/data_loader.py).
- Shared styling helpers live in [`utils/__init__.py`](utils/__init__.py).
- Reusable Plotly chart builders live in [`utils/charts.py`](utils/charts.py).
- The app entrypoint is [`app.py`](app.py), and Streamlit automatically exposes the page modules under [`pages/`](pages).

## Local Development

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the app

```powershell
streamlit run app.py
```

By default, Streamlit serves the dashboard at `http://localhost:8501`.

## Docker

Build the image:

```powershell
docker build -t dc-dashboard .
```

Run the container:

```powershell
docker run -p 8501:8501 dc-dashboard
```

The container starts Streamlit in headless mode and exposes port `8501`.

## AWS Deployment

The [`infra/`](infra) folder contains Terraform for deploying the dashboard to AWS using:

- VPC with public subnets
- Internet Gateway and route table
- Application Load Balancer
- ECS Cluster
- ECS Fargate service
- ECR repository
- CloudWatch log group
- IAM roles for ECS task execution

### Terraform workflow

From the `infra` directory:

```powershell
terraform init
terraform plan
terraform apply
```

### Current Terraform variables

The default `terraform.tfvars` is configured for:

- AWS region: `us-east-1`
- Project name: `dc-dashboard`
- Environment: `dev`
- Container port: `8501`
- Desired task count: `1`

After apply, Terraform outputs the ALB DNS name and application URL.

## Data Format

Each JSON file stores one dashboard domain as named sections. During runtime, those sections are converted into Pandas DataFrames. The app expects consistent columns such as:

- `Year`
- `Source URL`
- Domain-specific benchmark or note fields

If you update or replace the datasets, keep the section names and column structure aligned with the page code that consumes them.

## Notes

- The dashboard is built around 2023-2025 research, with some current operator references where public Mexico-specific benchmarks are limited.
- The app is fully static in terms of data sourcing at runtime: it does not fetch external APIs.
- There is currently no automated test suite in the repository.

## Main Files

- Entry point: [`app.py`](app.py)
- Energy page: [`pages/02_energy.py`](pages/02_energy.py)
- Data loaders: [`utils/data_loader.py`](utils/data_loader.py)
- Chart builders: [`utils/charts.py`](utils/charts.py)
- Infrastructure: [`infra/main.tf`](infra/main.tf)