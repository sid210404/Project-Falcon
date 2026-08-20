"""Export serializers for strategy-comparison results."""

from __future__ import annotations

import pandas as pd

from app.comparison.comparison_result import ComparisonResult


class ComparisonReport:
    """Create portable exports without coupling reports to Streamlit."""

    @staticmethod
    def dataframe(results: list[ComparisonResult]) -> pd.DataFrame:
        """Build a display-ready comparison table."""
        return pd.DataFrame(
            [
                {"Strategy": item.strategy_name, **item.metrics.to_dict()}
                for item in results
            ]
        )

    @classmethod
    def to_html(cls, results: list[ComparisonResult]) -> str:
        """Create a standalone HTML comparison report."""
        table = cls.dataframe(results).to_html(index=False, border=0)
        return f"""<!doctype html>
<html><head><meta charset=\"utf-8\"><title>Falcon Strategy Comparison</title>
<style>body{{font-family:Arial,sans-serif;margin:32px;color:#1f2937}} table{{border-collapse:collapse;width:100%}} th,td{{padding:10px;border:1px solid #d1d5db;text-align:right}} th{{background:#131722;color:#fff}} th:first-child,td:first-child{{text-align:left}}</style>
</head><body><h1>Project Falcon Strategy Comparison</h1>{table}</body></html>"""

    @classmethod
    def to_pdf(cls, results: list[ComparisonResult]) -> bytes:
        """Create a compact, dependency-free PDF summary for download."""
        lines = ["Project Falcon - Strategy Comparison", ""]
        for item in results:
            metrics = item.metrics
            lines.append(
                f"{item.strategy_name}: Net Profit {metrics.net_profit:.2f}, "
                f"Return {metrics.return_pct:.2f}%, Sharpe {metrics.sharpe_ratio:.2f}"
            )
        escaped_lines = [
            line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            for line in lines
        ]
        stream = "BT /F1 12 Tf 72 760 Td " + " ".join(
            f"({line}) Tj T*" for line in escaped_lines
        ) + " ET"
        objects = [
            "<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
            f"<< /Length {len(stream.encode('latin-1'))} >>\\nstream\\n{stream}\\nendstream",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        ]
        document = "%PDF-1.4\\n"
        offsets: list[int] = []
        for index, obj in enumerate(objects, start=1):
            offsets.append(len(document.encode("latin-1")))
            document += f"{index} 0 obj\\n{obj}\\nendobj\\n"
        xref = len(document.encode("latin-1"))
        document += f"xref\\n0 {len(objects) + 1}\\n0000000000 65535 f \\n"
        document += "".join(f"{offset:010d} 00000 n \\n" for offset in offsets)
        document += f"trailer\\n<< /Size {len(objects) + 1} /Root 1 0 R >>\\nstartxref\\n{xref}\\n%%EOF"
        return document.encode("latin-1")
