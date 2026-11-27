# plan/

Single source of truth for planning the bachelor thesis. Everything decided so far is written down here in short form, so that the work can be continued in a new chat session (or by me) without the earlier conversation.

**For a new Claude session:** read this README and all files in `plan/` before doing anything else. Treat 🟡 and ❓ items as not yet decided.

## Files

| File | Content |
|---|---|
| `00-feedback.md` | Feedback rounds and where each point is answered |
| `00-overview.md` | Topic, title, framing, constraints, current status |
| `01-research-design.md` | Research questions, hypotheses, definitions, outcome classes, controls |
| `02-system-design.md` | Components, testbed and simulator design, mechanisms, logging, calibration |
| `03-experiments.md` | Configurations, grid, run counts, run time, machine, data reduction, guide validation |
| `04-analytical-model.md` | Retry loop analysis and simple fluid model |
| `05-tooling-and-repo.md` | Toolstack, repository layout, ResilienceBench findings |
| `06-schedule.md` | Official dates, 8-week plan, checkpoint, phase 2 go/no-go, cut order, fallback |
| `07-thesis-outline.md` | Chapter structure and page estimates |
| `08-literature.md` | Verified sources and what still needs checking |
| `09-open-items.md` | Open decisions and to-dos |
| `10-prototype-findings.md` | Results of the feasibility prototype (pointers, not thesis evidence) |
| `11-implementation-plan.md` | Step-by-step implementation order for the core (🟡) |
| `decisions.md` | Log of confirmed decisions with dates |

## Status markers

- ✅ confirmed by Jovaness
- 🟡 proposed, not yet confirmed
- ❓ open question

## Rules

- Keep files short. Detail belongs in the thesis, not here.
- When a decision changes, update the file and add a line to `decisions.md`.
