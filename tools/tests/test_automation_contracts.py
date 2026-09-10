"""Deterministic regression tests, not full host/Bot/security certification."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import capability_templates as ct
import smoke_security as smoke
from quality import ROOT


class AutomationTests(unittest.TestCase):
    def test_short_command_rejected(self):
        for command in ([], ['npx'], ['npx', '-y']):
            data = ct.parse(ROOT / 'templates/opencode/playwright-isolated.jsonc')
            data['mcp']['playwright']['command'] = command
            with self.subTest(command=command), self.assertRaises(ValueError):
                ct.validate_fragment(data)

    def test_missing_checker_not_pass(self):
        output = io.StringIO()
        with patch('smoke_security.shutil.which', return_value=None), contextlib.redirect_stdout(output):
            self.assertEqual(smoke.main(), 2)
        self.assertEqual(json.loads(output.getvalue())['status'], 'BLOCKED')

    def test_wrong_exit_rejected_without_echoing_output(self):
        with patch('smoke_security.subprocess.run') as process:
            process.return_value.returncode = 3
            process.return_value.stdout = 'private fixture content'
            with self.assertRaisesRegex(RuntimeError, 'expected exit 0, got 3') as caught:
                smoke.run(['checker'], ROOT)
            self.assertNotIn('private', str(caught.exception))

    def test_expected_failure_is_a_valid_negative_test(self):
        with patch('smoke_security.subprocess.run') as process:
            process.return_value.returncode = 1
            self.assertIs(smoke.run(['checker'], ROOT, 1), process.return_value)

    def test_renovate_no_automerge_or_universal_managers(self):
        config = json.loads((ROOT / 'templates/project/renovate.json').read_text())
        self.assertFalse(config['automerge'])
        self.assertEqual(config['enabledManagers'], ['github-actions'])

    def test_staged_hook_not_worktree(self):
        content = (ROOT / 'templates/project/lefthook.yml').read_text()
        self.assertIn('gitleaks git --staged --redact', content)
        self.assertNotIn('git add', content)

    def test_no_dangerous_workflow_trigger_or_error_suppression(self):
        for path in (ROOT / 'templates/github').glob('*.yml'):
            with self.subTest(path=path.name):
                content = path.read_text()
                self.assertNotIn('pull_request_target:', content)
                self.assertNotIn('continue-on-error: true', content)
                self.assertNotIn('|| true', content)
                self.assertNotIn('@latest', content)
                self.assertIn('contents: read', content)

    def test_security_nonzero_exit_and_target_gate(self):
        g = (ROOT / 'templates/github/gitleaks.yml').read_text()
        t = (ROOT / 'templates/github/trivy-config.yml').read_text()
        self.assertIn('--redact', g)
        self.assertIn('--exit-code 1', g)
        self.assertIn('--exit-code 1', t)
        self.assertIn('No configuration target scanned', t)

    def test_new_setup_paths_are_reachable(self):
        for name in ['PROJECT_BOOTSTRAP', 'PROJECT_REFRESH']:
            self.assertIn('PROJECT_TOOLING_SETUP.md', (ROOT / f'prompts/{name}.md').read_text())
        self.assertIn('templates/opencode/README.md', (ROOT / 'prompts/OPENCODE_PLUGIN_SETUP.md').read_text())

    def test_gitleaks_maintenance_not_claimed_feature_active(self):
        catalog = json.loads((ROOT / 'catalog/automation-tools.json').read_text())
        g = next(t for t in catalog['tools'] if t['id'] == 'gitleaks')
        self.assertIn('security-patch-only', g['purpose'])


if __name__ == '__main__':
    unittest.main()
