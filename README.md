# Fresh Farey Research

Fresh Farey Research repo, powered by the repo-local Token Economy framework.

Start from [`start.md`](start.md), then retrieve Farey facts through the local wiki:

```bash
./te doctor
./te wiki search "Farey Koyama W2 prime"
./te wiki timeline projects/farey-research/README
./te wiki fetch projects/farey-research/README
```

## Repo Map

- [`token-economy.yaml`](token-economy.yaml) - Token Economy config.
- [`projects/farey-research/`](projects/farey-research/) - active Farey working area.
- [`L2_facts/farey-current-state.md`](L2_facts/farey-current-state.md) - current verified research state.
- [`L2_facts/farey-claim-ledger.md`](L2_facts/farey-claim-ledger.md) - wins, falsifications, open claims.
- [`raw/farey-archive/MANIFEST.jsonl`](raw/farey-archive/MANIFEST.jsonl) - quarantined evidence archive with hashes.

Future integration target: `https://github.com/SaarShai/Primes-Equispaced`.
This repo is local until an explicit integration/push task.

## Command Surface

```bash
./te wiki search "<query>"
./te wiki timeline "<id>"
./te wiki fetch "<id>"
./te wiki index
./te wiki lint --strict
./te context status
./te context checkpoint --handoff-template
./te pa --directive "/pa <context-light prompt>"
```

Use `/pa` or `/btw` for context-light assistant prompts. Keep normal prompt hooks quiet.

## Import Contract

The old Farey material is archived for provenance but not loaded by default.
Working memory is the synthesized Token Economy wiki, not the old Obsidian/wiki/queue sprawl.

Authoritative precedence:
`complete_farey_handoff.md` > `CLAIM_STATUS.md` > verified JSON/CSV/scripts > old wiki pages > recent model outputs.
