

def evaluate_conditions(condition: str, context: dict):
    allowed_globals = {}

    allowed_locals = context

    try:
        return eval(condition, allowed_globals, allowed_locals)
    except Exception:
        return False