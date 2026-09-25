#!/usr/bin/env python3
"""Offline acceptance checks for the R0.3 transport-neutral contracts."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import unicodedata
import unittest
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "contracts"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "r0_3"


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def normalize_phrase(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = "".join(" " if unicodedata.category(char).startswith("P") else char for char in value)
    return " ".join(value.split())


class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_paths = sorted(SCHEMA_ROOT.rglob("*.schema.json"))
        cls.schemas = [load_json(path) for path in cls.schema_paths]
        cls.registry = Registry().with_resources(
            (schema["$id"], Resource.from_contents(schema)) for schema in cls.schemas
        )

    def validator(self, schema_file: str) -> Draft202012Validator:
        matches = [
            schema
            for path, schema in zip(self.schema_paths, self.schemas)
            if path.name == schema_file
        ]
        self.assertEqual(len(matches), 1, f"expected one schema named {schema_file}")
        schema = matches[0]
        return Draft202012Validator(
            schema,
            registry=self.registry,
            format_checker=FormatChecker(),
        )

    def assert_valid(self, schema_file: str, instance) -> None:
        errors = sorted(
            self.validator(schema_file).iter_errors(instance), key=lambda error: list(error.path)
        )
        detail = "\n".join(f"{list(error.path)}: {error.message}" for error in errors)
        self.assertFalse(errors, detail)

    def assert_invalid(self, schema_file: str, instance) -> None:
        self.assertTrue(list(self.validator(schema_file).iter_errors(instance)))

    def test_all_schemas_are_draft_2020_12_and_have_unique_ids(self):
        self.assertEqual(len(self.schemas), 16)
        ids = []
        for schema in self.schemas:
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            Draft202012Validator.check_schema(schema)
            ids.append(schema["$id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_expected_outputs_validate(self):
        one_to_one = {
            "expected-url-batch.json": "url-batch.schema.json",
            "expected-keyword-table-ru.json": "keyword-table.schema.json",
            "expected-keyword-table-uk.json": "keyword-table.schema.json",
            "expected-serp-snapshot.json": "serp-snapshot.schema.json",
            "expected-page-observation.json": "page-observation.schema.json",
            "expected-artifact-envelope.json": "artifact-envelope.schema.json",
            "expected-cost-estimate.json": "cost-estimate.schema.json",
            "expected-run-plan.json": "run-plan.schema.json",
            "expected-stage-result.json": "stage-result.schema.json",
            "expected-notification-event.json": "notification-event.schema.json",
            "expected-notification-delivery.json": "notification-delivery.schema.json",
            "expected-telegram-command.json": "telegram-command.schema.json",
            "expected-telegram-confirmation.json": "telegram-confirmation.schema.json",
            "expected-telegram-outcome.json": "telegram-outcome.schema.json",
        }
        for fixture, schema in one_to_one.items():
            with self.subTest(fixture=fixture):
                self.assert_valid(schema, load_json(FIXTURE_ROOT / fixture))

        for record in load_json(FIXTURE_ROOT / "identity-records.json"):
            self.assert_valid("identity-record.schema.json", record)
        for record in load_json(FIXTURE_ROOT / "expected-normalized-keywords.json"):
            self.assert_valid("normalized-keyword.schema.json", record)

    def test_manual_url_input_matches_normalized_batch(self):
        lines = [
            line
            for line in (FIXTURE_ROOT / "url-list.txt").read_text(encoding="utf-8").splitlines()
            if line
        ]
        batch = load_json(FIXTURE_ROOT / "expected-url-batch.json")
        self.assertEqual(lines, [row["url"] for row in batch["rows"]])
        self.assertEqual(
            batch["source"]["original_hash"], sha256_file(FIXTURE_ROOT / "url-list.txt")
        )
        for value in lines:
            self.assertTrue(urlparse(value).hostname.endswith(".example.test"))

    def test_keyword_csvs_are_separate_and_deterministic(self):
        expected_tables = {}
        for language in ("ru", "uk"):
            csv_path = FIXTURE_ROOT / f"keywords-{language}.csv"
            with csv_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, ["phrase", "locale_tag", "target_url"])
                rows = list(reader)
            expected = load_json(FIXTURE_ROOT / f"expected-keyword-table-{language}.json")
            expected_tables[language] = expected
            self.assertEqual(expected["file"]["original_hash"], sha256_file(csv_path))
            self.assertEqual(expected["source"]["original_hash"], sha256_file(csv_path))
            self.assertEqual(
                rows,
                [
                    {key: row[key] for key in ("phrase", "locale_tag", "target_url")}
                    for row in expected["rows"]
                ],
            )
            self.assertTrue(
                all(not row["phrase"].lstrip().startswith(("=", "+", "-", "@")) for row in rows)
            )
            self.assertTrue(
                all(urlparse(row["target_url"]).hostname.endswith(".example.test") for row in rows)
            )

        self.assertEqual({row["locale_tag"] for row in expected_tables["ru"]["rows"]}, {"ru-UA"})
        self.assertEqual({row["locale_tag"] for row in expected_tables["uk"]["rows"]}, {"uk-UA"})

        normalized = load_json(FIXTURE_ROOT / "expected-normalized-keywords.json")
        by_source = {(row["source_batch_id"], row["source_row_number"]): row for row in normalized}
        for table in expected_tables.values():
            for row in table["rows"]:
                result = by_source[(table["batch_id"], row["row_number"])]
                self.assertEqual(result["original_phrase"], row["phrase"])
                self.assertEqual(result["normalized_phrase"], normalize_phrase(row["phrase"]))
                self.assertEqual(result["locale_tag"], row["locale_tag"])
                self.assertIsNone(result["metrics"])

    def test_offline_serp_adapter_is_explainable(self):
        raw_path = FIXTURE_ROOT / "offline-serp-response.json"
        raw = load_json(raw_path)
        normalized = load_json(FIXTURE_ROOT / "expected-serp-snapshot.json")
        self.assertEqual(normalized["provider_payload_hash"], sha256_file(raw_path))
        self.assertEqual(normalized["source"]["original_hash"], sha256_file(raw_path))
        self.assertEqual(normalized["query"], raw["request"]["query"])
        self.assertEqual(normalized["device"], raw["request"]["device"])
        for source, result in zip(raw["results"], normalized["results"]):
            self.assertEqual(
                (result["rank"], result["url"], result["title"], result["snippet"]),
                (source["position"], source["link"], source["title"], source["snippet"]),
            )

    def test_artifact_hash_and_retention_boundary(self):
        artifact = load_json(FIXTURE_ROOT / "expected-artifact-envelope.json")
        self.assertEqual(artifact["content_hash"], canonical_hash(artifact["payload"]))
        invalid = copy.deepcopy(artifact)
        invalid["retention"] = {
            "retention_class": "historical",
            "contains_raw_payload": True,
            "max_age_days": 30,
            "expires_at": None,
        }
        self.assert_invalid("artifact-envelope.schema.json", invalid)

    def test_identity_and_market_invariants(self):
        records = load_json(FIXTURE_ROOT / "identity-records.json")
        locales = [record["data"] for record in records if record["entity_type"] == "locale"]
        markets = [record["data"] for record in records if record["entity_type"] == "market"]
        targets = [
            record["data"] for record in records if record["entity_type"] == "content_target"
        ]
        self.assertEqual({locale["bcp47_tag"] for locale in locales}, {"ru-UA", "uk-UA"})
        self.assertEqual({market["device"] for market in markets}, {"desktop", "mobile"})
        self.assertEqual(len(markets), 4)
        self.assertEqual(len(targets), 2)
        self.assertEqual(
            {target["locale_id"] for target in targets}, {locale["locale_id"] for locale in locales}
        )

        existing = next(
            record
            for record in records
            if record["entity_type"] == "content_target"
            and record["data"]["target_kind"] == "existing"
        )
        invalid = copy.deepcopy(existing)
        invalid["data"]["canonical_url"] = None
        self.assert_invalid("identity-record.schema.json", invalid)

    def test_plan_is_bounded_and_cost_fail_closed(self):
        plan = load_json(FIXTURE_ROOT / "expected-run-plan.json")
        self.assertFalse(plan["resolve_missing_upstream"])
        self.assertEqual([stage["sequence"] for stage in plan["stages"]], [1, 2, 3])
        skipped = next(stage for stage in plan["stages"] if stage["action"] == "skip")
        self.assertEqual(skipped["skip"]["reason_code"], "owner_supplied")
        self.assertEqual(skipped["side_effects"], [])
        self.assertEqual(skipped["external_calls"], [])

        invalid_plan = copy.deepcopy(plan)
        invalid_plan["resolve_missing_upstream"] = True
        self.assert_invalid("run-plan.schema.json", invalid_plan)

        invalid_cost = load_json(FIXTURE_ROOT / "expected-cost-estimate.json")
        invalid_cost["cost_class"] = "unknown"
        invalid_cost["enqueue_allowed"] = True
        invalid_cost["blocked_reasons"] = ["unknown_price"]
        self.assert_invalid("cost-estimate.schema.json", invalid_cost)

    def test_telegram_contract_does_not_store_raw_message(self):
        command = load_json(FIXTURE_ROOT / "expected-telegram-command.json")
        invalid = copy.deepcopy(command)
        invalid["contains_raw_message"] = True
        self.assert_invalid("telegram-command.schema.json", invalid)

    def test_validation_report_counts_match_issues(self):
        fixtures = list(FIXTURE_ROOT.glob("expected-*.json"))
        for path in fixtures:
            value = load_json(path)
            values = value if isinstance(value, list) else [value]
            for item in values:
                report = item.get("validation") if isinstance(item, dict) else None
                if not report:
                    continue
                errors = sum(issue["severity"] == "error" for issue in report["issues"])
                warnings = sum(issue["severity"] == "warning" for issue in report["issues"])
                self.assertEqual(report["error_count"], errors, path.name)
                self.assertEqual(report["warning_count"], warnings, path.name)

    def test_fixture_checksum_manifest(self):
        manifest = load_json(FIXTURE_ROOT / "manifest.json")
        declared = manifest["files"]
        actual_names = {
            path.name
            for path in FIXTURE_ROOT.iterdir()
            if path.is_file() and path.name not in {"README.md", "manifest.json"}
        }
        self.assertEqual(set(declared), actual_names)
        for name, expected_hash in declared.items():
            self.assertEqual(expected_hash, sha256_file(FIXTURE_ROOT / name), name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
