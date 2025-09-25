#!/usr/bin/env python
"""Create a Person node in Neo4j using the project's models.

Run from the project root (the directory that contains the `app` package):

  python tools\create_user.py --name Alice --age 30

This script imports `app.config` to ensure neomodel is configured from `app/.env`.
"""
import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Person node in Neo4j")
    parser.add_argument("--name", required=True, help="Person name (unique)")
    parser.add_argument("--age", type=int, required=True, help="Person age")
    args = parser.parse_args(argv)

    # Import project config to ensure neomodel is configured
    try:
        import app.config  # noqa: F401  (runs config to set DATABASE_URL)
    except Exception as e:
        print("Failed to load app config (check app/.env). Error:", e)
        return 2

    try:
        from app.models.person import Person
    except Exception as e:
        print("Failed to import Person model:", e)
        return 3

    try:
        existing = Person.nodes.get_or_none(name=args.name)
        if existing:
            print(f"Person '{args.name}' already exists (id={existing.element_id}).")
            return 0

        person = Person(name=args.name, age=args.age).save()
        print(f"Created Person '{args.name}' (id={person.element_id}).")
        return 0
    except Exception as e:
        print("Failed to create Person:", e)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
