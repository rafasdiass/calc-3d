# ── Estágio base ───────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ── Dependências ────────────────────────────────────────────────────────────
FROM base AS deps

COPY requirements/base.txt requirements/prod.txt ./requirements/
RUN pip install -r requirements/prod.txt

# ── Código fonte ────────────────────────────────────────────────────────────
FROM deps AS runtime

COPY src/ ./src/
COPY pyproject.toml ./

# Instala o pacote em modo editável para que os imports funcionem
RUN pip install --no-deps -e .

EXPOSE 8000

CMD ["uvicorn", "lct_calculator.apps.api.main:app", \
     "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
