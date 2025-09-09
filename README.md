# Utility MCP Server

General-purpose MCP server providing utility tools for Computer Agent ecosystem integration.

## Features

### Read.AI Meeting Downloader

- **Tool**: `download_meeting_data`
- **Purpose**: Download meeting transcripts and summaries from Read.AI platform
- **Status**: ⚠️ **API Key Required** - Read.AI API documentation not publicly available
- **Configuration**: Requires `READ_AI_API_KEY` environment variable

### Server Status

- **Tool**: `util_server_status`
- **Purpose**: Check configuration and availability of all utility tools

## Installation

```bash
cd /home/danfmaia/_repos/_mcp/util-mcp
uv install
```

## Usage

### MCP Server (via Cursor)

The server is configured in `/home/danfmaia/.cursor/mcp.json`:

```json
{
  "utilities": {
    "name": "Utility MCP Server",
    "type": "command",
    "command": "/home/danfmaia/.local/bin/uv",
    "args": [
      "--directory",
      "/home/danfmaia/_repos/_mcp/util-mcp",
      "run",
      "util_server.py"
    ]
  }
}
```

### Standalone Testing

```bash
uv run util_server.py
```

## Technical Constraints

### Read.AI API Limitation

**Current Status**: No publicly available Read.AI API documentation or third-party access endpoints identified.

**Search Evidence**:

- Cursor native @Web search: No API documentation found
- Custom MCP web research: No API endpoints discovered
- Technical assessment: Browser automation would require significant maintenance overhead

**Recommendation**: Manual download workflow until Read.AI provides official API access.

## Dependencies

- `mcp`: Model Context Protocol framework
- `httpx`: HTTP client for potential API calls
- `fastmcp`: Simplified MCP server development

## Development

Built using FastMCP framework for simplified MCP server development and maintenance.
