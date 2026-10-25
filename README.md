<p align="center">
  <a href="https://www.instnews.net">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/logo-full-dark.svg">
      <img src="assets/logo-full.svg" alt="InstNews" width="340">
    </picture>
  </a>
</p>

<p align="center">
  <strong><a href="https://www.instnews.net">www.instnews.net</a></strong>
  &nbsp;·&nbsp; <a href="https://www.instnews.net/docs">Docs</a>
  &nbsp;·&nbsp; <a href="https://www.instnews.net/pricing">Pricing</a>
  &nbsp;·&nbsp; <a href="https://www.instnews.net/openapi.json">OpenAPI</a>
</p>

# InstNews — real-time stock market news API

InstNews turns the market's news firehose into a clean, machine-readable signal
feed. It aggregates 40+ sources in real time — major financial newswires, SEC
EDGAR 8-K filings, dedicated earnings wires, and curated social feeds — runs
every story through an AI analysis pipeline, and serves the result as simple
JSON: each item mapped to its ticker, with sentiment and trading-signal fields
on paid tiers.

No signup, no key, no SDK required to start:

```sh
curl 'https://www.instnews.net/api/news?tickers=NVDA&limit=5'
```

## Why InstNews

- **Analyzed, not just aggregated** — stories are mapped to the asset they are
  about (`target_asset`, `asset_type`, available to everyone, including
  anonymous callers). Pro/Max responses add AI sentiment, confidence, risk
  level, tradeability, and priced-in analysis.
- **Sources that move markets** — newswires, SEC EDGAR 8-K filings (earnings
  surprises straight from the source), Nasdaq and Benzinga earnings wires, and
  social feeds, deduplicated into one stream.
- **Push, not just pull** — `GET /api/news/stream` is a server-sent-events
  endpoint; hold one HTTP connection and receive items as they are ingested.
- **Built for machines** — a stable JSON schema, an
  [OpenAPI specification](https://www.instnews.net/openapi.json), an
  [llms.txt](https://www.instnews.net/llms.txt), and an MCP server so LLM
  agents can use the data directly.

## Quick start

```sh
curl 'https://www.instnews.net/api/news?limit=1'
python3 instnews.py
```

```python
from instnews import InstNews

client = InstNews()
result = client.news(limit=10, q="earnings")
for item in result["items"]:
    print(item.get("title"), item.get("link"))
```

The example client (`instnews.py`) uses only the Python standard library. It
exposes news, sources, and stats and reports HTTP errors without automatically
retrying requests.

## Authentication

- **Free tier:** no key, no signup — every `/api/*` endpoint works anonymously
  within free-tier limits.
- **Pro/Max REST:** pass your API key (issued from the
  [account dashboard](https://www.instnews.net/account)) as an
  `X-API-Key: <key>` header. Note: `Authorization: Bearer` on the REST API is
  reserved for browser session tokens, not API keys.
- **MCP:** the same dashboard API key, as `Authorization: Bearer <key>` or
  `X-API-Key: <key>` (see below). Pro or Max tier required.

Rate limits, items per request, and history depth depend on your plan — see
[pricing](https://www.instnews.net/pricing) for current tiers.

## REST endpoints

- `GET /api/news` — JSON news; supports search, source, date, sentiment, and
  ticker filters.
- `GET /api/news/stream` — server-sent events.
- `GET /api/sources` — available sources.
- `GET /api/stats` — service statistics.

CORS is not enabled on the REST API: call it from a server or CLI, not from
cross-origin browser JavaScript.

## Documentation

- [Stock market news API](https://www.instnews.net/stock-market-news-api)
- [API reference](https://www.instnews.net/docs/api-reference)
- [OpenAPI specification](https://www.instnews.net/openapi.json)

## MCP server

Streamable HTTP at `https://mcp.instnews.net/mcp` with a Pro or Max API key.
This is separate from the anonymous REST news free tier, and it serves **market
data**, not news: 36 tools covering US stock aggregates, snapshots, top movers,
ticker reference, dividends/splits/financials, technical indicators, options
chains/contracts, and futures quotes/bars with fuzzy symbol resolution
("CL=F", "crude oil").

Claude Code:

```sh
claude mcp add --transport http instnews-markets https://mcp.instnews.net/mcp \
  --header "Authorization: Bearer YOUR_API_KEY"
```

Cursor (`~/.cursor/mcp.json`; replace the placeholder locally):

```json
{
  "mcpServers": {
    "instnews-markets": {
      "url": "https://mcp.instnews.net/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

Claude Desktop (via `mcp-remote`) splits header values on whitespace — use the
`X-API-Key` form there:

```json
{
  "mcpServers": {
    "instnews-markets": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.instnews.net/mcp",
               "--header", "X-API-Key: YOUR_API_KEY"]
    }
  }
}
```

Do not commit a real key.

## License

Apache-2.0 (see [LICENSE](LICENSE)). API data access and redistribution remain
subject to the [service terms](https://www.instnews.net/).
