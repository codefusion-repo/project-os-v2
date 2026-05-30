"""Small Draft 2020-12 validator subset used by R1.10.

The repository schemas use a constrained keyword set. This module implements
that set locally so the validator command remains runnable with Python stdlib
only in clean checkouts.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class SchemaIssue:
    code: str
    pointer: str
    expected: Any
    actual: Any
    hint: str


def escape_pointer_token(token: object) -> str:
    return str(token).replace("~", "~0").replace("/", "~1")


def join_pointer(base: str, token: object) -> str:
    if base in ("", "/"):
        return "/" + escape_pointer_token(token)
    return base + "/" + escape_pointer_token(token)


class SchemaRegistry:
    def __init__(self) -> None:
        self._schemas: dict[str, Any] = {}

    @property
    def ids(self) -> set[str]:
        return set(self._schemas)

    def add(self, schema_id: str, schema: Any) -> None:
        self._schemas[schema_id] = schema

    def has(self, schema_id: str) -> bool:
        return schema_id in self._schemas

    def resolve(self, ref: str) -> Any:
        schema_id, _, fragment = ref.partition("#")
        if not schema_id:
            raise KeyError(ref)
        if schema_id not in self._schemas:
            raise KeyError(ref)
        target = self._schemas[schema_id]
        if not fragment:
            return target
        if not fragment.startswith("/"):
            raise KeyError(ref)
        for raw_token in fragment.lstrip("/").split("/"):
            token = raw_token.replace("~1", "/").replace("~0", "~")
            if isinstance(target, dict) and token in target:
                target = target[token]
            else:
                raise KeyError(ref)
        return target


class Draft202012SubsetValidator:
    def __init__(self, registry: SchemaRegistry) -> None:
        self.registry = registry

    def validate(self, instance: Any, schema: Any, pointer: str = "") -> list[SchemaIssue]:
        return self._validate(instance, schema, pointer or "/")

    def _validate(self, instance: Any, schema: Any, pointer: str) -> list[SchemaIssue]:
        if schema is True:
            return []
        if schema is False:
            return [
                SchemaIssue(
                    "JSON_SCHEMA_FALSE_SCHEMA",
                    pointer,
                    "schema allows no values",
                    instance,
                    "Update the instance or schema so the value is permitted.",
                )
            ]
        if not isinstance(schema, dict):
            return [
                SchemaIssue(
                    "JSON_SCHEMA_INVALID_SCHEMA",
                    pointer,
                    "schema object or boolean",
                    type(schema).__name__,
                    "Use a valid JSON Schema object or boolean schema.",
                )
            ]

        issues: list[SchemaIssue] = []

        if "$ref" in schema:
            ref = schema["$ref"]
            try:
                ref_schema = self.registry.resolve(ref)
            except KeyError:
                return [
                    SchemaIssue(
                        "JSON_SCHEMA_REF_UNRESOLVED",
                        pointer,
                        "resolvable $ref",
                        ref,
                        "Reference an existing schema $id and fragment.",
                    )
                ]
            issues.extend(self._validate(instance, ref_schema, pointer))

        for subschema in schema.get("allOf", []):
            issues.extend(self._validate(instance, subschema, pointer))

        if "anyOf" in schema:
            matches = [self._validate(instance, item, pointer) for item in schema["anyOf"]]
            if not any(not match for match in matches):
                issues.append(
                    SchemaIssue(
                        "JSON_SCHEMA_ANY_OF",
                        pointer,
                        "value matching at least one allowed schema",
                        instance,
                        "Change the value so it satisfies one of the allowed shapes.",
                    )
                )

        if "oneOf" in schema:
            matches = [self._validate(instance, item, pointer) for item in schema["oneOf"]]
            match_count = sum(1 for match in matches if not match)
            if match_count != 1:
                issues.append(
                    SchemaIssue(
                        "JSON_SCHEMA_ONE_OF",
                        pointer,
                        "value matching exactly one allowed schema",
                        instance,
                        "Change the value so it satisfies one and only one allowed shape.",
                    )
                )

        if "const" in schema and instance != schema["const"]:
            issues.append(
                SchemaIssue(
                    "JSON_SCHEMA_CONST",
                    pointer,
                    schema["const"],
                    instance,
                    "Use the required constant value.",
                )
            )

        if "enum" in schema and instance not in schema["enum"]:
            issues.append(
                SchemaIssue(
                    "JSON_SCHEMA_ENUM",
                    pointer,
                    schema["enum"],
                    instance,
                    "Use one of the allowed enum values.",
                )
            )

        if "type" in schema and not _matches_type(instance, schema["type"]):
            issues.append(
                SchemaIssue(
                    "JSON_SCHEMA_TYPE",
                    pointer,
                    schema["type"],
                    _json_type_name(instance),
                    "Use a value with the expected JSON type.",
                )
            )
            return issues

        if "pattern" in schema and isinstance(instance, str):
            if re.fullmatch(schema["pattern"], instance) is None:
                issues.append(
                    SchemaIssue(
                        "JSON_SCHEMA_PATTERN",
                        pointer,
                        schema["pattern"],
                        instance,
                        "Use a value matching the required pattern.",
                    )
                )

        if "minLength" in schema and isinstance(instance, str):
            if len(instance) < schema["minLength"]:
                issues.append(
                    SchemaIssue(
                        "JSON_SCHEMA_MIN_LENGTH",
                        pointer,
                        f">= {schema['minLength']}",
                        len(instance),
                        "Use a non-empty value with enough characters.",
                    )
                )

        if "minimum" in schema and _is_number(instance):
            if instance < schema["minimum"]:
                issues.append(
                    SchemaIssue(
                        "JSON_SCHEMA_MINIMUM",
                        pointer,
                        f">= {schema['minimum']}",
                        instance,
                        "Use a numeric value inside the permitted range.",
                    )
                )

        if "minProperties" in schema and isinstance(instance, dict):
            if len(instance) < schema["minProperties"]:
                issues.append(
                    SchemaIssue(
                        "JSON_SCHEMA_MIN_PROPERTIES",
                        pointer,
                        f">= {schema['minProperties']}",
                        len(instance),
                        "Add the required object properties.",
                    )
                )

        if isinstance(instance, dict):
            required = schema.get("required", [])
            for key in required:
                if key not in instance:
                    issues.append(
                        SchemaIssue(
                            "JSON_SCHEMA_REQUIRED",
                            join_pointer(pointer, key),
                            "present required field",
                            "missing",
                            "Add the required field at the reported JSON pointer.",
                        )
                    )

            properties = schema.get("properties", {})
            for key, value in instance.items():
                if key in properties:
                    issues.extend(self._validate(value, properties[key], join_pointer(pointer, key)))
                elif schema.get("additionalProperties") is False:
                    issues.append(
                        SchemaIssue(
                            "JSON_SCHEMA_ADDITIONAL_PROPERTY",
                            join_pointer(pointer, key),
                            "no additional properties",
                            key,
                            "Remove the unsupported field or update the schema in a scoped schema issue.",
                        )
                    )
                elif isinstance(schema.get("additionalProperties"), dict):
                    issues.extend(
                        self._validate(
                            value,
                            schema["additionalProperties"],
                            join_pointer(pointer, key),
                        )
                    )

        if isinstance(instance, list):
            if "items" in schema:
                for index, value in enumerate(instance):
                    issues.extend(self._validate(value, schema["items"], join_pointer(pointer, index)))
            if schema.get("uniqueItems") is True:
                seen: set[str] = set()
                for index, value in enumerate(instance):
                    key = json.dumps(value, sort_keys=True, separators=(",", ":"))
                    if key in seen:
                        issues.append(
                            SchemaIssue(
                                "JSON_SCHEMA_UNIQUE_ITEMS",
                                join_pointer(pointer, index),
                                "unique array item",
                                value,
                                "Remove duplicate values from the array.",
                            )
                        )
                    seen.add(key)

        return issues


def iter_refs(value: Any, pointer: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = join_pointer(pointer or "/", key)
            if key == "$ref" and isinstance(child, str):
                yield child_pointer, child
            else:
                yield from iter_refs(child, child_pointer)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_refs(child, join_pointer(pointer or "/", index))


def _matches_type(instance: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_matches_type(instance, item) for item in expected)
    if expected == "null":
        return instance is None
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return _is_number(instance)
    return True


def _is_number(instance: Any) -> bool:
    return isinstance(instance, (int, float)) and not isinstance(instance, bool)


def _json_type_name(instance: Any) -> str:
    if instance is None:
        return "null"
    if isinstance(instance, bool):
        return "boolean"
    if isinstance(instance, dict):
        return "object"
    if isinstance(instance, list):
        return "array"
    if isinstance(instance, str):
        return "string"
    if isinstance(instance, int):
        return "integer"
    if isinstance(instance, float):
        return "number"
    return type(instance).__name__
