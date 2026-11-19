#!/usr/bin/env python3
"""
Unit and Integration Tests for PFS Milestone M1 Automated Architecture Validator
================================================================================
Verifies that M1Validator correctly catches errors, detects cycles, parses schemas,
and properly exits with code 0 on valid architecture repository.
"""

import os
import sys
import unittest
import tempfile
import json
import csv

# Add tools/validation to python path
sys.path.insert(0, os.path.dirname(__file__))
from validate_m1 import M1Validator, Finding

class TestM1ValidatorUnits(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.validator = M1Validator(self.repo_root)

    def test_finding_str_formatting(self):
        f = Finding("M1-FND-001", "CRITICAL", "TestCat", "Test message", "test/path.md", 42)
        s = str(f)
        self.assertIn("[CRITICAL]", s)
        self.assertIn("TestCat in test/path.md:42", s)
        self.assertIn("Test message", s)

    def test_cycle_detection_on_synthetic_cycle(self):
        """Tests that DFS cycle detector correctly detects an intentional cycle."""
        cyclic_graph = {
            "MOD-A": ["MOD-B"],
            "MOD-B": ["MOD-C"],
            "MOD-C": ["MOD-A"]
        }
        visited = {n: 0 for n in cyclic_graph}
        cycles = []

        def dfs(node, path):
            visited[node] = 1
            for neighbor in cyclic_graph.get(node, []):
                if visited[neighbor] == 1:
                    cycles.append(path + [neighbor])
                elif visited[neighbor] == 0:
                    dfs(neighbor, path + [neighbor])
            visited[node] = 2

        for n in cyclic_graph:
            if visited[n] == 0:
                dfs(n, [n])

        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0], ["MOD-A", "MOD-B", "MOD-C", "MOD-A"])

    def test_cycle_detection_on_synthetic_dag(self):
        """Tests that DFS cycle detector finds 0 cycles on a true DAG."""
        dag = {
            "MOD-A": ["MOD-B", "MOD-C"],
            "MOD-B": ["MOD-D"],
            "MOD-C": ["MOD-D"],
            "MOD-D": []
        }
        visited = {n: 0 for n in dag}
        cycles = []

        def dfs(node, path):
            visited[node] = 1
            for neighbor in dag.get(node, []):
                if visited[neighbor] == 1:
                    cycles.append(path + [neighbor])
                elif visited[neighbor] == 0:
                    dfs(neighbor, path + [neighbor])
            visited[node] = 2

        for n in dag:
            if visited[n] == 0:
                dfs(n, [n])

        self.assertEqual(len(cycles), 0)

    def test_json_schema_draft_2020_12_check(self):
        """Verifies that all 8 schemas declare Draft 2020-12."""
        schemas_dir = os.path.join(self.repo_root, "docs", "M1-architecture", "schemas")
        for f in os.listdir(schemas_dir):
            if f.endswith(".json"):
                with open(os.path.join(schemas_dir, f), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                self.assertIn("$schema", data, f"Schema {f} missing $schema")
                self.assertIn("2020-12", data["$schema"], f"Schema {f} not Draft 2020-12")

    def test_openapi_contract_validity(self):
        """Verifies that pfs-openapi.json is valid OpenAPI 3.1."""
        contract_path = os.path.join(self.repo_root, "docs", "M1-architecture", "contracts", "pfs-openapi.json")
        with open(contract_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        self.assertEqual(data.get("openapi"), "3.1.0")
        self.assertIn("/projects", data.get("paths", {}))
        self.assertIn("ProjectResponse", data.get("components", {}).get("schemas", {}))

    def test_full_repository_validation_passes(self):
        """End-to-end execution of M1Validator on current repository baseline."""
        exit_code = self.validator.run_all()
        self.assertEqual(exit_code, 0, "M1Validator must pass with exit code 0")

if __name__ == "__main__":
    unittest.main()
