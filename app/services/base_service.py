from typing import Any, Dict, Optional, Sequence, List, Tuple
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_, text, String, cast
from sqlalchemy.orm import joinedload
from app.core.errors import NotFound
from datetime import datetime, timezone
from typing import Iterable, Set
from starlette.requests import Request
from app.utils.jwt_utils import decode_access_token
from app.core.config import settings


class BaseService:
    """Generic async BaseService offering common CRUD, status and list helpers.

    Intended to be subclassed. Subclasses should set `model` to the SQLAlchemy
    declarative model class they operate on, or override `get_model()`.
    """

    model = None  # override in subclass
    status_column = "active"

    def __init__(self, db: AsyncSession, request: Optional[Request] = None) -> None:
        self.db = db
        # optional Request injected by controller helper; when present
        # BaseService.list will read query params (page, limit, q, sort/filter)
        # so controllers don't need to forward them explicitly.
        self.request: Optional[Request] = request

    def get_model(self):
        if self.model is None:
            raise RuntimeError("BaseService.model must be set in subclasses")
        return self.model

    def _is_request_admin(self) -> bool:
        """Return True if the current request carries an admin token.

        Defensive: any error or missing token -> False.
        """
        if not hasattr(self, "request") or self.request is None:
            return False
        auth = self.request.headers.get("Authorization")
        if not auth:
            return False
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return False
        token = parts[1]
        try:
            payload = decode_access_token(token, settings.JWT_PRIVATE)
        except Exception:
            return False
        role = payload.get("role") if isinstance(payload, dict) else None
        if isinstance(role, str) and role.lower() in ("admin", "superadmin"):
            return True
        if isinstance(role, (list, tuple)) and any(str(r).lower() in ("admin", "superadmin") for r in role):
            return True
        return False

    async def get(self, id: int):
        """Return a model instance by primary id or raise NotFound."""
        Model = self.get_model()
        row = await self.db.get(Model, id)
        if not row:
            raise NotFound(f"{Model.__name__} not found")
        # If model exposes a status column, enforce access rules:
        status_val = getattr(row, self.status_column, None)
        # always disallow access to deleted rows (2)
        if status_val == 2:
            raise NotFound(f"{Model.__name__} not found")
        # non-admins must only see active==1 rows
        if status_val is not None and status_val != 1 and not self._is_request_admin():
            raise NotFound(f"{Model.__name__} not found")
        return row

    async def get_one_by(self, column: str, value):
        """Return a single model instance matching column==value or None.

        Useful for uniqueness checks and simple lookups.
        """
        Model = self.get_model()
        if not hasattr(Model, column):
            return None
        q = select(Model).where(getattr(Model, column) == value)
        return await self.db.scalar(q)

    async def exists_by(self, column: str, value) -> bool:
        """Return True if a row exists with column==value."""
        row = await self.get_one_by(column, value)
        return row is not None

    async def create(self, payload: Dict[str, Any]):
        Model = self.get_model()
        # Support both dict payloads and Pydantic models by converting
        # Pydantic objects to dict via .dict(exclude_unset=True)
        if hasattr(payload, "dict"):
            # Exclude unset and None values so DB server defaults (e.g. enrolled_at)
            # are applied when the client didn't provide the field.
            data = payload.dict(exclude_unset=True, exclude_none=True)
        else:
            data = dict(payload or {})

        instance = Model(**data)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update_by_global_id(self, global_id: str, payload: Dict[str, Any]):
        Model = self.get_model()
        q = select(Model).where(getattr(Model, "global_id") == global_id)
        row = await self.db.scalar(q)
        if not row:
            raise NotFound(f"{Model.__name__} not found")
        # Prevent updates on deleted rows
        status_val = getattr(row, self.status_column, None)
        if status_val == 2:
            raise NotFound(f"{Model.__name__} not found")
        # Non-admins cannot update rows that are not active
        if status_val is not None and status_val != 1 and not self._is_request_admin():
            raise NotFound(f"{Model.__name__} not found")
        # Support both dict payloads and Pydantic models by converting
        # Pydantic objects to dict via .dict(exclude_unset=True)
        if hasattr(payload, "dict"):
            data = payload.dict(exclude_unset=True)
        else:
            data = dict(payload or {})

        for k, v in data.items():
            if hasattr(row, k):
                setattr(row, k, v)
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def get_by_global_id(self, global_id: str):
        Model = self.get_model()
        q = select(Model).where(getattr(Model, "global_id") == global_id)
        row = await self.db.scalar(q)
        if not row:
            raise NotFound(f"{Model.__name__} not found")
        status_val = getattr(row, self.status_column, None)
        # always disallow access to deleted rows
        if status_val == 2:
            raise NotFound(f"{Model.__name__} not found")
        # non-admins must only see active rows
        if status_val is not None and status_val != 1 and not self._is_request_admin():
            raise NotFound(f"{Model.__name__} not found")
        return row

    async def get_id_by_global_id(self, global_id: str) -> int:
        row = await self.get_by_global_id(global_id)
        return int(getattr(row, "id"))

    async def set_status_by_global_id(self, global_id: str, value: int):
        Model = self.get_model()
        q = select(Model).where(getattr(Model, "global_id") == global_id)
        row = await self.db.scalar(q)
        if not row:
            raise NotFound(f"{Model.__name__} not found")
        setattr(row, self.status_column, int(value))
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def delete_by_global_id(self, global_id: str):
        """Soft-delete by setting status column to 2 (deleted).

        This is the standard admin-friendly delete behavior used across controllers.
        Subclasses may override if they require physical deletion.
        """
        return await self.set_status_by_global_id(global_id, 2)

    def _ms_to_dt(self, val: Optional[int]) -> Optional[datetime]:
        if val is None:
            return None
        try:
            # Expect milliseconds since epoch UTC
            return datetime.fromtimestamp(val / 1000.0, tz=timezone.utc)
        except Exception:
            return None

    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        q: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        columns: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
        date_from_ms: Optional[int] = None,
        date_to_ms: Optional[int] = None,
        date_col: Optional[str] = "created_at",
        with_relations: Optional[List[str]] = None,
        with_count: Optional[List[str]] = None,
        page: Optional[int] = None,
    ) -> Sequence[Any]:
        """Return rows matching filters and pagination.

        Supports simple q search, filters, dot-path relation filters
        (e.g. "rel.column"), sorting and date range on created_at.
        Filters with string values perform ILIKE partial match.
        """
        # If controller attached a Request to this service instance, prefer
        # reading pagination / filter args from it when the caller did not
        # explicitly provide them. This allows controllers to simply call
        # `svc.list()` and let the BaseService pick params from the route.
        if hasattr(self, "request") and self.request is not None:
            qp = self.request.query_params
            # page and limit
            try:
                page = int(qp.get("page")) if qp.get("page") is not None else page
            except Exception:
                pass
            try:
                limit = int(qp.get("limit")) if qp.get("limit") is not None else limit
            except Exception:
                pass
            # simple fields
            q = qp.get("q") or q
            sort_by = qp.get("sort_by") or sort_by
            sort_dir = qp.get("sort_dir") or sort_dir
            # date range
            try:
                date_from_ms = int(qp.get("date_from_ms")) if qp.get("date_from_ms") is not None else date_from_ms
            except Exception:
                pass
            try:
                date_to_ms = int(qp.get("date_to_ms")) if qp.get("date_to_ms") is not None else date_to_ms
            except Exception:
                pass
            # parse filter[...] params into filters dict
            if not filters:
                filters = {}
            for k, v in qp.items():
                if k.startswith("filter[") and k.endswith("]"):
                    key = k[len("filter["):-1]
                    # keep last value if multiple provided for same key
                    filters[key] = v

        Model = self.get_model()
        stmt = select(Model)

        # By default return only active rows (active==1) when model has a status column.
        # If caller provided an explicit filter for the status column in `filters`, honor that
        # only for admin requests. Regular users will never see inactive (0) or deleted (2) rows.
        def _request_is_admin() -> bool:
            # Inspect Authorization header and decode token; be defensive — any error -> not admin
            if not hasattr(self, "request") or self.request is None:
                return False
            auth = self.request.headers.get("Authorization")
            if not auth:
                return False
            parts = auth.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return False
            token = parts[1]
            try:
                payload = decode_access_token(token, settings.JWT_PRIVATE)
            except Exception:
                return False
            role = payload.get("role") if isinstance(payload, dict) else None
            if isinstance(role, str) and role.lower() in ("admin", "superadmin"):
                return True
            if isinstance(role, (list, tuple)) and any(str(r).lower() in ("admin", "superadmin") for r in role):
                return True
            return False

        if hasattr(Model, self.status_column):
            is_admin = _request_is_admin()
            # For non-admins, always enforce active==1 regardless of caller-supplied filters
            if not filters:
                if not is_admin:
                    filters = {self.status_column: 1}
            else:
                # if caller didn't request the status column explicitly, default to active==1
                if self.status_column not in filters:
                    # don't mutate caller's dict if it's not a plain dict
                    try:
                        filters = dict(filters)
                    except Exception:
                        filters = {**filters}
                    if not is_admin:
                        filters[self.status_column] = 1
                else:
                    # caller requested the status column explicitly; if they're not admin,
                    # force the value to 1 to prevent seeing inactive/deleted rows
                    if not is_admin:
                        try:
                            filters = dict(filters)
                        except Exception:
                            filters = {**filters}
                        filters[self.status_column] = 1

        where_clauses = []
        if filters:
            for col, val in filters.items():
                # normalize numeric CSV strings to int or list[int] to avoid ILIKE on numeric columns
                if isinstance(val, str):
                    s = val.strip()
                    if re.fullmatch(r"\d+(,\d+)*", s):
                        if "," in s:
                            parts = [p.strip() for p in s.split(",")]
                            try:
                                val = [int(p) for p in parts]
                            except Exception:
                                pass
                        else:
                            try:
                                val = int(s)
                            except Exception:
                                pass
                if "." in col:
                    # relation filter
                    rel, rel_col = col.split(".", 1)
                    # use exists/select via text to avoid complex generic joins here
                    clause = text(f"EXISTS(SELECT 1 FROM {rel} WHERE {rel}.id = {Model.__tablename__}.{rel}_id AND {rel}.{rel_col} = :val)")
                    where_clauses.append(clause.bindparams(val=val))
                else:
                    if not hasattr(Model, col):
                        continue
                    col_attr = getattr(Model, col)
                    if isinstance(val, str):
                        # prefer ilike on the column if available, otherwise cast to text
                        if hasattr(col_attr, "ilike"):
                            where_clauses.append(col_attr.ilike(f"%{val}%"))
                        else:
                            where_clauses.append(cast(col_attr, String).ilike(f"%{val}%"))
                    elif isinstance(val, (list, tuple, set)):
                        where_clauses.append(col_attr.in_(list(val)))
                    else:
                        where_clauses.append(col_attr == val)

        # date range (apply to selectable date column, default created_at)
        dt_from = self._ms_to_dt(date_from_ms)
        dt_to = self._ms_to_dt(date_to_ms)
        if date_col and hasattr(Model, date_col):
            date_attr = getattr(Model, date_col)
            if dt_from and dt_to:
                where_clauses.append(date_attr >= dt_from)
                where_clauses.append(date_attr <= dt_to)
            elif dt_from:
                where_clauses.append(date_attr >= dt_from)
            elif dt_to:
                where_clauses.append(date_attr <= dt_to)

        if q and columns:
            q_term = f"%{q}%"
            or_exprs = []
            for col in columns:
                if "." in col:
                    # skip relation columns in free-text search for simplicity
                    continue
                if not hasattr(Model, col):
                    continue
                col_attr = getattr(Model, col)
                if hasattr(col_attr, "ilike"):
                    or_exprs.append(col_attr.ilike(q_term))
                else:
                    or_exprs.append(cast(col_attr, String).ilike(q_term))
            if or_exprs:
                where_clauses.append(or_(*or_exprs))

        # Always exclude deleted rows (status == 2) from list results.
        if hasattr(Model, self.status_column):
            status_attr = getattr(Model, self.status_column)
            where_clauses.append(status_attr != 2)

        if where_clauses:
            stmt = stmt.where(and_(*where_clauses))

        # sorting
        if sort_by and hasattr(Model, sort_by):
            col = getattr(Model, sort_by)
            if sort_dir and str(sort_dir).lower() == "desc":
                stmt = stmt.order_by(col.desc())
            else:
                stmt = stmt.order_by(col.asc())
        else:
            # default
            if hasattr(Model, "id"):
                stmt = stmt.order_by(getattr(Model, "id").asc())

        # eager loads
        if with_relations:
            for r in with_relations:
                stmt = stmt.options(joinedload(r))

        # pagination
        # If caller provided page, compute skip from page (1-indexed)
        if page is not None:
            if page < 1:
                page = 1
            skip = (page - 1) * limit

        stmt = stmt.offset(skip).limit(limit)

        results = await self.db.scalars(stmt)
        rows = results.all()

        # If page was requested, return pagination payload instead of raw rows
        if page is not None:
            # Attempt to get total using count(); fall back to len(rows)
            try:
                total = await self.count(q=q, filters=filters, columns=columns, date_from_ms=date_from_ms, date_to_ms=date_to_ms, date_col=date_col)
            except TypeError:
                try:
                    total = len(rows)
                except Exception:
                    total = 0

            per_page = limit
            total_pages = (total + per_page - 1) // per_page if per_page else 0
            next_page = page + 1 if page < total_pages else None
            prev_page = page - 1 if page > 1 else None

            return {
                "items": rows,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "next_page": next_page,
                "prev_page": prev_page,
            }

        return rows

    async def count(
        self,
        q: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        columns: Optional[List[str]] = None,
        date_from_ms: Optional[int] = None,
        date_to_ms: Optional[int] = None,
        date_col: Optional[str] = "created_at",
    ) -> int:
        """Count rows matching the same filter/q/date logic used by list()."""
        Model = self.get_model()

        where_clauses = []
        if filters:
            for col, val in filters.items():
                # normalize numeric CSV strings to int or list[int]
                if isinstance(val, str):
                    s = val.strip()
                    if re.fullmatch(r"\d+(,\d+)*", s):
                        if "," in s:
                            parts = [p.strip() for p in s.split(",")]
                            try:
                                val = [int(p) for p in parts]
                            except Exception:
                                pass
                        else:
                            try:
                                val = int(s)
                            except Exception:
                                pass
                if "." in col:
                    rel, rel_col = col.split(".", 1)
                    clause = text(f"EXISTS(SELECT 1 FROM {rel} WHERE {rel}.id = {Model.__tablename__}.{rel}_id AND {rel}.{rel_col} = :val)")
                    where_clauses.append(clause.bindparams(val=val))
                else:
                    if not hasattr(Model, col):
                        continue
                    col_attr = getattr(Model, col)
                    if isinstance(val, str):
                        where_clauses.append(col_attr.ilike(f"%{val}%"))
                    elif isinstance(val, (list, tuple, set)):
                        where_clauses.append(col_attr.in_(list(val)))
                    else:
                        where_clauses.append(col_attr == val)

        # date range (apply to selectable date column, default created_at)
        dt_from = self._ms_to_dt(date_from_ms)
        dt_to = self._ms_to_dt(date_to_ms)
        if date_col and hasattr(Model, date_col):
            date_attr = getattr(Model, date_col)
            if dt_from and dt_to:
                where_clauses.append(date_attr >= dt_from)
                where_clauses.append(date_attr <= dt_to)
            elif dt_from:
                where_clauses.append(date_attr >= dt_from)
            elif dt_to:
                where_clauses.append(date_attr <= dt_to)

        if q and columns:
            q_term = f"%{q}%"
            or_exprs = []
            for col in columns:
                if "." in col:
                    continue
                if hasattr(Model, col):
                    or_exprs.append(getattr(Model, col).ilike(q_term))
            if or_exprs:
                where_clauses.append(or_(*or_exprs))

        # Always exclude deleted rows (status == 2) from count results.
        count_stmt = select(func.count()).select_from(Model)
        if hasattr(Model, self.status_column):
            status_attr = getattr(Model, self.status_column)
            where_clauses.append(status_attr != 2)
        if where_clauses:
            count_stmt = count_stmt.where(and_(*where_clauses))
        total = await self.db.scalar(count_stmt)
        return int(total or 0)

    # pagination is handled via list(page=...) which returns a pagination payload


async def generic_list(
    db: AsyncSession,
    model,
    *,
    skip: int = 0,
    limit: int = 50,
    q: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    sort_by: Optional[str] = None,
    sort_dir: Optional[str] = None,
    allowed_cols: Optional[Set[str]] = None,
    text_cols: Optional[Iterable] = None,
):
    """Lightweight wrapper exposing the same filters as BaseService.list for
    services that prefer a functional approach.
    """
    svc = BaseService(db)
    svc.model = model
    cols = [c.key for c in (text_cols or []) if hasattr(c, "key")]
    rows = await svc.list(skip=skip, limit=limit, q=q, filters=filters, sort_by=sort_by, sort_dir=sort_dir, columns=cols)
    return rows


async def generic_count(
    db: AsyncSession,
    model,
    *,
    q: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    allowed_cols: Optional[Set[str]] = None,
    text_cols: Optional[Iterable] = None,
) -> int:
    svc = BaseService(db)
    svc.model = model
    cols = [c.key for c in (text_cols or []) if hasattr(c, "key")]
    total = await svc.count(q=q, filters=filters, columns=cols)
    return total