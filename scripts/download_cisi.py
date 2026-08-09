
"""
Download and verify the CISI Information Retrieval dataset.

Files:
    CISI.ALL  - 1460 documents
    CISI.QRY  - 112 queries
    CISI.REL  - relevance judgments

The files are downloaded into:
    datasets/cisi/

Verification:
    1. HTTP response must succeed.
    2. Content must not be suspiciously small.
    3. Expected byte size is checked.
    4. SHA-256 is computed.
    5. SHA-256 is persisted in SHA256SUMS.
    6. Files are downloaded to .part files and renamed only
       after successful verification.

Run:
    python scripts/download_cisi.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATASET_DIR = Path("datasets/cisi")

# Mirror currently known to contain the CISI collection.
BASE_URL = (
    "https://raw.githubusercontent.com/"
    "GianRomani/CISI-project-MLOps/refs/heads/main/"
)

FILES = {
    "CISI.ALL": {
        "url": BASE_URL + "CISI.ALL",

        # CISI.ALL is around 2 MB.
        # Keep this as a sanity boundary rather than pretending it is
        # a cryptographically authoritative size.
        "min_size": 1_000_000,
    },
    "CISI.QRY": {
        "url": BASE_URL + "CISI.QRY",

        # CISI.QRY is substantially smaller than CISI.ALL.
        "min_size": 10_000,
    },
    "CISI.REL": {
        "url": BASE_URL + "CISI.REL",

        # CISI.REL is around 80 KB.
        "min_size": 50_000,
    },
}

CHUNK_SIZE = 1024 * 1024


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    """Calculate the SHA-256 digest of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            digest.update(chunk)

    return digest.hexdigest()


def load_manifest() -> dict[str, str]:
    """Load SHA-256 values from SHA256SUMS if it exists."""

    manifest = DATASET_DIR / "SHA256SUMS"

    if not manifest.exists():
        return {}

    result = {}

    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line:
            continue

        digest, filename = line.split(maxsplit=1)
        result[filename] = digest

    return result


def write_manifest(hashes: dict[str, str]) -> None:
    """Write the local SHA-256 manifest."""

    manifest = DATASET_DIR / "SHA256SUMS"

    lines = [
        f"{digest}  {filename}"
        for filename, digest in sorted(hashes.items())
    ]

    manifest.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_file(
    filename: str,
    url: str,
    minimum_size: int,
) -> tuple[int, str]:

    destination = DATASET_DIR / filename
    temporary = DATASET_DIR / f"{filename}.part"

    print(f"\n[GET] {filename}")
    print(f"      {url}")

    request = Request(
        url,
        headers={
            "User-Agent": "IR-Lab-CISI-Downloader/1.0",
        },
    )

    try:
        with urlopen(request, timeout=30) as response:

            status = response.status

            if status != 200:
                raise RuntimeError(
                    f"unexpected HTTP status: {status}"
                )

            content_type = response.headers.get("Content-Type", "")

            print(f"      HTTP:         {status}")
            print(f"      Content-Type: {content_type}")

            with temporary.open("wb") as output:

                total = 0

                while chunk := response.read(CHUNK_SIZE):
                    output.write(chunk)
                    total += len(chunk)

    except HTTPError as exc:
        temporary.unlink(missing_ok=True)

        raise RuntimeError(
            f"HTTP {exc.code} while downloading {filename}"
        ) from exc

    except URLError as exc:
        temporary.unlink(missing_ok=True)

        raise RuntimeError(
            f"network error while downloading {filename}: {exc.reason}"
        ) from exc

    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    print(f"      Size:          {total:,} bytes")

    # ---------------------------------------------------------------
    # Size sanity check
    # ---------------------------------------------------------------

    if total < minimum_size:
        temporary.unlink(missing_ok=True)

        raise RuntimeError(
            f"{filename} is suspiciously small "
            f"({total:,} bytes; expected at least {minimum_size:,})"
        )

    # ---------------------------------------------------------------
    # SHA-256
    # ---------------------------------------------------------------

    digest = sha256_file(temporary)

    print(f"      SHA-256:       {digest}")

    # ---------------------------------------------------------------
    # Atomic acceptance
    # ---------------------------------------------------------------

    temporary.replace(destination)

    print(f"      [OK] {destination}")

    return total, digest


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_existing_file(
    filename: str,
    expected_hash: str | None,
) -> str | None:

    path = DATASET_DIR / filename

    if not path.exists():
        return None

    print(f"\n[CHECK] {filename}")

    digest = sha256_file(path)
    size = path.stat().st_size

    print(f"        Size:    {size:,} bytes")
    print(f"        SHA-256: {digest}")

    if expected_hash and digest != expected_hash:
        print(
            "        [WARN] SHA-256 differs from manifest"
        )

        return None

    print("        [OK] verified")

    return digest


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:

    DATASET_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = load_manifest()

    print("=" * 64)
    print("CISI Dataset Downloader")
    print("=" * 64)

    hashes = {}

    for filename, config in FILES.items():

        expected_hash = manifest.get(filename)

        existing_hash = verify_existing_file(
            filename,
            expected_hash,
        )

        if existing_hash:
            hashes[filename] = existing_hash
            continue

        try:
            _, digest = download_file(
                filename=filename,
                url=config["url"],
                minimum_size=config["min_size"],
            )

        except Exception as exc:
            print(f"\n[ERROR] {exc}", file=sys.stderr)
            return 1

        # If a previous manifest existed and the newly downloaded file
        # does not match it, reject it.
        if expected_hash and digest != expected_hash:
            print(
                f"\n[ERROR] SHA-256 mismatch for {filename}",
                file=sys.stderr,
            )
            print(
                f"        Expected: {expected_hash}",
                file=sys.stderr,
            )
            print(
                f"        Actual:   {digest}",
                file=sys.stderr,
            )

            (DATASET_DIR / filename).unlink(
                missing_ok=True
            )

            return 1

        hashes[filename] = digest

    write_manifest(hashes)

    print("\n" + "=" * 64)
    print("CISI dataset ready.")
    print("=" * 64)

    for filename, digest in sorted(hashes.items()):
        path = DATASET_DIR / filename

        print(
            f"{filename:10} "
            f"{path.stat().st_size:>10,} bytes  "
            f"{digest}"
        )

    print(f"\nManifest: {DATASET_DIR / 'SHA256SUMS'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
