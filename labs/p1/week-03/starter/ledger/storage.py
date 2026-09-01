"""Storage backends. `standard` track — you write these.

`Storage` must be a `Protocol`, not an ABC, so that a backend never imports the core.
The `hard` track depends on that being true.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol, runtime_checkable

from .models import Account, Transaction


@runtime_checkable
class Storage(Protocol):
    def put_account(self, account: Account) -> None: ...
    def get_account(self, account_id: str) -> Account | None: ...
    def accounts(self) -> Iterator[Account]: ...
    def put_transaction(self, txn: Transaction) -> None: ...
    def has_transaction(self, txn_id: str) -> bool: ...
    def transactions(self) -> Iterator[Transaction]: ...


class MemoryStorage:
    """TODO (standard): everything in dicts."""

    def __init__(self) -> None:
        raise NotImplementedError("MemoryStorage")


class JsonFileStorage:
    """TODO (standard): one JSON document on disk, rewritten *atomically*
    (temp file + os.replace) on every write. A partial write into the real path
    is how you lose a ledger."""

    def __init__(self, path: object) -> None:
        raise NotImplementedError("JsonFileStorage")
