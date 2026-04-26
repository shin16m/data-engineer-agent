def gate_result(name: str, passed: bool, note: str = "") -> dict:
    return {
        "gate": name,
        "passed": passed,
        "note": note,
    }

