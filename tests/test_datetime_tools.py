#!/usr/bin/env python3
"""
Test suite for datetime MCP tools.
Run with: uv run python -m pytest tests/ -v
"""

from util_server import get_current_datetime, calculate_time_difference
import pytest
import asyncio
import sys
import os
from datetime import datetime, timezone, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestDateTimeTools:
    """Test class for datetime MCP tools."""

    @pytest.mark.asyncio
    async def test_get_current_datetime_utc_iso(self):
        """Test getting current datetime in UTC with ISO format."""
        result = await get_current_datetime("UTC", "iso")

        assert "Current DateTime" in result
        assert "**Timezone:** UTC" in result
        assert "**Format:** iso" in result
        assert "**DateTime:**" in result
        assert "**UTC Offset:** +0000" in result

    @pytest.mark.asyncio
    async def test_get_current_datetime_sao_paulo(self):
        """Test getting current datetime in São Paulo timezone."""
        result = await get_current_datetime("America/Sao_Paulo", "iso")

        assert "Current DateTime" in result
        assert "**Timezone:** America/Sao_Paulo" in result
        assert "**Format:** iso" in result
        assert "-03:00" in result  # São Paulo is UTC-3

    @pytest.mark.asyncio
    async def test_get_current_datetime_readable_format(self):
        """Test readable format output."""
        result = await get_current_datetime("UTC", "readable")

        assert "Current DateTime" in result
        assert "**Format:** readable" in result
        # Should contain day of week and full month name
        assert any(day in result for day in [
                   "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    @pytest.mark.asyncio
    async def test_get_current_datetime_timestamp_format(self):
        """Test timestamp format output."""
        result = await get_current_datetime("UTC", "timestamp")

        assert "Current DateTime" in result
        assert "**Format:** timestamp" in result
        # Should contain a numeric timestamp
        lines = result.split('\n')
        datetime_line = [
            line for line in lines if line.startswith("**DateTime:**")][0]
        timestamp = datetime_line.split("**DateTime:** ")[1]
        assert timestamp.isdigit()

    @pytest.mark.asyncio
    async def test_get_current_datetime_invalid_timezone(self):
        """Test error handling for invalid timezone."""
        result = await get_current_datetime("Invalid/Timezone", "iso")

        assert "❌ Unknown timezone" in result
        assert "Invalid/Timezone" in result
        assert "💡 Try:" in result

    @pytest.mark.asyncio
    async def test_calculate_time_difference_specific_dates(self):
        """Test calculating difference between specific dates."""
        result = await calculate_time_difference(
            "2025-09-09 10:00:00",
            "2025-09-09 14:30:00",
            "UTC"
        )

        assert "Time Difference Calculation" in result
        assert "**From:** 2025-09-09 10:00:00 UTC" in result
        assert "**To:** 2025-09-09 14:30:00 UTC" in result
        assert "**Total Duration:** 16,200 seconds" in result
        assert "- Days: 0" in result
        assert "- Hours: 4" in result
        assert "- Minutes: 30" in result
        assert "**Summary:** 4 hours, 30 minutes (later)" in result

    @pytest.mark.asyncio
    async def test_calculate_time_difference_to_now(self):
        """Test calculating difference from past time to now."""
        # Create a time 1 hour ago
        one_hour_ago = (datetime.now(timezone.utc) -
                        timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

        result = await calculate_time_difference(one_hour_ago, "", "UTC")

        assert "Time Difference Calculation" in result
        assert "Total Duration:" in result
        # Could be slightly over 1 hour
        assert "Hours: 1" in result or "Minutes: 60" in result
        assert "later" in result

    @pytest.mark.asyncio
    async def test_calculate_time_difference_past_to_future(self):
        """Test calculating difference where end is before start."""
        result = await calculate_time_difference(
            "2025-09-09 14:30:00",
            "2025-09-09 10:00:00",
            "UTC"
        )

        assert "Time Difference Calculation" in result
        assert "**Total Duration:** 16,200 seconds" in result
        assert "**Summary:** 4 hours, 30 minutes (earlier)" in result

    @pytest.mark.asyncio
    async def test_calculate_time_difference_invalid_start_date(self):
        """Test error handling for invalid start date format."""
        result = await calculate_time_difference("invalid-date", "", "UTC")

        assert "❌ Invalid start datetime format" in result
        assert "💡 Use: YYYY-MM-DD HH:MM:SS" in result

    @pytest.mark.asyncio
    async def test_calculate_time_difference_invalid_timezone(self):
        """Test error handling for invalid timezone in time calculation."""
        result = await calculate_time_difference(
            "2025-09-09 10:00:00",
            "2025-09-09 14:30:00",
            "Invalid/Timezone"
        )

        assert "❌ Unknown timezone" in result
        assert "Invalid/Timezone" in result


if __name__ == "__main__":
    # Run tests directly
    asyncio.run(TestDateTimeTools().test_get_current_datetime_utc_iso())
    print("✅ Basic test passed - run full suite with: uv run python -m pytest tests/ -v")
