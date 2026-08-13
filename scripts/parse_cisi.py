
"""
Convert the raw CISI collection into JSON.

Input:
    datasets/cisi/CISI.ALL
    datasets/cisi/CISI.QRY
    datasets/cisi/CISI.REL

Output:
    datasets/cisi/documents.json
    datasets/cisi/queries.json
    datasets/cisi/qrels.json

The parser deliberately preserves the structure of the original
CISI collection instead of mapping it directly onto the IR Lab's
internal Document/Query models.

CISI.ALL fields:
    .I  Document ID
    .T  Title
    .A  Author(s)
    .W  Abstract / document text
    .X  References / citation information

CISI.QRY:
    .I  Query ID
    .W  Query text

CISI.REL:
    Query-document relevance pairs
"""

from __future__ import annotations

import json
from pathlib import Path


DATASET_DIR = Path("datasets/cisi")

CISI_ALL = DATASET_DIR / "CISI.ALL"
CISI_QRY = DATASET_DIR / "CISI.QRY"
CISI_REL = DATASET_DIR / "CISI.REL"

DOCUMENTS_JSON = DATASET_DIR / "documents.json"
QUERIES_JSON = DATASET_DIR / "queries.json"
QRELS_JSON = DATASET_DIR / "qrels.json"


# ---------------------------------------------------------------------------
# Generic CISI record parser
# ---------------------------------------------------------------------------

def parse_records(path: Path) -> list[dict]:
    """
    Parse a CISI marker-based file.

    Records begin with:
        .I <id>

    Subsequent lines beginning with "." introduce fields.

    Everything else belongs to the current field.
    """

    records: list[dict] = []

    current: dict | None = None
    current_field: str | None = None

    with path.open("r", encoding="utf-8", errors="replace") as file:

        for raw_line in file:
            line = raw_line.rstrip("\n\r")

            # ---------------------------------------------------------------
            # New record
            # ---------------------------------------------------------------

            if line.startswith(".I"):

                if current is not None:
                    records.append(current)

                parts = line.split(maxsplit=1)

                if len(parts) != 2:
                    raise ValueError(
                        f"Malformed record identifier in {path}: {line!r}"
                    )

                current = {
                    "id": int(parts[1]),
                }

                current_field = None
                continue

            # Ignore content before the first .I
            if current is None:
                continue

            # ---------------------------------------------------------------
            # New field
            # ---------------------------------------------------------------

            if line.startswith(".") and len(line) >= 2:

                field = line[1:2]

                current_field = field

                # Keep fields as lists initially. This avoids losing
                # information if a field occurs more than once.
                current.setdefault(field, [])

                continue

            # ---------------------------------------------------------------
            # Field content
            # ---------------------------------------------------------------

            if current_field is not None:
                current[current_field].append(line)

    # Append final record.
    if current is not None:
        records.append(current)

    return records


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def collapse_lines(lines: list[str]) -> str:
    """
    Convert CISI's physical lines into a single logical string.

    Multiple whitespace characters are normalized.
    """

    return " ".join(
        " ".join(lines).split()
    )


def normalize_documents(records: list[dict]) -> list[dict]:
    """
    Convert raw CISI.ALL records into readable JSON while preserving
    the important fields.
    """

    documents = []

    for record in records:

        document = {
            "id": record["id"],
            "title": collapse_lines(record.get("T", [])),
            "authors": collapse_lines(record.get("A", [])),
            "text": collapse_lines(record.get("W", [])),
            "references": [
                line.strip()
                for line in record.get("X", [])
                if line.strip()
            ],
        }

        documents.append(document)

    return documents


def normalize_queries(records: list[dict]) -> list[dict]:
    """
    Convert CISI.QRY records.
    """

    queries = []

    for record in records:

        query = {
            "id": record["id"],
            "text": collapse_lines(record.get("W", [])),
        }

        queries.append(query)

    return queries


# ---------------------------------------------------------------------------
# Qrels
# ---------------------------------------------------------------------------

def parse_qrels(path: Path) -> list[dict]:
    """
    Parse CISI.REL.

    CISI relevance lines contain:
        query_id document_id

    Some versions contain additional columns. We preserve those as
    'extra' rather than silently throwing them away.
    """

    qrels = []

    with path.open("r", encoding="utf-8", errors="replace") as file:

        for line_number, raw_line in enumerate(file, start=1):

            line = raw_line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 2:
                raise ValueError(
                    f"Malformed qrel at line {line_number}: {line!r}"
                )

            query_id = int(parts[0])
            document_id = int(parts[1])

            qrel = {
                "query_id": query_id,
                "document_id": document_id,
            }

            # Preserve additional columns if present.
            if len(parts) > 2:
                qrel["extra"] = parts[2:]

            qrels.append(qrel)

    return qrels


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def write_json(path: Path, data: object) -> None:

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

        file.write("\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:

    for path in (CISI_ALL, CISI_QRY, CISI_REL):

        if not path.exists():
            raise FileNotFoundError(
                f"Missing CISI file: {path}"
            )

    print("[1/3] Parsing CISI.ALL...")
    raw_documents = parse_records(CISI_ALL)
    documents = normalize_documents(raw_documents)

    print(f"      Documents: {len(documents)}")

    print("[2/3] Parsing CISI.QRY...")
    raw_queries = parse_records(CISI_QRY)
    queries = normalize_queries(raw_queries)

    print(f"      Queries:   {len(queries)}")

    print("[3/3] Parsing CISI.REL...")
    qrels = parse_qrels(CISI_REL)

    print(f"      Qrels:     {len(qrels)}")

    write_json(DOCUMENTS_JSON, documents)
    write_json(QUERIES_JSON, queries)
    write_json(QRELS_JSON, qrels)

    print()
    print("CISI converted successfully:")
    print(f"  {DOCUMENTS_JSON}")
    print(f"  {QUERIES_JSON}")
    print(f"  {QRELS_JSON}")


if __name__ == "__main__":
    main()
