# Harvesting the queries an assistant fires before it answers

Ask ChatGPT a buying question and it runs two or three web searches of its own before it writes
a word. Those **fan-out queries** are the brief for the page that wins the citation. They are
not what the buyer typed; they are what the machine decided to go and look up on the buyer's
behalf, which is a better description of what a page has to contain.

There are two ways to read them and they are not equivalent. Use the account.

## The good source: a logged-in session

```
GET /backend-api/conversation/<id>
Authorization: Bearer <accessToken from /api/auth/session>
```

There is no `queries` field, whatever a tutorial tells you to search for. The searches are
`assistant` messages with `content_type: "code"` addressed to `recipient: "web.run"`, one query
per line, in an undocumented syntax:

```
fast|ClickUp creative agency features proofing workload docs automations 2026|30|clickup.com
slow|best ClickUp consulting agencies marketing agency ClickUp consultant 2026|30
business|France|agence automatisation IA PME;agence automation IA Make n8n PME
```

`lane|query|recency in days|site filter`, where the last two are optional. `fast` is the ordinary
lookup, `slow` reaches past the first page, and `business|<geo>|<q>;<q>` is a **local business
lookup** rather than a web search, `<geo>` is a place or the literal `user`, meaning the buyer's
own location. A prompt that fires `business|` is telling you a Google Business Profile is part of
the answer and no article will reach it.

The retrieved pages are on the `tool` message as `metadata.search_result_groups`, grouped by
domain. **That is the whole consideration set**, including every page the answer then ignored,
and it is the most useful thing in the response.

Driving 24 prompts unattended: type into `#prompt-textarea` with
`document.execCommand('insertText')`, click `[data-testid="send-button"]`, wait for
`[data-testid="stop-button"]` to disappear, click `a[href="/"]` for the next. New chat is
client-side routing, so an in-page async loop survives the whole run and the browser automation
only has to poll it. Do not pass `?q=...&hints=search`: the hint chip injects the literal string
`@Web search` into the first search call.

**Logged out is a dead end, not a slower path.** An anonymous conversation is served from
`/unauth-mweb/conversation/updates`, streams HTML fragments rather than JSON, says only
`Searching 9 websites` where the queries would be, and `GET /backend-api/conversation/<id>`
answers `conversation_inaccessible`. There is no `queries` key in 115KB of it.

## The fallback: DataForSEO, for a niche you have no account in

```
POST /v3/ai_optimization/chat_gpt/llm_responses/live
[{ "user_prompt": "...", "model_name": "gpt-5.5", "web_search": true }]
```

`fan_out_queries` comes back beside the answer, at about $0.09 a prompt. It is a fair proxy for
**subject** and a bad one for **standing**. Measured against the real product on the same 24
prompts, 1 Sep 2026:

| | DataForSEO | chatgpt.com logged in |
| --- | --- | --- |
| the client's mentions | 9 of 24 | 11 of 24 |
| the incumbent's mentions | **0** | **9** |
| prompts running no search | 2 | 1, and a different one |
| query syntax | bare strings | lane, recency window, site pin |
| local `business\|` lookups | absent | 5 of 24 prompts |
| retrieved-but-not-cited pages | absent | the whole consideration set |

Never quote its scoreboard. It reported the incumbent as absent from a category it appears in
nine times out of 24, which is the kind of wrong that gets a strategy built on it.

## Five rules from the first two runs

**A fan-out query is not a keyword.** Many come back machine-shaped, in strings no human would
type. They carry no search volume and must never be quoted as one. Only the human-shaped minority
belongs in a rank tracker. The rest is the outline of a single page that answers all of one
prompt's fan-out at once, which is the page that gets lifted.

**An empty fan-out is a do-not-write signal.** The model answered from memory without searching,
so no page can win that prompt. Check it before committing a page, and check it on the real
product, because the fallback got which prompt this was wrong.

**Retrieved and rejected beats every ranking signal you have.** When the consideration set holds
your page and the answer names somebody else, the page was read and judged not to answer. There is
no discovery problem left to solve, only a content one. One run found a page that had the measured
proof on it, retrieved on a prompt asking for exactly that proof, losing anyway because the number
sat on a case-study page rather than on the page answering the question.

**Ranking and being lifted are different.** A page ranking 7th on Google for the exact query went
uncited in the same week. Position is not the currency.

**The directory is often the lever, not the article.** In one run the assistant paged twelve deep
through a vendor's partner directory and pulled individual partner profiles. The most-retrieved
domain was not being read as a vendor; it was being mined for names. Check what the retrieved set
is actually made of before planning a single page.
