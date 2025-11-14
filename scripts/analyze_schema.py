#!/usr/bin/env python3
"""Analyze the Care API schema and show available operations."""

import json
import sys
from pathlib import Path
from collections import defaultdict


def analyze_schema(schema_path: str):
    """Analyze the Care API schema."""
    with open(schema_path, "r") as f:
        schema = json.load(f)

    print("=" * 80)
    print("CARE API SCHEMA ANALYSIS")
    print("=" * 80)
    print()

    # Basic info
    print(f"OpenAPI Version: {schema.get('openapi')}")
    print(f"API Title: {schema['info']['title']}")
    print(f"API Version: {schema['info']['version']}")
    print()

    # Count operations
    operations = []
    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            if isinstance(details, dict) and "operationId" in details:
                operations.append((details["operationId"], path, method, details.get("tags", [])))

    print(f"Total API Paths: {len(schema.get('paths', {}))}")
    print(f"Total Operations: {len(operations)}")
    print()

    # Group by entity type
    entity_counts = defaultdict(list)
    for op in operations:
        parts = op[0].split("_")
        if len(parts) >= 3:
            entity = parts[2]
            entity_counts[entity].append(op)

    print("=" * 80)
    print("TOP ENTITY TYPES")
    print("=" * 80)
    sorted_entities = sorted(entity_counts.items(), key=lambda x: len(x[1]), reverse=True)

    for i, (entity, ops) in enumerate(sorted_entities[:15], 1):
        print(f"{i:2}. {entity:20} {len(ops):4} operations")

    print()

    # Check whitelisted operations from our implementation
    print("=" * 80)
    print("WHITELISTED OPERATIONS IN SCHEMA")
    print("=" * 80)

    # Import whitelist from our implementation
    sys.path.insert(0, str(Path(schema_path).parent))
    try:
        from src.care_mcp_server.whitelist import WhitelistManager

        manager = WhitelistManager()
        whitelist = manager.get_allowed_operations()

        real_op_ids = {op[0] for op in operations}

        found = []
        missing = []

        for op_id in sorted(whitelist):
            if op_id in real_op_ids:
                found.append(op_id)
            else:
                missing.append(op_id)

        print(f"\n✅ Found in schema: {len(found)}/{len(whitelist)}")
        for op in found:
            # Find the operation details
            op_details = [o for o in operations if o[0] == op][0]
            print(f"   • {op}")
            print(f"     {op_details[2].upper()} {op_details[1]}")

        if missing:
            print(f"\n❌ Missing from schema: {len(missing)}")
            for op in missing:
                print(f"   • {op}")

    except ImportError as e:
        print(f"Could not import whitelist: {e}")

    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    schema_file = Path(__file__).parent.parent / "care_api_swagger_schema.json"

    if not schema_file.exists():
        print(f"Error: Schema file not found at {schema_file}")
        sys.exit(1)

    analyze_schema(str(schema_file))
