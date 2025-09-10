# Utility MCP Server

General-purpose MCP server providing utility tools for Computer Agent ecosystem integration.

## Features

### DateTime Tools ⭐ NEW

- **Tool**: `get_current_datetime`
- **Purpose**: Get current date/time in any timezone with multiple format options
- **Status**: ✅ **Ready** - No configuration required
- **Timezones**: Full pytz database support (UTC, US/Eastern, Europe/London, America/Sao_Paulo, etc.)
- **Formats**: ISO, readable, timestamp, custom

- **Tool**: `calculate_time_difference`
- **Purpose**: Calculate time differences between dates or from a date to now
- **Status**: ✅ **Ready** - No configuration required
- **Features**: Detailed breakdown (days, hours, minutes, seconds), multiple input formats

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

### Testing DateTime Tools

```bash
uv run python test_datetime.py
```

## Usage Examples

### DateTime Tools

**Get current time in different timezones:**

- `get_current_datetime("UTC", "readable")` → "Tuesday, September 09, 2025 at 11:56:34 PM UTC"
- `get_current_datetime("America/Sao_Paulo", "iso")` → "2025-09-09T20:56:34-03:00"
- `get_current_datetime("US/Eastern", "custom")` → "2025-09-09 19:56:34 EDT"

**Calculate time differences:**

- `calculate_time_difference("2025-09-09 10:00:00", "2025-09-09 14:30:00", "UTC")` → "4 hours, 30 minutes"
- `calculate_time_difference("2025-09-08 15:00:00", "", "UTC")` → Time from yesterday 3pm to now

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
- `pytz`: Timezone database for datetime operations
- `fastmcp`: Simplified MCP server development

## Development

Built using FastMCP framework for simplified MCP server development and maintenance.
