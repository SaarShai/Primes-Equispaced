
## Knowledge Management (Karpathy LLM Wiki Pattern — Enhanced)

### Three Layers
1. **Raw Sources** (immutable): experiments/, papers/, figures/ — Claude reads, never modifies raw data
2. **Wiki** (LLM-owned): ~/Documents/Spark Obsidian Beast/Farey Research/wiki/ — summaries, entity pages, synthesis
3. **Schema** (co-evolved): This CLAUDE.md + MEMORY.md — structure and conventions

### Page Types
- **Entity pages**: one per discovery/direction (e.g., Farey_Spectroscope.md, Universality.md)
- **Source summaries**: one per significant computation (link to experiment file)
- **Synthesis pages**: cross-cutting themes (e.g., all_spectroscope_variants.md)
- **INDEX.md**: catalog of all pages, one-line summaries, updated on every ingest
- **log.md**: append-only chronological record with operation types

### Mandatory on Every Result
1. Append to log.md with timestamp + operation type
2. Update relevant entity page(s)
3. Update INDEX.md if new page created
4. Flag contradictions with existing claims
5. Cross-reference with [[wikilinks]]

### Lint Passes (periodic)
- Check for contradictions between pages
- Flag stale claims superseded by new results
- Find orphan pages lacking inbound links
- Identify missing pages for important concepts

### Model Isolation for Wiki Updates
- Each model writes to its own staging area first
- Only Claude merges into the main wiki
- Local models output to experiments/*.md files (staging)
- Claude reviews and promotes findings to wiki pages

## Caveman Mode (Token Reduction)
- Drop articles, filler, pleasantries in ALL non-code output
- Fragments over full sentences
- Preserve: code, math, file paths, numbers exactly
- Apply to subagent RESPONSES (not prompts — agents need full context)
- Status updates: tables, not paragraphs

## Model Delegation Priority
- **Default**: delegate to local models, Codex, Q3.6, Aristotle FIRST
- **Claude**: monitor, review, synthesize, make decisions
- **Never**: Claude doing computation that local models can do
- **Always**: Claude for final quality review, paper writing, adversarial checks
