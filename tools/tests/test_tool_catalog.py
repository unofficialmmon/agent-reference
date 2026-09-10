import copy
import sys
import unittest
from datetime import date
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tool_catalog as tc

TODAY = date(2026, 9, 10)


class Reader:
    def __init__(self, archived=False, disabled=False, old=False, release=False):
        self.archived, self.disabled, self.old, self.release = archived, disabled, old, release

    def get(self, path):
        if path.endswith('/releases/latest'):
            if self.release:
                return {'draft': False, 'prerelease': False, 'tag_name': 'v1', 'published_at': '2026-09-09T00:00:00Z'}
            raise ValueError('GitHub API HTTP 404')
        if '/commits?' in path:
            return [{'sha': 'a' * 40, 'commit': {'committer': {'date': '2024-01-01T00:00:00Z' if self.old else '2026-09-09T00:00:00Z'}}}]
        return {'full_name': 'org/repo', 'archived': self.archived, 'disabled': self.disabled, 'default_branch': 'main'}


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = tc.load_json(tc.ROOT / 'catalog/agent-capabilities.json')

    def test_all_catalogs(self):
        tools = tc.load_tools(today=TODAY)
        self.assertEqual(len(tools), 40)
        self.assertEqual(tools['serena']['policy'], 'pilot')
        self.assertEqual(tools['openrewrite']['policy'], 'operational')
        self.assertEqual(tools['playwright-mcp']['activation'], 'explicit-opt-in')

    def reject(self, key, value):
        data = copy.deepcopy(self.data)
        data['tools'][0][key] = value
        with self.assertRaises(ValueError):
            tc.validate_tools(data, 'agent-capabilities', TODAY)

    def test_unsafe_upstream(self):
        for value in ('../repo', 'org/..', 'https://other/repo', 'org/repo?token=x'):
            with self.subTest(value=value):
                self.reject('upstream', value)

    def test_unknown_policy(self):
        self.reject('policy', 'always-install')

    def test_unsafe_activation(self):
        data = copy.deepcopy(self.data)
        data['tools'][0]['policy'] = 'operational'
        with self.assertRaises(ValueError):
            tc.validate_tools(data, 'agent-capabilities', TODAY)

    def test_duplicate(self):
        self.data['tools'].append(self.data['tools'][0])
        with self.assertRaises(ValueError):
            tc.validate_tools(self.data, 'agent-capabilities', TODAY)

    def test_bad_docs(self):
        self.reject('docs', 'https://secret:password@example.com')

    def test_future_review(self):
        self.data['policyReviewedAt'] = '2099-01-01'
        with self.assertRaises(ValueError):
            tc.validate_tools(self.data, 'agent-capabilities', TODAY)

    def test_scope(self):
        with self.assertRaises(ValueError):
            tc.validate_tools(self.data, 'developer-cli', TODAY)

    def test_offline(self):
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, None, TODAY, 180)['status'], 'NOT_CHECKED')

    def test_recent(self):
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Reader(), TODAY, 180)['status'], 'RECENT_ACTIVITY')

    def test_slow_is_not_dead(self):
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Reader(old=True), TODAY, 180)['status'], 'REVIEW_DUE')

    def test_release_counts(self):
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Reader(old=True, release=True), TODAY, 180)['status'], 'RECENT_ACTIVITY')

    def test_archived(self):
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Reader(archived=True), TODAY, 180)['status'], 'ARCHIVED')

    def test_disabled(self):
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Reader(disabled=True), TODAY, 180)['status'], 'DISABLED')

    def test_identity_change(self):
        self.assertEqual(tc.observe({'upstream': 'other/repo'}, Reader(), TODAY, 180)['status'], 'RENAMED')

    def test_unreachable_not_current(self):
        class Offline:
            def get(self, path):
                raise ValueError('GitHub API HTTP 429')
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Offline(), TODAY, 180)['status'], 'UNRESOLVED')

    def test_malformed_not_current(self):
        class Broken:
            def get(self, path):
                return None
        self.assertEqual(tc.observe({'upstream': 'org/repo'}, Broken(), TODAY, 180)['status'], 'UNRESOLVED')

    def test_timestamp_validation(self):
        for value in ('2099-01-01T00:00:00Z', '2026-01-01', None):
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                tc.timestamp(value, TODAY)

    def test_review_window_validation(self):
        for value in (0, -1, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                tc.report({}, TODAY, review_days=value)


if __name__ == '__main__':
    unittest.main()
