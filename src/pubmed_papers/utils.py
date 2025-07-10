import sys

class DebugUtil:
    enabled: bool = False

    @staticmethod
    def debug_print(msg: str) -> None:
        if DebugUtil.enabled:
            print(f"[DEBUG] {msg}", file=sys.stderr)