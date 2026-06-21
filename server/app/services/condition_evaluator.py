

def evaluate_conditions(condition: str, context: dict):
    '''Evaluates the condition string of a workflow step and returns whether or not the step 
    needs to be executed or not'''
    allowed_globals = {}

    allowed_locals = context

    try:
        return eval(condition, allowed_globals, allowed_locals)
    except Exception:
        return False