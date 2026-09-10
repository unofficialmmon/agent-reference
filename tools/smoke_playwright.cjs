// Direct MCP protocol smoke in a disposable localhost fixture; no model/host claim.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');
const { createRequire } = require('node:module');

async function main() {
  const prefix = process.env.CAPABILITY_PREFIX;
  if (!prefix || !path.isAbsolute(prefix)) throw new Error('CAPABILITY_PREFIX must name the isolated installed dependency directory');
  const dependency = createRequire(path.join(prefix, 'package.json'));
  const { Client } = dependency('@modelcontextprotocol/sdk/client/index.js');
  const { StdioClientTransport } = dependency('@modelcontextprotocol/sdk/client/stdio.js');
  const binary = path.join(prefix, 'node_modules/@playwright/mcp/cli.js');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'agent-reference-browser-'));
  const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<!doctype html><title>Local MCP fixture</title><main><h1>Local MCP fixture</h1><p>No external data or credentials.</p></main>');
  });
  const client = new Client({ name: 'agent-reference-smoke', version: '1.0.0' });
  const transport = new StdioClientTransport({ command: process.execPath, args: [binary, '--isolated', '--headless', '--browser', 'chromium', '--output-dir', dir], stderr: 'pipe' });
  try {
    await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
    await client.connect(transport);
    const tools = await client.listTools();
    for (const name of ['browser_navigate', 'browser_snapshot', 'browser_close']) {
      if (!tools.tools.some(t => t.name === name)) throw new Error(`Missing MCP tool ${name}`);
    }
    const navigation = await client.callTool({ name: 'browser_navigate', arguments: { url: `http://127.0.0.1:${server.address().port}/` } });
    if (navigation.isError) throw new Error('Local browser navigation failed');
    const snapshot = await client.callTool({ name: 'browser_snapshot', arguments: {} });
    if (snapshot.isError || !JSON.stringify(snapshot.content).includes('Local MCP fixture')) throw new Error('Local fixture absent from browser snapshot');
    const closed = await client.callTool({ name: 'browser_close', arguments: {} });
    if (closed.isError) throw new Error('Browser cleanup failed');
    console.log(JSON.stringify({ status: 'PASS', mcpVersion: dependency('@playwright/mcp/package.json').version, checks: ['initialize', 'tools-list', 'localhost-navigation', 'snapshot', 'browser-close'], openCodeHost: 'NOT RUN', personalProfile: 'NOT USED' }));
  } finally {
    await client.close().catch(() => {});
    await transport.close().catch(() => {});
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(dir, { recursive: true, force: true });
  }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
