"""
Object storage client — Sprint 0 stub.

Sprint 1: S3-compatible (AWS S3 / Cloudflare R2 / MinIO) via aioboto3.

Configuração via env:
  S3_ENDPOINT_URL   (opcional — para R2/MinIO)
  S3_ACCESS_KEY_ID
  S3_SECRET_ACCESS_KEY
  S3_BUCKET_NAME    (default: calc3d-artifacts)
"""
from __future__ import annotations

import os

S3_BUCKET: str = os.getenv("S3_BUCKET_NAME", "calc3d-artifacts")
S3_ENDPOINT: str | None = os.getenv("S3_ENDPOINT_URL")

# Sprint 1:
# import aioboto3
# _session = aioboto3.Session()
#
# async def upload_artifact(key: str, data: bytes, content_type: str) -> str:
#     async with _session.client("s3", endpoint_url=S3_ENDPOINT) as s3:
#         await s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data, ContentType=content_type)
#     return f"{S3_ENDPOINT or 'https://s3.amazonaws.com'}/{S3_BUCKET}/{key}"


async def upload_artifact(key: str, data: bytes, content_type: str) -> str:
    """Sprint 0 placeholder — retorna URL fake. Sprint 1: upload real."""
    _ = key, data, content_type  # silence unused warnings
    return f"s3://{S3_BUCKET}/{key}"
