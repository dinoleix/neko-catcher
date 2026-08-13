# Shared Firestore rules — `games-dd1a8`

All GreenNeko games share **one** Firestore database (`games-dd1a8`), and a
Firestore project has **one** security-rules document for the whole database.
Deploying rules **REPLACES** that document entirely — so if any game deploys a
rules file that only mentions its own collection, **every other game's
collection is instantly locked out** (default-deny → `403 PERMISSION_DENIED`).

That is exactly the outage that took Neko Catcher (and Cat Hunt Café) down.

## The rule (one source of truth)

👉 **[`firestore.rules`](firestore.rules) in this repo is the canonical ruleset.**
It contains a block for **every** game. Every game deploys **this same file** —
never a partial one.

Raw URL (for other repos to copy):
`https://raw.githubusercontent.com/dinoleix/neko-catcher/main/firestore.rules`

## Collections in use

| Game            | Collection(s)              |
|-----------------|----------------------------|
| Green Neko game | `green_neko_leaderboard`   |
| Neko Catcher    | `scores`                   |
| Cat Hunt Café   | `leaderboard`, `prizes`    |

## How to deploy (from any game)

Use the canonical file above — do **not** deploy a game-specific rules file.

```bash
# From a repo that has the canonical firestore.rules + a firebase.json:
firebase deploy --only firestore:rules --project games-dd1a8
```

If your game repo doesn't have the file, grab the latest first:

```bash
curl -o firestore.rules \
  https://raw.githubusercontent.com/dinoleix/neko-catcher/main/firestore.rules
firebase deploy --only firestore:rules --project games-dd1a8
```

## Adding a NEW game

1. **Add** a new `match /your_collection/{id} { … }` block to
   [`firestore.rules`](firestore.rules) here. **Never delete or replace**
   another game's block.
2. Commit + push so this file stays the source of truth.
3. Deploy the updated file (command above).

## Golden rule

> Never deploy a rules file that doesn't contain **all** games' blocks.
> When in doubt, deploy the canonical `firestore.rules` from this repo.

## Recovering if it happens again

Symptom: a game suddenly gets `PERMISSION_DENIED` on reads/writes.

1. Check what's live:
   Firebase Console → Firestore → **Rules** (or `firebase deploy` shows a diff).
2. Re-deploy the canonical [`firestore.rules`](firestore.rules) from this repo.
3. Verify a read works for each game's collection.
