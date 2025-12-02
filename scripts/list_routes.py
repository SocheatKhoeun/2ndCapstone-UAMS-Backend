import sys
import pathlib

# Ensure project root is on sys.path so `app` package can be imported when running from scripts/
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app
from fastapi.routing import APIRoute

def get_dep_names(route: APIRoute):
    names = []
    # route.dependant may have dependencies
    try:
        for d in getattr(route, "dependant", getattr(route, "dependant", None)).dependencies or []:
            fn = getattr(d, "call", None)
            if fn:
                names.append(getattr(fn, "__name__", repr(fn)))
            else:
                names.append(repr(d))
    except Exception:
        pass
    # route.dependencies (explicit)
    try:
        for d in getattr(route, "dependencies", []) or []:
            fn = getattr(d, "call", None) or d
            names.append(getattr(fn, "__name__", repr(fn)))
    except Exception:
        pass
    return list(dict.fromkeys(names))


def is_protected(dep_names):
    # Consider various dependency name patterns used for auth/role guards
    keywords = ("require_roles", "require_roles_claims", "get_current_user", "get_current_admin", "get_current_", "role_guard", "role")
    for n in dep_names:
        ln = n.lower() if isinstance(n, str) else str(n).lower()
        if any(token in ln for token in keywords):
            return True
    return False


def main():
    print("Scanning routes from app...\n")
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        methods = ",".join(sorted(route.methods))
        deps = get_dep_names(route)
        protected = is_protected(deps)
        print(f"{route.path:40} {methods:12} protected={protected} deps={deps}")

if __name__ == '__main__':
    main()
