"""
General-Purpose Utility MCP Server
Simple automation tools and utilities for productivity enhancement.

Created by: Cod.1 (Coder Agent)
Date: 2025-09-06
Mission: T83 Component 2 - Simplified Utility Server Approach
"""

import os
from typing import Optional, Dict, Any
import httpx
import json
from datetime import datetime, timezone
import pytz

from mcp.server.fastmcp import FastMCP


# Create FastMCP server
mcp = FastMCP("Utility Server")


class ReadAIClient:
    """Simple Read.AI API client for downloading meeting data."""

    def __init__(self):
        self.api_key = os.getenv('READ_AI_API_KEY')
        self.base_url = os.getenv('READ_AI_API_URL', 'https://api.read.ai/v1')

    def is_available(self) -> bool:
        """Check if Read.AI integration is configured."""
        return bool(self.api_key)

    async def get_meeting_data(self, meeting_id: str, include_transcript: bool = True, include_summary: bool = True) -> Dict[str, Any]:
        """Download meeting transcript and/or summary from Read.AI."""

        if not self.is_available():
            return {
                'error': 'Read.AI API key not configured',
                'config_help': 'Set READ_AI_API_KEY environment variable',
                'mock_data': self._get_mock_data(meeting_id, include_transcript, include_summary)
            }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }

                result = {'meeting_id': meeting_id}

                if include_transcript:
                    transcript_url = f"{self.base_url}/meetings/{meeting_id}/transcript"
                    response = await client.get(transcript_url, headers=headers)
                    response.raise_for_status()
                    result['transcript'] = response.json()

                if include_summary:
                    summary_url = f"{self.base_url}/meetings/{meeting_id}/summary"
                    response = await client.get(summary_url, headers=headers)
                    response.raise_for_status()
                    result['summary'] = response.json()

                return result

        except httpx.HTTPStatusError as e:
            return {
                'error': f'Read.AI API error: {e.response.status_code}',
                'details': e.response.text,
                'meeting_id': meeting_id
            }
        except Exception as e:
            return {
                'error': f'Request failed: {str(e)}',
                'meeting_id': meeting_id
            }

    def _get_mock_data(self, meeting_id: str, include_transcript: bool, include_summary: bool) -> Dict[str, Any]:
        """Provide mock data for development/testing."""
        mock_data = {'meeting_id': meeting_id}

        if include_transcript:
            mock_data['transcript'] = {
                'segments': [
                    {'speaker': 'Alice', 'timestamp': '00:00',
                        'text': 'Good morning everyone, let\'s start our standup.'},
                    {'speaker': 'Bob', 'timestamp': '00:30',
                        'text': 'I completed the API integration yesterday.'},
                    {'speaker': 'Carol', 'timestamp': '01:00',
                        'text': 'Great! I\'m working on the frontend components.'}
                ]
            }

        if include_summary:
            mock_data['summary'] = {
                'key_points': [
                    'Team standup meeting held',
                    'Bob completed API integration',
                    'Carol working on frontend components'
                ],
                'action_items': [
                    'Carol to complete frontend by Friday',
                    'Bob to review Carol\'s code'
                ],
                'duration_minutes': 15,
                'participant_count': 3
            }

        return mock_data


# Initialize Read.AI client
readai_client = ReadAIClient()


# MCP Tools

@mcp.tool()
async def get_current_datetime(timezone_name: str = "UTC", format_type: str = "iso") -> str:
    """
    Get the current date and time in the specified timezone and format.

    Args:
        timezone_name: Timezone name (e.g., "UTC", "US/Eastern", "Europe/London", "America/Sao_Paulo")
        format_type: Format type ("iso", "readable", "timestamp", "custom")

    Returns:
        Current datetime in the requested format
    """
    try:
        # Get current UTC time
        now_utc = datetime.now(timezone.utc)

        # Convert to requested timezone
        if timezone_name.upper() == "UTC":
            target_time = now_utc
        else:
            try:
                tz = pytz.timezone(timezone_name)
                target_time = now_utc.astimezone(tz)
            except pytz.UnknownTimeZoneError:
                return f"❌ Unknown timezone: {timezone_name}\n💡 Try: UTC, US/Eastern, Europe/London, America/Sao_Paulo, etc."

        # Format the datetime
        if format_type.lower() == "iso":
            formatted_time = target_time.isoformat()
        elif format_type.lower() == "readable":
            formatted_time = target_time.strftime(
                "%A, %B %d, %Y at %I:%M:%S %p %Z")
        elif format_type.lower() == "timestamp":
            formatted_time = str(int(target_time.timestamp()))
        else:  # custom or other
            formatted_time = target_time.strftime("%Y-%m-%d %H:%M:%S %Z")

        result = f"🕐 **Current DateTime**\n"
        result += f"**Timezone:** {timezone_name}\n"
        result += f"**Format:** {format_type}\n"
        result += f"**DateTime:** {formatted_time}\n"
        result += f"**UTC Offset:** {target_time.strftime('%z')}\n"

        return result

    except Exception as e:
        return f"❌ Error getting current datetime: {str(e)}"


@mcp.tool()
async def calculate_time_difference(start_datetime: str, end_datetime: str = "", timezone_name: str = "UTC") -> str:
    """
    Calculate the time difference between two datetimes or from a start time to now.

    Args:
        start_datetime: Start datetime in ISO format (YYYY-MM-DD HH:MM:SS or YYYY-MM-DDTHH:MM:SS)
        end_datetime: End datetime in ISO format (optional - defaults to current time)
        timezone_name: Timezone for interpretation (default: UTC)

    Returns:
        Time difference with detailed breakdown
    """
    try:
        # Parse timezone
        if timezone_name.upper() == "UTC":
            tz = timezone.utc
        else:
            try:
                tz = pytz.timezone(timezone_name)
            except pytz.UnknownTimeZoneError:
                return f"❌ Unknown timezone: {timezone_name}\n💡 Try: UTC, US/Eastern, Europe/London, America/Sao_Paulo, etc."

        # Parse start datetime
        try:
            # Handle different datetime formats
            if 'T' in start_datetime:
                start_dt = datetime.fromisoformat(
                    start_datetime.replace('Z', '+00:00'))
            else:
                start_dt = datetime.strptime(
                    start_datetime, "%Y-%m-%d %H:%M:%S")
                start_dt = start_dt.replace(tzinfo=tz)
        except ValueError:
            return f"❌ Invalid start datetime format: {start_datetime}\n💡 Use: YYYY-MM-DD HH:MM:SS or YYYY-MM-DDTHH:MM:SS"

        # Parse end datetime or use current time
        if end_datetime:
            try:
                if 'T' in end_datetime:
                    end_dt = datetime.fromisoformat(
                        end_datetime.replace('Z', '+00:00'))
                else:
                    end_dt = datetime.strptime(
                        end_datetime, "%Y-%m-%d %H:%M:%S")
                    end_dt = end_dt.replace(tzinfo=tz)
            except ValueError:
                return f"❌ Invalid end datetime format: {end_datetime}\n💡 Use: YYYY-MM-DD HH:MM:SS or YYYY-MM-DDTHH:MM:SS"
        else:
            end_dt = datetime.now(tz)

        # Calculate difference
        time_diff = end_dt - start_dt

        # Extract components
        total_seconds = abs(time_diff.total_seconds())
        days = int(total_seconds // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        # Determine direction
        direction = "later" if time_diff.total_seconds() >= 0 else "earlier"

        # Format result
        result = f"⏱️ **Time Difference Calculation**\n"
        result += f"**From:** {start_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        result += f"**To:** {end_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        result += f"**Timezone:** {timezone_name}\n\n"

        result += f"**Total Duration:** {total_seconds:,.0f} seconds\n"
        result += f"**Breakdown:**\n"
        result += f"- Days: {days}\n"
        result += f"- Hours: {hours}\n"
        result += f"- Minutes: {minutes}\n"
        result += f"- Seconds: {seconds}\n\n"

        # Human-readable summary
        if days > 0:
            result += f"**Summary:** {days} days, {hours} hours, {minutes} minutes ({direction})\n"
        elif hours > 0:
            result += f"**Summary:** {hours} hours, {minutes} minutes ({direction})\n"
        elif minutes > 0:
            result += f"**Summary:** {minutes} minutes, {seconds} seconds ({direction})\n"
        else:
            result += f"**Summary:** {seconds} seconds ({direction})\n"

        return result

    except Exception as e:
        return f"❌ Error calculating time difference: {str(e)}"


@mcp.tool()
async def download_meeting_data(meeting_id: str, include_transcript: bool = True, include_summary: bool = True) -> str:
    """
    Download meeting transcript and/or summary from Read.AI.

    Args:
        meeting_id: Read.AI meeting ID
        include_transcript: Whether to download the full transcript (default: True)
        include_summary: Whether to download the meeting summary (default: True)

    Returns:
        Meeting data in formatted text or JSON structure
    """

    try:
        data = await readai_client.get_meeting_data(meeting_id, include_transcript, include_summary)

        # Handle errors
        if 'error' in data:
            result = f"❌ Error downloading meeting {meeting_id}:\n"
            result += f"   {data['error']}\n"

            if 'config_help' in data:
                result += f"   Configuration: {data['config_help']}\n"

            # Show mock data if available
            if 'mock_data' in data:
                result += "\n📝 Mock data for development:\n"
                result += json.dumps(data['mock_data'], indent=2)

            return result

        # Format successful response
        result = f"✅ Meeting Data Downloaded: {meeting_id}\n"
        result += "=" * 50 + "\n\n"

        if include_transcript and 'transcript' in data:
            result += "## Transcript\n"
            if 'segments' in data['transcript']:
                for segment in data['transcript']['segments']:
                    result += f"[{segment.get('timestamp', '??:??')}] {segment.get('speaker', 'Speaker')}: {segment.get('text', '')}\n"
            else:
                result += json.dumps(data['transcript'], indent=2)
            result += "\n"

        if include_summary and 'summary' in data:
            result += "## Summary\n"
            summary = data['summary']

            if 'key_points' in summary:
                result += "**Key Points:**\n"
                for point in summary['key_points']:
                    result += f"- {point}\n"
                result += "\n"

            if 'action_items' in summary:
                result += "**Action Items:**\n"
                for item in summary['action_items']:
                    result += f"- {item}\n"
                result += "\n"

            if 'duration_minutes' in summary:
                result += f"**Duration:** {summary['duration_minutes']} minutes\n"

            if 'participant_count' in summary:
                result += f"**Participants:** {summary['participant_count']}\n"

            # Add raw JSON if structure is different
            if not any(key in summary for key in ['key_points', 'action_items']):
                result += json.dumps(summary, indent=2) + "\n"

        # Add development note if using mock data
        if not readai_client.is_available():
            result += "\n📝 Note: Using mock data. Configure READ_AI_API_KEY for live Read.AI integration.\n"

        return result

    except Exception as e:
        return f"❌ Unexpected error downloading meeting {meeting_id}: {str(e)}"


@mcp.tool()
async def util_server_status() -> str:
    """
    Check the status of all utility server integrations.

    Returns:
        Status report of available utilities and their configuration
    """

    status = "Utility Server Status\n"
    status += "===================\n\n"

    # Read.AI Integration
    status += "**Read.AI Meeting Downloader**\n"
    status += f"- Available: {'✅ Yes' if readai_client.is_available() else '❌ No (API key needed)'}\n"
    status += f"- API Base URL: {readai_client.base_url}\n"
    if not readai_client.is_available():
        status += "- Configuration: Set READ_AI_API_KEY environment variable\n"
        status += "- Development: Mock data available for testing\n"
    status += "\n"

    # Datetime Tools
    status += "**DateTime Tools**\n"
    status += "- Available: ✅ Yes (no configuration needed)\n"
    status += "- Timezone Support: Full pytz timezone database\n"
    status += "- Formats: ISO, readable, timestamp, custom\n"
    status += "\n"

    # Server Info
    status += "**Server Information**\n"
    status += "- Framework: FastMCP\n"
    status += "- Tools Available: 4\n"
    status += "- Purpose: General-purpose utilities for productivity\n"
    status += "\n"

    # Available Tools
    status += "**Available Tools**\n"
    status += "1. `get_current_datetime` - Get current date/time in any timezone and format\n"
    status += "2. `calculate_time_difference` - Calculate time differences with detailed breakdown\n"
    status += "3. `download_meeting_data` - Download Read.AI meeting transcripts and summaries\n"
    status += "4. `util_server_status` - Check utility server status and configuration\n"
    status += "\n"

    # Future Expansion
    status += "**Expansion Ready**\n"
    status += "This server is designed to house multiple simple utility tools.\n"
    status += "New tools can be easily added without creating separate MCP servers.\n"

    return status


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='stdio')
