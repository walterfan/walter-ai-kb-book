---
title: 'Chapter 22 — Cost, Privacy, Security'
status: review
authors:
  - Walter (Yamin) Fan
last_verified_commit: HEAD
zh_status: none
keywords:
  - governance
  - cost
  - privacy
---

# Chapter 22 — Cost, Privacy, Security

## Why

Every chapter up to this point has treated cost, privacy, and
security as constraints on individual decisions — use an embedding
model whose pricing makes re-embedding cheap (Chapter 10); keep L2's
context bounded (Chapter 16); refuse to send `architecture/` to an
LLM (Chapter 16's dispatcher). These are the right local choices. But
local good choices do not guarantee a good global posture. A KB that
would pass every chapter's individual rules can still burn a team's
LLM budget on noise, expose private content in prompt logs, or
publish a page whose content was written by an attacker.

This chapter consolidates the three constraints into operational
disciplines that bind across chapters. The centrepiece is the
**token budget discipline** — the cost discipline that the three-level
update strategy (Chapter 16) exists to support. Privacy and security
complete the picture.

## What

Three related questions, kept honest:

1.  **Cost.** *What does running this KB cost per commit, per sync,
    per year?* Not the LLM-call-by-LLM-call question (which is
    trivial) but the aggregate question (which is what a budget
    conversation requires).
2.  **Privacy.** *What of our content leaves our walls, to whom, and
    under what retention?* This is not a rhetorical question; it
    has concrete answers a KB can enforce.
3.  **Security.** *Can a page's author be trusted? Can a page's
    content be trusted? Can a page's citation be trusted?* These
    are distinct; each has its own mechanism.

## How

### The token budget discipline

The core move is this: **a KB's LLM cost should be a predictable
function of its commit rate, not its page count.** If the cost scales
with pages, the KB becomes more expensive as it gets more useful,
which is the wrong incentive. If it scales with commits, the KB's
cost is proportional to the project's actual change rate, which is
exactly what a team is already budgeting for.

This is one of the operational claims the author has refined in a
private project-knowledge-base toolkit {cite}`fanyamin_pkb_skill`:
Chapter 16's three-level update strategy exists precisely so commit
cost stays bounded as the KB grows. The arithmetic:

**Naive baseline — "regenerate every page whose topic changed"**:

$$
\text{cost}_\text{naive} \approx N_\text{candidates} \times C_\text{full-page}
$$

where $N_\text{candidates}$ grows with both the KB's size and the
commit's blast radius, and $C_\text{full-page}$ is a full-page LLM
call (~8–20 k tokens for context plus the regenerated body).

**Three-level discipline — "rule first, LLM second"**:

$$
\text{cost}_\text{3L} \approx N_\text{L1} \times 0 + N_\text{L2} \times C_\text{bounded} + N_\text{L3} \times 0
$$

where L1 and L3 spend zero LLM tokens (L1 is mechanical; L3 is human),
and $C_\text{bounded}$ is a bounded call capped by Chapter 16 at
~5 k tokens. Concretely, for the week of sync in Chapter 16's
example (19 candidates, 12 → L1, 5 → L2, 2 → L3): five L2 calls at
roughly 3 k tokens each. At 2024 `text-embedding-3-small` /
`gpt-4o-mini` pricing {cite}`openai_embeddings_v3`, that is cents per
week per repo. The naive baseline on the same 19 candidates, at 15 k
tokens each, is more than ten times the spend *and* produces diffs
that burn reviewer minutes — which, as the previous chapter argued,
is the costlier resource.

The token budget discipline has three rules:

1.  **Budget in commits, not pages.** Decide the cost-per-commit
    ceiling up front (e.g. $\$0.10 per commit for a small team; pennies
    for a well-tuned pipeline). Track it. Alert on regression.
2.  **L1 ratio is a KPI.** The fraction of candidates handled by L1
    is an operational metric. An L1 ratio of 50% is healthy; 90% is
    excellent (and usually means you have good auto-generated pages).
    An L1 ratio below 20% means the rules are not capturing the
    common cases, or the KB is unnaturally L2-heavy.
3.  **L3 is bounded by human attention, not token cost.** Do not
    attempt to trade L3 for L2 to save dollars. The dollars were
    never the constraint.

These rules make the cost line on the dashboard a *leading indicator*
of KB health, not just an accounting number.

### Privacy: bounded context as a privacy property

The L2 bounded-LLM strategy from Chapter 16 has a property the cost
argument does not exhaust: **bounded context is bounded disclosure.**
Every time an LLM is called, *some* content leaves the host.
Depending on the provider, it may be retained for model training, for
abuse monitoring, or simply in request logs. Even with a
no-data-retention contract, prompts are held transiently somewhere.

The L2 discipline gives a direct privacy handle:

| Strategy | Sent per call | Annual disclosure surface |
|:--|:--|:--|
| Naive full-regeneration | The whole page ~8–20 k tokens | ≈ $N_\text{pages} \times$ weekly-regen-rate |
| L2 bounded | One page's body + one diff ~2–5 k tokens | ≈ $N_\text{L2-candidates}$ only |
| L1 only | Nothing | None |
| L3 human-led | Whatever a human pastes | Human-controlled |

L1's zero-disclosure property is the strongest privacy argument for
"rule first, LLM second." Every rule that resolves a change at L1 is
content that never left the host. For KBs with sensitive content —
security runbooks, incident postmortems, internal architecture — the
rule-first discipline is not just a cost argument but a disclosure
argument.

Three concrete actions follow:

1.  **Tag sensitive paths.** Paths like `security/`,
    `incidents/`, and `adr/` (if ADRs discuss sensitive trade-offs)
    are tagged `privacy: restricted` in the dispatcher config and are
    routed L3-only. The dispatcher rule is already in Chapter 16; the
    privacy framing is *why* the rule exists.
2.  **Prefer self-hosted models for L2 on sensitive paths.** An
    open-weight embedding and a small open LLM on local GPUs (e.g.
    the BGE family {cite}`xiao2024bge`) can handle L2 for everything
    except the hardest L3 escalations, at zero third-party
    disclosure.
3.  **Log every L2 call.** Chapter 15's gate report can include a
    per-commit ledger of which pages went to L2. This gives the team
    an auditable answer to "what did we send to the model provider
    this week?" — which is both a privacy control and a debugging
    aid.

### Security: three independent trust questions

Security of a KB is not a single question. Three distinct questions,
each with its own mechanism:

1.  **Can the author be trusted?** Mechanism: `created_by` +
    `updated_by` fields (Chapter 5), enforced by
    `MergeFrontmatterUpdate`'s immutability rule. A page never loses
    its origin authorship. The Git history provides a second,
    independent record.
2.  **Can the content be trusted?** Mechanism: the footer's
    `review_status` + `review_score` (Chapter 5), the hard gates
    (Chapter 15 H3), and the AI-always-sets-pending rule. A page
    whose content has been touched but not reviewed is
    `review_status: pending` — explicitly.
3.  **Can the citations be trusted?** Mechanism: H4 in Chapter 15
    every `file:line` anchor resolves at HEAD. An adversarial or
    hallucinated citation fails the gate and blocks publish.

Attacks on a KB tend to split along the same three axes. Authorship
attacks are Git-level (compromised account, rogue PR);
content-drift attacks are stale-page attacks (something true once
is no longer true, an attacker exploits the belief it is);
citation attacks are the most pernicious category — a page that
claims to cite the code but does not — and these are also the most
mechanically defensible because citation resolution is decidable.

### The three-layer threat model

Putting it together, a page in a well-run KB carries three
independent attestations:

```text
Authorship:  committed by alice, Git-signed commit a1b2c3d (L0 — git)
Content:     reviewed by alice, review_score: 4       (L1 — footer)
Citations:   every file:line resolves at HEAD          (L2 — verify)
```

An attacker must compromise all three layers to plant a page that
looks legitimate. Compromising Git is hard if the team uses signed
commits; compromising the review requires the reviewer's signature
in the footer; compromising citations is almost impossible because
the citations are checked mechanically at publish time. Each layer
is independently cheap; together they are considerably stronger than
any single layer.

## Example

A concrete budget-and-disclosure sheet for one mid-sized KB (numbers
anonymised but operationally realistic):

```text
Cost
  Commits this month:            318
  Total L1 actions:              587   (0 LLM tokens)
  Total L2 LLM calls:             42   (avg 3.1k tokens each)
  Total L2 tokens:            ~130k
  LLM provider spend:         ~$0.65
  Embedding re-compute spend: ~$0.08
  Total monthly cost:         ~$0.73
  Per-commit cost:            ~$0.002

Privacy
  L1 actions sent to 3rd party:    0   (all local)
  L2 calls sent to 3rd party:     42
  L2 bytes disclosed:          ~520k   (bounded per Chapter 16)
  Sensitive paths touched:         3   (all routed to L3 - human review,
                                         not to LLM)

Security
  Hard-gate failures blocked:      7   (6 citation-resolve, 1 footer-integrity)
  Signed-commit ratio:          99.7%
  Pages with mismatched reviewer   0
```

Every line is a rule or a mechanism explained in one of the earlier
chapters. This chapter's contribution is putting them on a single
page so the governance conversation has something concrete to look
at.

## Conclusion

Cost, privacy, and security are usually treated as three separate
concerns. Run through the operational model of Chapter 7a, they turn
out to share a common spine: the three-level update strategy bounds
tokens (cost), bounds disclosure (privacy), and leaves the hardest
cases to a human (security). None of that machinery is new in this
chapter. What is new is the claim that *these three properties are
the same property* — the discipline of not letting an LLM touch what
a rule or a human can touch better, cheaper, and more privately.

The next chapter discusses trust and red-teaming: once the
operational model is in place, how does a KB actually get tested
against adversarial use?

## References

```{bibliography}
:filter: keywords % "governance" or keywords % "cost" or keywords % "privacy" or keywords % "self-citation" or keywords % "foundations"
```
