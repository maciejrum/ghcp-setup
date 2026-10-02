"""Frozen, black-box checks. Run outside the measured A/B workspaces."""

import argparse
import json
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"
EXPECTED_IDS = {
    "alpha": {
        "open": ["alpha-016", "alpha-013", "alpha-010", "alpha-007", "alpha-004", "alpha-001"],
        "in_progress": ["alpha-017", "alpha-014", "alpha-011", "alpha-008", "alpha-005", "alpha-002"],
        "closed": ["alpha-018", "alpha-015", "alpha-012", "alpha-009", "alpha-006", "alpha-003"],
    },
    "beta": {
        "open": ["beta-007", "beta-004", "beta-001"],
        "in_progress": ["beta-008", "beta-005", "beta-002"],
        "closed": ["beta-009", "beta-006", "beta-003"],
    },
}


class IncidentAcceptance(unittest.TestCase):
    """Expected answers are fixed here, not read from the submitted application."""

    def request(self, query=None, tenant="alpha"):
        headers = {} if tenant is None else {"X-Tenant-ID": tenant}
        request = Request(BASE_URL.rstrip("/") + "/api/incidents?" + urlencode(query or {}),
                          headers=headers)
        try:
            with urlopen(request, timeout=10) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def assert_page(self, payload, ids, total, page=1, page_size=5):
        self.assertEqual(set(payload), {"items", "total", "page", "page_size"})
        self.assertEqual([item["id"] for item in payload["items"]], ids)
        self.assertEqual((payload["total"], payload["page"], payload["page_size"]),
                         (total, page, page_size))
        for item in payload["items"]:
            self.assertEqual(set(item), {"id", "title", "status", "severity", "created_at"})
            self.assertIn(item["status"], {"open", "in_progress", "closed"})
            self.assertIsInstance(item["title"], str)
            self.assertIsInstance(item["created_at"], str)

    def test_omitted_status_preserves_response_and_default_pagination(self):
        code, payload = self.request()
        self.assertEqual(code, 200)
        self.assert_page(payload, [f"alpha-{n:03}" for n in range(18, 13, -1)], 18)
        code, payload = self.request({"page": 2, "page_size": 3}, tenant="beta")
        self.assertEqual(code, 200)
        self.assert_page(payload, ["beta-006", "beta-005", "beta-004"], 9, 2, 3)

    def test_each_valid_status_filters_alpha(self):
        for status, ids in EXPECTED_IDS["alpha"].items():
            with self.subTest(status=status):
                code, payload = self.request({"status": status})
                self.assertEqual(code, 200)
                self.assert_page(payload, ids[:5], 6)
                self.assertTrue(all(item["status"] == status for item in payload["items"]))

    def test_filter_runs_before_pagination_and_total_counts_filtered_rows(self):
        for status, ids in EXPECTED_IDS["alpha"].items():
            with self.subTest(status=status):
                code, payload = self.request({"status": status, "page": 2, "page_size": 2})
                self.assertEqual(code, 200)
                self.assert_page(payload, ids[2:4], 6, 2, 2)

    def test_filter_preserves_beta_tenant_isolation(self):
        for status, ids in EXPECTED_IDS["beta"].items():
            with self.subTest(status=status):
                code, payload = self.request({"status": status, "page_size": 50}, tenant="beta")
                self.assertEqual(code, 200)
                self.assert_page(payload, ids, 3, 1, 50)
                self.assertTrue(all(item["status"] == status for item in payload["items"]))

    def test_invalid_status_returns_422(self):
        for value in ("unknown", "OPEN", "", "closed,open"):
            with self.subTest(status=value):
                code, payload = self.request({"status": value})
                self.assertEqual(code, 422)
                self.assertIn("detail", payload)

    def test_filtered_page_beyond_end_preserves_filtered_total(self):
        code, payload = self.request({"status": "open", "page": 20})
        self.assertEqual(code, 200)
        self.assert_page(payload, [], 6, 20)

    def test_tenant_guards_are_preserved(self):
        for tenant, expected_code in ((None, 401), ("unknown", 401)):
            with self.subTest(tenant=tenant):
                code, payload = self.request({"status": "open"}, tenant=tenant)
                self.assertEqual(code, expected_code)
                self.assertIn("detail", payload)
                self.assertNotIn("items", payload)

    def test_existing_pagination_validation_is_preserved(self):
        for query in ({"page": 0}, {"page_size": 0}, {"page_size": 51}):
            with self.subTest(query=query):
                code, _ = self.request({"status": "open", **query})
                self.assertEqual(code, 422)


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test.id())


def main():
    global BASE_URL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()
    BASE_URL = args.base_url
    try:
        request = Request(BASE_URL.rstrip("/") + "/api/incidents", headers={"X-Tenant-ID": "alpha"})
        with urlopen(request, timeout=5):
            pass
    except HTTPError:
        # An HTTP error still means the service is reachable; assess its behavior below.
        pass
    except (URLError, TimeoutError, OSError) as error:
        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            args.json_output.write_text(json.dumps({
                "base_url": BASE_URL, "tests_run": 0, "status": "BLOCKED",
                "environment_error": str(error),
            }, indent=2) + "\n", encoding="utf-8")
        parser.exit(2, f"Cannot reach benchmark API: {error}\nNo acceptance checks were run.\n")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IncidentAcceptance)
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(suite)
    if args.json_output:
        report = {
            "base_url": BASE_URL, "tests_run": result.testsRun,
            "passed": result.wasSuccessful(), "successful_checks": result.successes,
            "failures": [{"check": check.id(), "detail": detail} for check, detail in result.failures],
            "errors": [{"check": check.id(), "detail": detail} for check, detail in result.errors],
        }
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
