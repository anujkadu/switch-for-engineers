"""Backend application entry point."""
from __future__ import annotations
import argparse

def main() -> None:
    parser = argparse.ArgumentParser(description="Engineering Flight Simulator backend")
    parser.add_argument("--check", action="store_true", help="Check package import without starting server")
    args = parser.parse_args()
    if args.check:
        print("EFS backend package import OK; server implementation is pending.")
        return
    raise SystemExit("Backend scaffold only: MCP server is not implemented. See backend/README.md.")

if __name__ == "__main__":
    main()
