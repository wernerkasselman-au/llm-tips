# Token-Efficient Documentation Guide

Research: 42 articles (2025-2026) | Key Finding: 35-50% reduction, comprehension maintained/improved

## Principles

### 1. Information Density > Character Count

Myth: Shorter text = fewer tokens
Reality: `customer_id` (2 tok) vs `customerId` (3 tok). Shorter isn't cheaper.
Rule: Optimize semantic density. Remove articles only when non-essential.

### 2. Markdown > JSON for Documentation

Evidence: Markdown = 16% token savings vs JSON, +10% comprehension (Medium 2026)

| Format | Tokens | Comprehension | Use |
|--------|--------|---------------|-----|
| CSV | ★★★★★ | ❌ 44% | Avoid |
| JSON | ★★★ | ★★★ 50% | APIs only |
| Markdown | ★★★★ | ★★★★ 55% | Default |
| MD-KV | ★ | ★★★★★ 61% | Complex |

Why: it's LLM training bias (GitHub/Stack Overflow), hierarchical parsing, compression 0.65-0.80

### 3. Structure-Aware Organization

Pattern:
```markdown
# Concept
1-sentence overview
## Sub-concept
- Terse point
```

Anti-pattern: narrative paragraphs that don't earn their tokens

## Techniques

### T1: Remove Filler Phrases

| Before | After | Savings |
|--------|-------|---------|
| This tool is used to execute Claude CLI commands. You should use... (28t) | Executes Claude CLI commands for CLI interaction (10t) | 64% |

Remove: `This tool is used to` → direct verb | `You should use` → omit | `In order to` → `To` | `It should be noted that` → omit

### T2: Remove Unnecessary Articles

Before: The correlation ID is a unique identifier for the request (13t)
After: Correlation ID: unique identifier for request (8t)
Savings: 38%

Keep articles when they're load-bearing: technical distinction (`a session` vs `the session`), or clarity

### T3: Compact Structures

Before: `{ id, name, created_at }` (11t)
After: `{id,name,created_at}` (7t)
Savings: 36%

Conventions: ✅ `snake_case` (2t) | ❌ `camelCase` (3t) | ✅ Terse: `IN`,`OUT`,`ERR`

### T4: Inline Constraints

Before: `quantity: number  // Must be >0, required` (8t)
After: `quantity:int!>0` (3t)
Savings: 58%

Notation: `!`=required | `?`=optional | `:int`=type | `>0`=constraint

### T5: Consolidate Tools

Before: Separate tools (web_search_google, web_search_bing, web_search_duckduckgo) 150t
After: Single tool + parameter (web_search, provider:enum) 50t
Savings: 67%

### T6: Terse Descriptions

Formula: Verb + Object + Features (≤12 words)

Before (45t):
```text
This tool allows you to execute requests to the Claude CLI. It provides
comprehensive support...
```
After (10t):
```text
Executes Claude CLI requests with model/session/format control
```
Savings: 78%

### T7: Standard Parameter Names

Consistency benefits: the model learns the name once, so it doesn't spend tokens on variants

Standards: `query` (not searchTerm/q/search) | `session_id` (not sessionId/sid) | `model` (not modelName/llm)

## MCP Optimizations

### Tool Schema Cost

Per tool: name(3-5) + desc(20-50) + params(50-100) = 75-155 tokens
10 tools: 750-1,550 tokens for schema alone

Strategies:
1. Filter: `allowed_tools:["claude_request","gemini_request"]` → Save 75-155 per excluded
2. Cache: `previous_response_id:last.id` → 90% savings on repeats
3. Prune: `exposedTools=all.filter(t=>t.relevance>0.7&&!t.sensitive)`

### Resource Optimization

Pattern:
```typescript
{uri:"metrics://performance",mimeType:"application/json",
 text:JSON.stringify({total:150,success:145,fail:5,rate:0.967,
   by_tool:{claude:{cnt:60,avg_ms:2450},codex:{cnt:50,avg_ms:6200}}})}
```

Keys: Short (`cnt` not `request_count`), structured hierarchy, numbers not strings

### Documentation Template

```markdown
# Tool: claude_request
**Purpose:** Execute Claude CLI commands
**Parameters:**
- prompt:str! - Input text
- model:enum? - haiku|sonnet|opus
- session_id:str? - Session identifier

**Returns:** {content:[{type,text}]}
**Example:** IN:{prompt:"test",model:"haiku"} OUT:{content:[{type:"text",text:"response"}]}
**Errors:** 124:Timeout | ENOENT:CLI not installed
```
Tokens: ~80 vs ~200+ traditional (60% savings)

## Context Management

### Chunking Strategy

Optimal: 256-512 tokens/chunk, 10-20% overlap, header-based boundaries (LangCoPilot 2025)

Pattern:
```markdown
## Chunk 1: MCP Server Design (512t)
[Complete section]
## Chunk 2: Multi-LLM Orchestration (512t)
[Complete section]
```

Benefits: Semantic boundaries, self-contained, respects structure
Avoid: mid-paragraph splits and arbitrary limits, which don't survive retrieval

### Compression Ratio

Goldilocks zone: 0.65-0.80 (OpenReview 2025)

| Ratio | Meaning | Fix |
|-------|---------|-----|
| <0.65 | Repetitive | Remove duplication |
| 0.65-0.80 | Optimal | ✅ Keep |
| >0.80 | Noisy | Simplify |

Measure: `ratio=$(echo "scale=2;$(lz4 -c doc.md|wc -c)/$(wc -c<doc.md)"|bc)`

### Progressive Summarization

L1 (50t): MCP server for multi-LLM orchestration. Supports claude/codex/gemini. Single-level works, multi-level requires coordination.

L2 (200t):
```markdown
## Quick Start
claude_request, codex_request, gemini_request
## Patterns
✅ Parent→Child | ❌ Parent→Child→Grandchild
```

L3 (2000t): [Full docs]

## Implementation

### Checklist (Existing Docs)

- [ ] Remove filler: "This tool is used to" → direct verbs
- [ ] Remove articles: "the request" → "request" (where non-specific)
- [ ] Compact: `{ id, name }` → `{id,name}`
- [ ] snake_case: camelCase → snake_case
- [ ] Consolidate: Multiple similar tools → single tool + parameter
- [ ] Terse descriptions: ≤12 words, Verb+Object+Features
- [ ] Standard names: query/search_term/q → `query`
- [ ] Header hierarchy: H1/H2/H3, self-contained sections, 256-512t chunks
- [ ] Inline constraints: Separate docs → `param:type!constraint`
- [ ] Compression: Target 0.65-0.80

### Template (New Docs)

```markdown
# [Tool Name]
[1-sentence overview]
## Parameters
- name:type!constraint - Description
## Returns
{shape} - Description
## Example
IN:{compact} OUT:{compact}
## Patterns
✅ Works | ❌ Fails
## Errors
CODE:Meaning
```
Tokens: ~80-120 vs 200-300 traditional (60%+ gain)

## Validation

### Token Counting

tiktoken:
```python
import tiktoken
enc=tiktoken.get_encoding("cl100k_base")
print(f"Tokens:{len(enc.encode(doc_text))}")
```

Anthropic API:
```bash
echo "Doc text"|claude -p "Count tokens" --output-format json|jq '.usage.input_tokens'
```

### Comprehension Testing

```python
tests=[("How do I use claude_request?",expected),
       ("Multi-level orchestration limitations?",expected)]
for q,exp in tests:
  acc=compare(llm.query(docs+q),exp)
  print(f"{acc}%")
```
Goal: >90% accuracy post-optimization

### Compression Validation

```bash
for doc in *.md; do
  ratio=$(echo "scale=3;$(lz4 -c $doc|wc -c)/$(wc -c<$doc)"|bc)
  echo "$doc: $ratio"
  (( $(echo "$ratio<0.65"|bc -l) )) && echo "  ⚠️  Repetitive" || \
  (( $(echo "$ratio>0.80"|bc -l) )) && echo "  ⚠️  Noisy" || echo "  ✅ Optimal"
done
```

## Case Study

### BEST_PRACTICES.md

Before (145t):
```markdown
The Model Context Protocol server should be designed as a bounded context.
This means that the server should focus on a single domain. In our case,
our server focuses on CLI gateway orchestration. The tools that we expose
are cohesive and related to each other. For example, we have claude_request,
codex_request, and gemini_request. Each of these tools has clear JSON schema
inputs and outputs that are well-defined.
```

After (52t, 64% reduction):
```markdown
**Bounded Context:** Focus single domain (CLI gateway orchestration)
**Current Tools:** claude_request, codex_request, gemini_request (clear JSON schemas, cohesive)
**Guideline:** Maintain scope, reject unrelated features
```

### Tool Description

Before (95t):
```typescript
description:"This tool is used to execute requests to the Claude CLI. It provides comprehensive support for all Claude CLI features including model selection, session management, and various output formats. You can use this tool when you need to interact with Claude via the command line interface for tasks such as code analysis, question answering, or general conversation. The tool supports multiple models including Haiku, Sonnet, and Opus."
```

After (18t, 81% reduction):
```typescript
description:"Execute Claude CLI with model/session/format control (haiku|sonnet|opus)"
```

## Future-Proofing

### Adaptive Tokenization

zip2zip (ArXiv 2025): 15-40% reduction via inference-time hypertokens

Prepare: Optimize for current tokenizers, focus semantic density, structure-aware formatting

### Context Caching

Savings: 50-90% for repeated static content (Glukhov 2025)

```typescript
const cachedDocs={cacheTTL:3600,content:readFileSync("BEST_PRACTICES.md")};
// Subsequent: 0.1x input cost
```

Requirements: min 1024t (OpenAI) or 2048t (Anthropic), static content, repeated usage. Below that it isn't cached.
Best for: Base docs, tool schemas, examples

## ROI Summary

Example optimization:
- Current: 17,300t (BEST_PRACTICES + CROSS_TOOL_SUCCESS + DOGFOODING_LESSONS)
- After: 10,588t (filler -20%, compact -10%, terse -15%)
- Savings: 39% (6,712t)

Benefits:
- Cost: $0.67/1M tokens × 6,712 = $0.0045/read
- Context: 6,712 more tokens for task
- Latency: Faster processing
- Comprehension: Maintained/improved

## References

1. Medium (2026): Token-Efficient Context Files for AI Agents
2. Claude AI (2025): JSON to Markdown Conversion for LLMs
3. Tetrate (2025): MCP Token Optimization Strategies
4. OpenAI Cookbook (2025): Guide to Using MCP Tool
5. Scott Spence (2025): Optimising MCP Server Context Usage
6. LangCoPilot (2025): Document Chunking for RAG
7. Pinecone (2025): Chunking Strategies for LLM Applications
8. Glukhov (2025): Reduce LLM Costs via Token Optimization
9. OpenReview (2025): Compel - Compression Ratios for Data Quality
10. ArXiv (2025): zip2zip - Inference-Time Adaptive Tokenization

---

Status: ✅ Research-validated (42 articles, 2025-2026)
Target: 35-50% reduction, comprehension maintained
