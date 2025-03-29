import os
from serpapi import GoogleSearch
from dataclasses import dataclass

import anyio
import anyio.to_thread
from pydantic import TypeAdapter
from typing_extensions import TypedDict

from pydantic_ai.tools import Tool

__all__ = ("google_search_tool",)


class GoogleResult(TypedDict):
    """A DuckDuckGo search result."""

    position: int
    title: str
    link: str
    snippet: str
    source: str


google_ta = TypeAdapter(list[GoogleResult])


@dataclass
class GoogleSearchTool:
    """The Google search tool."""

    api_key: str
    """The API key for the SerpApi."""

    max_results: int | None = None
    """The maximum number of results. If None, returns results only from the first response."""

    async def __call__(self, query: str) -> list[GoogleResult]:
        """Searches Google for the given query and returns the results.

        SerApi have a limit of 100 queries a month on the free plan.

        The parameters available for GoogleSearch are:
        <https://serpapi.com/integrations/python#google-search-api-capability>

        Args:
            query: The query to search for.

        Returns:
            The search results.
        """
        search = GoogleSearch({"q": query, "api_key": self.api_key})
        result = await anyio.to_thread.run_sync(search.get_dict)
        return google_ta.validate_python(result["organic_results"])


def google_search_tool(max_results: int = 10):
    """Creates a Google search tool.

    Args:
        duckduckgo_client: The DuckDuckGo search client.
        max_results: The maximum number of results. If None, returns results only from the first response.
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        raise RuntimeError("SERP_API_KEY is not set.")

    return Tool(
        GoogleSearchTool(api_key=api_key, max_results=max_results).__call__,
        name="google_search",
        description="Searches Google for the given query and returns the results.",
    )
