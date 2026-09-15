"""Static documentation contracts only; these are not host setup smoke tests."""
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]


class SetupContractTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding='utf-8')

    def test_entries_share_contract(self):
        for name in ('TOOLING_SETUP', 'OPENCODE_PLUGIN_SETUP', 'DEVELOPER_CLI_SETUP', 'PROJECT_TOOLING_SETUP'):
            with self.subTest(name=name):
                self.assertIn('CONTRACT.md', self.read(f'prompts/{name}.md'))

    def test_legacy_entry_retained(self):
        self.assertIn('catalog/tooling.json', self.read('prompts/OPENCODE_PLUGIN_SETUP.md'))
        self.assertIn('catalog/agent-capabilities.json', self.read('prompts/OPENCODE_PLUGIN_SETUP.md'))

    def test_missing_installation_supported(self):
        self.assertIn('Missing tools are a normal initial state', self.read('prompts/TOOLING_SETUP.md'))

    def test_global_apm_bootstrap_contract(self):
        merge = self.read('templates/setup/GLOBAL_REFERENCE_MERGE.md')
        tooling = self.read('prompts/TOOLING_SETUP.md')
        self.assertIn('prompts/APM_SETUP.md', merge)
        self.assertIn('commands/apm-setup.md', merge)
        self.assertIn('only agent-reference package command intended for user-global discovery', merge)
        self.assertIn('Do not install `/agent-sync` or `/test-setup` globally', merge)
        self.assertIn('default global active Skill count remains zero', merge)
        self.assertIn('global `/apm-setup` bootstrap', tooling)

    def test_global_bootstrap_is_documented_for_fresh_projects(self):
        index = self.read('prompts/README.md')
        self.assertIn('before a repository has adopted APM', index)
        self.assertIn('`/agent-sync` and `/test-setup` remain project-local', index)

    def test_no_blanket_config_replacement(self):
        self.assertIn('Never parse JSONC through jq/yq', self.read('templates/setup/CONTRACT.md'))

    def test_secret_boundary(self):
        self.assertIn('never commit or upload that copy', self.read('templates/setup/CONTRACT.md'))

    def test_host_claim_boundary(self):
        self.assertIn('reading a template is not proof of idempotence', self.read('templates/setup/CONTRACT.md'))

    def test_context7_duplicate_guard(self):
        self.assertIn('Reuse one healthy instance', self.read('prompts/OPENCODE_PLUGIN_SETUP.md'))

    def test_pilot_requires_selection(self):
        self.assertIn('explicit pilot only', self.read('prompts/OPENCODE_PLUGIN_SETUP.md'))

    def test_operational_rewrite_not_setup(self):
        self.assertIn('Recipe execution changes application source and is outside this prompt', self.read('prompts/PROJECT_TOOLING_SETUP.md'))

    def test_hook_ownership(self):
        self.assertIn('core.hooksPath', self.read('prompts/PROJECT_TOOLING_SETUP.md'))
        self.assertIn('partial staging', self.read('prompts/PROJECT_TOOLING_SETUP.md'))

    def test_cli_not_mcp(self):
        self.assertIn('not invented MCP entries', self.read('prompts/OPENCODE_PLUGIN_SETUP.md'))

    def test_rollback_no_shared_uninstall(self):
        self.assertIn('Do not uninstall a shared runtime', self.read('templates/setup/CONTRACT.md'))


if __name__ == '__main__':
    unittest.main()
