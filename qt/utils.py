"""Internal helpers for Qt compatibility shims."""


def resolve_enum(owner, scope_name, value_name):
    scope = getattr(owner, scope_name, None)
    if scope is not None:
        value = getattr(scope, value_name, None)
        if value is not None:
            return value
            
    return getattr(owner, value_name)
