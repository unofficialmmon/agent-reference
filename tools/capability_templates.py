#!/usr/bin/env python3
"""Static policy checks for shipped fragments, not a user-config patcher/schema."""
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from _audit_core import strip_jsonc
from quality import ROOT, require, unique_object

MCP_IDS = {'github', 'context7', 'serena', 'playwright'}


def parse(path):
    return json.loads(strip_jsonc(Path(path).read_text(encoding='utf-8')), object_pairs_hook=unique_object)


def validate_fragment(data):
    require(isinstance(data, dict) and set(data) <= {'$schema', 'mcp', 'permission'}, 'Fragment contains unrelated host settings')
    require(data.get('$schema') == 'https://opencode.ai/config.json', 'Missing OpenCode schema')
    mcps = data.get('mcp')
    require(isinstance(mcps, dict) and len(mcps) == 1, 'One MCP per merge fragment')
    ident, server = next(iter(mcps.items()))
    require(ident in MCP_IDS and isinstance(server, dict), 'Unknown MCP')
    require(server.get('enabled') is False, 'Shipped MCP fragments must be disabled')
    require(not ({'args', 'env', 'mcpServers'} & set(server)), 'Wrong host config shape')
    if ident in {'github', 'context7'}:
        require(server.get('type') == 'remote', 'Expected remote MCP')
        expected = 'https://api.githubcopilot.com/mcp/' if ident == 'github' else 'https://mcp.context7.com/mcp'
        require(server.get('url') == expected, 'Unexpected MCP endpoint')
        headers = server.get('headers')
        require(isinstance(headers, dict), 'Missing headers')
        if ident == 'github':
            require(server.get('oauth') is False, 'PAT configuration must disable OAuth discovery')
            require(headers.get('Authorization') == 'Bearer {env:GITHUB_PERSONAL_ACCESS_TOKEN}', 'Token must be an environment reference')
            require(headers.get('X-MCP-Readonly') == 'true', 'Read-only must not be disabled')
            require(headers.get('X-MCP-Toolsets') == 'repos,issues,pull_requests,actions', 'Unexpected broad toolset')
        else:
            require(headers == {'CONTEXT7_API_KEY': '{env:CONTEXT7_API_KEY}'}, 'Context7 key must be an environment reference')
    else:
        require(server.get('type') == 'local', 'Expected local MCP')
        command = server.get('command')
        require(isinstance(command, list) and len(command) >= 3 and all(isinstance(x, str) and x for x in command), 'Invalid command array')
        joined = ' '.join(command)
        require('@latest' not in joined and '<' not in joined and '>' not in joined, 'Unpinned/unresolved MCP command')
        require(data.get('permission', {}).get(ident + '_*') in {'ask', 'deny'}, 'Operational permission gate missing')
        if ident == 'playwright':
            require(command[:2] == ['npx', '-y'] and bool(re.fullmatch(r'@playwright/mcp@\d+\.\d+\.\d+', command[2])), 'Unpinned Playwright package')
            require('--isolated' in command and '--headless' in command, 'Isolated headless fixture required')
            require(not any(x.startswith(('--cdp', '--extension', '--user-data-dir', '--storage-state', '--no-sandbox', '--ignore-https-errors')) for x in command), 'Unsafe browser example')
        else:
            require(command[:2] == ['uvx', '--from'] and bool(re.fullmatch(r'git\+https://github.com/oraios/serena@[0-9a-f]{40}', command[2])), 'Unpinned Serena source')
            require('--project-from-cwd' in command and '--mode' in command and 'planning' in command, 'Missing Serena project/planning scope')
    return ident


def check(root=ROOT):
    files = sorted((root / 'templates/opencode').glob('*.jsonc'))
    require(len(files) == 4, 'Expected four MCP fragments')
    require({validate_fragment(parse(p)) for p in files} == MCP_IDS, 'MCP fragment coverage mismatch')
    routing = parse(root / 'templates/omo/mcp/readonly-research.jsonc')
    require(routing == {'agents': {'librarian': {'mcps': ['context7', 'gh_grep', 'github']}}}, 'Unexpected research routing expansion')
    project = json.loads((root / 'templates/opencode/serena-project.example.yml').read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    require(project.get('read_only') is True and project.get('activation_command') is None, 'Unsafe Serena project')
    require(project.get('fixed_tools') == ['get_symbols_overview', 'find_symbol', 'find_referencing_symbols'], 'Serena toolset expanded')
    require(project.get('excluded_tools') == [] and project.get('included_optional_tools') == [], 'Conflicting Serena fixed toolset')
    return {'status': 'PASS', 'scope': 'shipped-template-policy-only', 'fragments': len(files), 'hostBehavior': 'NOT RUN'}


if __name__ == '__main__':
    try:
        print(json.dumps(check()))
    except (ValueError, TypeError, KeyError, IndexError, OSError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}))
        raise SystemExit(1)
