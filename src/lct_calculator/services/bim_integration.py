import logging

logger = logging.getLogger(__name__)


def sincronizar_bim(fundacao_id: int) -> None:
    """
    Stub de sincronização BIM — SQLite removido na Sprint 0.
    Será reimplementado com PostgreSQL na Sprint 1.

    :param fundacao_id: ID da fundação a ser sincronizada.
    """
    logger.warning(
        "sincronizar_bim: persistência SQLite removida. "
        "Reimplementar com PostgreSQL na Sprint 1. fundacao_id=%s",
        fundacao_id,
    )
    raise NotImplementedError(
        "BIM sync requer persistência PostgreSQL (Sprint 1). "
        f"fundacao_id={fundacao_id}"
    )
