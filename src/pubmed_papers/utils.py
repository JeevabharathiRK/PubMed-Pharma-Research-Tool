import sys

class DebugUtil:
    enabled: bool = False

    @staticmethod
    def debug_print(msg: str, error: bool = False) -> None:
        """
        Print debug message if enabled, or always raise RuntimeError if error=True.
        """
        if error:
            raise RuntimeError(msg if DebugUtil.enabled else "An error occurred. Try run using -d flag")
        if DebugUtil.enabled:
            print(f"[DEBUG] {msg}", file=sys.stderr)