import copy
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import capability_templates as ct


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.github = ct.parse(ct.ROOT / 'templates/opencode/github-readonly.jsonc')
        self.browser = ct.parse(ct.ROOT / 'templates/opencode/playwright-isolated.jsonc')

    def test_repository_fragments(self):
        self.assertEqual(ct.check()['status'], 'PASS')

    def test_no_automatic_activation(self):
        self.github['mcp']['github']['enabled'] = True
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.github)

    def test_no_token_literal(self):
        self.github['mcp']['github']['headers']['Authorization'] = 'Bearer example-not-a-token'
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.github)

    def test_readonly_required(self):
        self.github['mcp']['github']['headers']['X-MCP-Readonly'] = 'false'
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.github)

    def test_no_provider_overwrite(self):
        self.github['provider'] = {}
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.github)

    def test_no_foreign_host_keys(self):
        self.github['mcpServers'] = self.github.pop('mcp')
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.github)

    def test_no_personal_browser(self):
        for flag in ['--extension', '--cdp-endpoint', '--no-sandbox', '--storage-state']:
            data = copy.deepcopy(self.browser)
            data['mcp']['playwright']['command'].append(flag)
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                ct.validate_fragment(data)

    def test_isolation_required(self):
        self.browser['mcp']['playwright']['command'].remove('--isolated')
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.browser)

    def test_pinned_package(self):
        self.browser['mcp']['playwright']['command'][2] = '@playwright/mcp@latest'
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.browser)

    def test_permission_gate(self):
        self.browser['permission']['playwright_*'] = 'allow'
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.browser)

    def test_server_id_alignment(self):
        self.github['mcp']['github-mcp'] = self.github['mcp'].pop('github')
        with self.assertRaises(ValueError):
            ct.validate_fragment(self.github)


if __name__ == '__main__':
    unittest.main()
