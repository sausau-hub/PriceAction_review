import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { execSync } from 'child_process';

function ntn(method, path, body) {
  const args = ['api', '-X', method, path];
  if (body) args.push('-d', JSON.stringify(body));
  const result = execSync(`ntn ${args.map(a => `"${a.replace(/"/g,'\\\"')}"`).join(' ')}`, {
    encoding: 'utf8', timeout: 30000, windowsHide: true,
  });
  return JSON.parse(result);
}

const server = new McpServer({ name: 'notion', version: '1.0.0' });

server.tool('notion_create_database',
  'Create a new Notion database under a parent page',
  {
    parent_page_id: z.string().describe('Parent page ID'),
    title: z.string().describe('Database title'),
    properties: z.string().describe('JSON string of Notion property definitions'),
  },
  async ({ parent_page_id, title, properties }) => {
    const props = JSON.parse(properties);
    const body = {
      parent: { type: 'page_id', page_id: parent_page_id },
      title: [{ type: 'text', text: { content: title } }],
      properties: props,
    };
    const r = ntn('POST', '/databases', body);
    return { content: [{ type: 'text', text: JSON.stringify({ id: r.id, url: r.url }) }] };
  }
);

server.tool('notion_create_page',
  'Create a new page/row in a Notion database',
  {
    database_id: z.string().describe('Target database ID'),
    properties: z.string().describe('JSON string of property values for the new page'),
    children: z.string().optional().describe('JSON string of block children content'),
  },
  async ({ database_id, properties, children }) => {
    const body = {
      parent: { database_id },
      properties: JSON.parse(properties),
    };
    if (children) body.children = JSON.parse(children);
    const r = ntn('POST', '/pages', body);
    return { content: [{ type: 'text', text: JSON.stringify({ id: r.id, url: r.url }) }] };
  }
);

server.tool('notion_query_database',
  'Query pages in a Notion database with optional filter',
  {
    database_id: z.string().describe('Database ID to query'),
    filter: z.string().optional().describe('JSON string of Notion filter object'),
    page_size: z.number().optional().describe('Max results (default 10)'),
  },
  async ({ database_id, filter, page_size }) => {
    const body = { page_size: page_size || 10 };
    if (filter) body.filter = JSON.parse(filter);
    const r = ntn('POST', `/databases/${database_id}/query`, body);
    const rows = (r.results || []).map(p => ({ id: p.id, url: p.url, properties: p.properties }));
    return { content: [{ type: 'text', text: JSON.stringify(rows) }] };
  }
);

server.tool('notion_update_page',
  'Update properties of an existing Notion page/row',
  {
    page_id: z.string().describe('Page ID to update'),
    properties: z.string().describe('JSON string of property values to update'),
  },
  async ({ page_id, properties }) => {
    const body = { properties: JSON.parse(properties) };
    const r = ntn('PATCH', `/pages/${page_id}`, body);
    return { content: [{ type: 'text', text: JSON.stringify({ id: r.id, url: r.url }) }] };
  }
);

server.tool('notion_get_database',
  'Get metadata and property schema of a Notion database',
  {
    database_id: z.string().describe('Database ID'),
  },
  async ({ database_id }) => {
    const r = ntn('GET', `/databases/${database_id}`);
    return { content: [{ type: 'text', text: JSON.stringify({ id: r.id, title: r.title, properties: Object.keys(r.properties) }) }] };
  }
);

server.tool('notion_append_blocks',
  'Append block content to an existing Notion page',
  {
    page_id: z.string().describe('Page ID to append to'),
    children: z.string().describe('JSON array of block objects'),
  },
  async ({ page_id, children }) => {
    const body = { children: JSON.parse(children) };
    const r = ntn('PATCH', `/blocks/${page_id}/children`, body);
    return { content: [{ type: 'text', text: JSON.stringify({ results_count: r.results?.length }) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
