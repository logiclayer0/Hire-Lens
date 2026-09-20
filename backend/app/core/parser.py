from pathlib import Path
from app.utils.files import extract_text


class Parser:
    def parse(self, path: Path) -> dict:
        text = extract_text(path)
        lines = [ln.strip() for ln in text.splitlines()]
        non_empty = [ln for ln in lines if ln]
        return {
            "filename": path.name,
            "path": str(path),
            "text": text,
            "line_count": len(non_empty),
            "char_count": len(text),
            "lines": non_empty,
        }


parser = Parser()