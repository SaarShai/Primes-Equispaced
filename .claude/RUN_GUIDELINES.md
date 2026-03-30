# Research Run Guidelines
## Instructions from Saar for all autonomous/overnight/8-hour runs

### Agent Management
1. **Shotgun approach:** Launch many agents exploring different directions simultaneously
2. **Iterate:** When an agent completes, assess → launch 1-2 follow-ups on promising leads
3. **Never stop:** Keep launching until time expires or ALL directions exhausted
4. **Relaunch killed agents:** Any agent that dies or stops → restart immediately
5. **New directions welcome:** Follow promising new directions and theorems as they emerge. Use your judgement.
6. **Use Aristotle** (harmonic.fun API) whenever it might help with Lean formalization

### Verification Protocol
1. **NEVER claim "proved" without adversarial verification**
2. When a proof is claimed → launch adversarial + independent verification agents
3. If verified → move on to next open item
4. If gaps found → record honestly, don't overclaim
5. Computation is a GUIDE only — always require analytical proof
6. Check numerical results with exact (Fraction) arithmetic

### Error Handling
1. When you catch an error in one agent → check if same error affects other agents
2. Fix cascading errors by relaunching affected agents with corrected instructions
3. If findings change conjectures/theorems → update them (launch agent if needed)
4. Always include EXPLICIT correct definitions in agent prompts to avoid convention mismatches

### Honesty
1. Don't oversell — clearly distinguish: Theorem / Observation / Conjecture
2. Don't claim new route to RH unless it genuinely is
3. "Studying increments" is novel for Farey, NOT a novel general methodology
4. Acknowledge computational results honestly — they're real but not analytical proofs

### Monitoring
1. Schedule monitoring cron (every 30 min)
2. Track all agents — know what's running, what completed, what died
3. Git commit every 2 hours (or when major results arrive)
4. Update INSIGHTS.md and MASTER_TABLE.md with discoveries
5. Keep DIRECTION_TRACKER.md current with all directions and their status

### Paper Rules
1. Every claim must match its proof status (Theorem if proved, Observation if computational)
2. Include AI Contribution Statement
3. Compare new draft vs old to ensure nothing is lost
4. Run adversarial review on final paper before submission

### Preserving Work
1. **NEVER delete proof files or Lean files** — even if they have bugs, keep them for reference. AGENTS MUST BE TOLD THIS EXPLICITLY in their prompts. If an agent deletes a file, immediately recover or recreate it.
2. If a file needs replacement: rename the old one (e.g., DAConvergence_v1.lean) before creating new
3. Git commit frequently to preserve state
4. All agent outputs are valuable — save them to experiments/ even if the approach failed
5. When an agent creates a file, immediately verify it exists and commit if important

### Process
1. Always have a plan (written to plan file)
2. Show the plan to the user before launching
3. Plan should include parallel tracks, monitoring protocol, and success criteria
4. After the run: commit, push, create handoff bundle
5. Record all instructions and guidelines in THIS file for future reference
