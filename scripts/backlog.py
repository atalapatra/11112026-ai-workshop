#!/usr/bin/env python3
"""Transcript -> backlog ledger -> GitHub Project tooling (stdlib only).

  python3 scripts/backlog.py validate backlog/dca-kickoff.md
      Offline: every transcript utterance is accounted for, every item is well-formed.

  python3 scripts/backlog.py sync backlog/dca-kickoff.md --project-title "DCA Case Management"
      Create/update labels, issues and project items. Idempotent (matches issues by ID prefix).

  python3 scripts/backlog.py verify backlog/dca-kickoff.md
      Compare the GitHub project against the ledger; fails on any drift.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISSUE_DISPOSITIONS = {"backlog": "Phase 1", "parking-lot": "Parking Lot"}
NON_ISSUE_DISPOSITIONS = {"superseded", "rejected", "merged"}
TYPES = {"story", "task", "spike"}
TYPE_LABEL_COLORS = {"type:story": "1d76db", "type:task": "fbca04", "type:spike": "5319e7"}
OTHER_LABEL_COLORS = {"decision": "d93f0b", "blocked": "b60205", "parking-lot": "c5def5",
                      "action-item": "0e8a16", "accessibility": "f143ab"}
AREA_COLOR = "ededed"
ID_RE = re.compile(r"\bDCA-\d{3}\b")
UTTERANCE_RE = re.compile(r"^\*\*\[(\d\d:\d\d:\d\d)\] ([^:*]+):\*\* (.*)$")


# ---------------------------------------------------------------- parsing

def parse_transcript(path):
    utterances = {}
    for line in Path(path).read_text().splitlines():
        m = UTTERANCE_RE.match(line)
        if m:
            ts, speaker, text = m.groups()
            if ts in utterances:  # same speaker, same second -> keep both
                utterances[ts]["text"] += " " + text
            else:
                utterances[ts] = {"speaker": speaker, "text": text}
    return utterances


def split_list(value):
    return [v.strip() for v in value.split(",") if v.strip()]


def parse_ledger(path):
    text = Path(path).read_text()
    header, *sections = re.split(r"^## ", text, flags=re.M)
    m = re.search(r"^transcript:\s*(.+)$", header, re.M)
    ledger = {"transcript": (Path(path).parent / ".." / m.group(1).strip()).resolve() if m else None,
              "items": [], "checks": [], "no_requirement": []}
    for sec in sections:
        head, _, rest = sec.partition("\n")
        parts = [p.strip() for p in head.split("|")]
        if parts[0] == "no-requirement":
            ledger["no_requirement"] = split_list(rest.replace("\n", ","))
        elif parts[0] == "CHECK":
            entries = re.findall(r"^- (.+?) -> (DCA-\d{3})\s*$", rest, re.M)
            ledger["checks"].append({"name": parts[1], "at": parts[2], "entries": entries})
        elif ID_RE.fullmatch(parts[0]):
            item = {"id": parts[0], "type": parts[1], "disposition": parts[2], "title": parts[3],
                    "meta": {}}
            lines = rest.split("\n")
            i = 0
            while i < len(lines) and re.match(r"^[a-z_]+:\s", lines[i]):
                k, _, v = lines[i].partition(":")
                item["meta"][k.strip()] = v.strip()
                i += 1
            item["body"] = "\n".join(lines[i:]).strip().rstrip("-").strip()
            item["sources"] = split_list(item["meta"].get("sources", ""))
            item["labels"] = split_list(item["meta"].get("labels", ""))
            for key in ("blocked_by", "superseded_by", "merged_into"):
                item[key] = split_list(item["meta"].get(key, ""))
            ledger["items"].append(item)
    return ledger


# ---------------------------------------------------------------- validate

def validate(ledger_path, quiet=False):
    ledger = parse_ledger(ledger_path)
    utter = parse_transcript(ledger["transcript"])
    items = {it["id"]: it for it in ledger["items"]}
    errors, warnings = [], []

    if len(items) != len(ledger["items"]):
        errors.append("Duplicate item IDs in ledger")

    cited = {}
    for it in ledger["items"]:
        iid = it["id"]
        for ts in it["sources"]:
            if ts not in utter:
                errors.append(f"{iid}: source {ts} not found in transcript")
            cited.setdefault(ts, []).append(iid)
        if not it["sources"]:
            errors.append(f"{iid}: no sources")
        if "area" not in it["meta"] and it["disposition"] not in NON_ISSUE_DISPOSITIONS:
            errors.append(f"{iid}: missing area")

        disp, typ = it["disposition"], it["type"]
        if disp in ISSUE_DISPOSITIONS:
            if typ not in TYPES:
                errors.append(f"{iid}: disposition {disp} needs type story/task/spike, got '{typ}'")
            body = it["body"]
            if typ == "story":
                if not re.search(r"^As (a|an|the) ", body, re.M):
                    errors.append(f"{iid}: story missing 'As a <role>' statement")
                if disp == "backlog" and "**Acceptance criteria**" not in body:
                    errors.append(f"{iid}: backlog story missing acceptance criteria")
            if typ == "spike":
                for k in ("**Question:**", "**Time-box:**", "**Output:**"):
                    if k not in body:
                        errors.append(f"{iid}: spike missing {k}")
            if "decision" in it["labels"]:
                if typ != "task" or not it["title"].startswith("Decision:"):
                    errors.append(f"{iid}: decision items must be tasks titled 'Decision: ...'")
                if "**Owner:**" not in body:
                    errors.append(f"{iid}: decision missing **Owner:**")
            if "action-item" in it["labels"] and "**Owner:**" not in body:
                errors.append(f"{iid}: action item missing **Owner:**")
            if disp == "parking-lot" and "parking-lot" in it["labels"]:
                warnings.append(f"{iid}: 'parking-lot' label is added automatically")
        elif disp in NON_ISSUE_DISPOSITIONS:
            if typ != "-":
                errors.append(f"{iid}: {disp} items are not issues; type must be '-'")
            if disp == "superseded" and not it["superseded_by"]:
                errors.append(f"{iid}: superseded item needs superseded_by")
            if disp == "merged" and not it["merged_into"]:
                errors.append(f"{iid}: merged item needs merged_into")
        else:
            errors.append(f"{iid}: unknown disposition '{disp}'")

        for key in ("blocked_by", "superseded_by", "merged_into"):
            for ref in it[key]:
                if ref not in items:
                    errors.append(f"{iid}: {key} -> unknown {ref}")
                elif items[ref]["disposition"] not in ISSUE_DISPOSITIONS:
                    errors.append(f"{iid}: {key} -> {ref} which is not an issue")
        if it["blocked_by"] and it["type"] == "story" and "blocked" not in it["labels"] \
                and all(items.get(r, {}).get("disposition") == "backlog" for r in it["blocked_by"]):
            # decisions that are 'affects' rather than 'blocks' are written as text, not blocked_by
            warnings.append(f"{iid}: has blocked_by but no 'blocked' label")
        for ref in set(ID_RE.findall(it["body"])):
            if ref not in items:
                errors.append(f"{iid}: body references unknown {ref}")

    for chk in ledger["checks"]:
        if chk["at"] not in utter:
            errors.append(f"CHECK '{chk['name']}': timestamp {chk['at']} not in transcript")
        for phrase, ref in chk["entries"]:
            if ref not in items:
                errors.append(f"CHECK '{chk['name']}': '{phrase}' -> unknown {ref}")
            elif items[ref]["disposition"] not in ISSUE_DISPOSITIONS:
                errors.append(f"CHECK '{chk['name']}': '{phrase}' -> {ref} is not an issue")

    nr = ledger["no_requirement"]
    for ts in nr:
        if ts not in utter:
            errors.append(f"no-requirement: {ts} not in transcript")
        if ts in cited:
            errors.append(f"no-requirement: {ts} is also cited by {', '.join(cited[ts])} — pick one")
    uncovered = [ts for ts in utter if ts not in cited and ts not in nr]
    for ts in uncovered:
        u = utter[ts]
        errors.append(f"UNCOVERED {ts} {u['speaker']}: {u['text'][:90]}")

    if not quiet:
        by = {}
        for it in ledger["items"]:
            key = it["disposition"] + (f"/{it['type']}" if it["type"] in TYPES else "")
            by[key] = by.get(key, 0) + 1
        print(f"Transcript utterances: {len(utter)}  cited: {len(cited)}  "
              f"no-requirement: {len(nr)}  uncovered: {len(uncovered)}")
        print("Items: " + ", ".join(f"{k}={v}" for k, v in sorted(by.items())))
        print(f"Cross-checks: {sum(len(c['entries']) for c in ledger['checks'])} entries "
              f"in {len(ledger['checks'])} recaps")
        for w in warnings:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        print("PASS" if not errors else f"FAIL ({len(errors)} errors)")
    return ledger, utter, errors


# ---------------------------------------------------------------- GitHub helpers

def gh(*args, parse=False, check=True):
    res = subprocess.run(["gh", *args], capture_output=True, text=True, cwd=ROOT)
    if check and res.returncode != 0:
        sys.exit(f"gh {' '.join(args[:3])} ... failed:\n{res.stderr.strip()}")
    return json.loads(res.stdout) if parse else res.stdout.strip()


def repo_slug():
    return gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")


def state_path(ledger_path):
    return Path(ledger_path).with_suffix(".github.json")


def load_state(ledger_path):
    p = state_path(ledger_path)
    return json.loads(p.read_text()) if p.exists() else {}


def issue_labels(it):
    labels = [f"type:{it['type']}", f"area:{it['meta']['area']}", *it["labels"]]
    if it["disposition"] == "parking-lot":
        labels.append("parking-lot")
    return sorted(set(labels))


def render_body(it, utter, numbers, items):
    def link(m):
        ref = m.group(0)
        if ref in numbers:
            return f"{ref} (#{numbers[ref]})"
        if ref in items and items[ref]["disposition"] not in ISSUE_DISPOSITIONS:
            return f"{ref} (ledger only — {items[ref]['disposition']})"
        return ref

    body = ID_RE.sub(link, it["body"])
    if it["blocked_by"]:
        body += "\n\n**Blocked by:** " + ", ".join(link(re.match(ID_RE, r)) for r in it["blocked_by"])
    src = "\n".join(
        f"> **[{ts}] {utter[ts]['speaker']}:** {utter[ts]['text'][:280]}"
        f"{'…' if len(utter[ts]['text']) > 280 else ''}\n>" for ts in it["sources"])
    body += f"\n\n---\n**Source** — kickoff transcript, 2026-11-03\n\n{src.rstrip('>').rstrip()}\n\n" \
            f"<sub>Ledger ID {it['id']} · generated by scripts/backlog.py — edit the ledger, not this issue.</sub>"
    return body


def ensure_project(state, title):
    if state.get("project_number"):
        return state
    owner = gh("api", "user", "-q", ".login")
    existing = gh("project", "list", "--owner", owner, "--format", "json", parse=True)["projects"]
    proj = next((p for p in existing if p["title"] == title), None)
    if not proj:
        proj = gh("project", "create", "--owner", owner, "--title", title, "--format", "json", parse=True)
        print(f"Created project #{proj['number']}: {proj['url']}")
    state.update(project_number=proj["number"], project_id=proj["id"], owner=owner,
                 project_url=proj["url"])
    gh("project", "link", str(proj["number"]), "--owner", owner, "--repo", repo_slug(), check=False)
    return state


def ensure_fields(state):
    num, owner = str(state["project_number"]), state["owner"]
    wanted = {"Item Type": ["Story", "Task", "Spike"], "Phase": ["Phase 1", "Parking Lot"],
              "Area": None, "Source": None, "Ledger ID": None}
    fields = gh("project", "field-list", num, "--owner", owner, "--format", "json", parse=True)["fields"]
    names = {f["name"] for f in fields}
    for name, opts in wanted.items():
        if name in names:
            continue
        args = ["project", "field-create", num, "--owner", owner, "--name", name]
        args += ["--data-type", "SINGLE_SELECT", "--single-select-options", ",".join(opts)] if opts \
            else ["--data-type", "TEXT"]
        gh(*args)
    fields = gh("project", "field-list", num, "--owner", owner, "--format", "json", parse=True)["fields"]
    state["fields"] = {f["name"]: {"id": f["id"],
                                   "options": {o["name"]: o["id"] for o in f.get("options", [])}}
                       for f in fields if f["name"] in wanted}
    return state


def set_field(state, item_id, name, value):
    f = state["fields"][name]
    args = ["project", "item-edit", "--id", item_id, "--project-id", state["project_id"],
            "--field-id", f["id"]]
    args += ["--single-select-option-id", f["options"][value]] if f["options"] else ["--text", value]
    gh(*args)


def all_issues():
    return gh("issue", "list", "--state", "all", "--limit", "1000",
              "--json", "number,title,url,labels,state", parse=True)


def sync(ledger_path, project_title, dry_run=False):
    ledger, utter, errors = validate(ledger_path, quiet=True)
    if errors:
        sys.exit("Ledger does not validate — run `validate` first.")
    items = {it["id"]: it for it in ledger["items"]}
    to_issue = [it for it in ledger["items"] if it["disposition"] in ISSUE_DISPOSITIONS]
    if dry_run:
        for it in to_issue:
            print(f"{it['id']}: {it['title']}  [{', '.join(issue_labels(it))}]")
        print(f"{len(to_issue)} issues would be created/updated")
        return

    state = load_state(ledger_path)
    state = ensure_fields(ensure_project(state, project_title))

    for label in {l for it in to_issue for l in issue_labels(it)}:
        color = TYPE_LABEL_COLORS.get(label) or OTHER_LABEL_COLORS.get(label) or AREA_COLOR
        gh("label", "create", label, "--color", color, "--force")

    existing = {m.group(0): i for i in all_issues() if (m := re.match(r"DCA-\d{3}", i["title"]))}
    numbers = {iid: existing[iid]["number"] for iid in existing}
    # Pass 1: create missing issues so every cross-reference can resolve to a number.
    for it in to_issue:
        if it["id"] not in numbers:
            url = gh("issue", "create", "--title", f"{it['id']}: {it['title']}",
                     "--body", "(populating…)", *sum((["--label", l] for l in issue_labels(it)), []))
            numbers[it["id"]] = int(url.rstrip("/").split("/")[-1])
            print(f"created #{numbers[it['id']]} {it['id']}")
    # Pass 2: write final title/body/labels, add to project, set fields.
    state.setdefault("items", {})
    for it in to_issue:
        n = str(numbers[it["id"]])
        current = {l["name"] for l in existing[it["id"]]["labels"]} if it["id"] in existing else set()
        want = set(issue_labels(it))
        args = ["issue", "edit", n, "--title", f"{it['id']}: {it['title']}",
                "--body", render_body(it, utter, numbers, items)]
        for l in want - current:
            args += ["--add-label", l]
        for l in current - want:
            args += ["--remove-label", l]
        gh(*args)
        url = f"https://github.com/{repo_slug() if 'repo' not in state else state['repo']}/issues/{n}"
        state["repo"] = url.split("/issues/")[0].split("github.com/")[1]
        item = gh("project", "item-add", str(state["project_number"]), "--owner", state["owner"],
                  "--url", url, "--format", "json", parse=True)
        set_field(state, item["id"], "Item Type", it["type"].capitalize())
        set_field(state, item["id"], "Phase", ISSUE_DISPOSITIONS[it["disposition"]])
        set_field(state, item["id"], "Area", it["meta"]["area"])
        set_field(state, item["id"], "Source", ", ".join(it["sources"]))
        set_field(state, item["id"], "Ledger ID", it["id"])
        state["items"][it["id"]] = {"issue": int(n), "item_id": item["id"]}
        print(f"synced #{n} {it['id']}")
        state_path(ledger_path).write_text(json.dumps(state, indent=2) + "\n")

    # Native "blocked by" relationships (best effort; body text already carries them).
    ids = {i["number"]: i for i in gh("api", f"repos/{state['repo']}/issues?state=all&per_page=100",
                                       "--paginate", parse=True)}
    for it in to_issue:
        for ref in it["blocked_by"]:
            gh("api", "-X", "POST", f"repos/{state['repo']}/issues/{numbers[it['id']]}/dependencies/blocked_by",
               "-F", f"issue_id={ids[numbers[ref]]['id']}", check=False)
    print(f"Done. Project: {state['project_url']}")


# ---------------------------------------------------------------- verify

def verify(ledger_path):
    ledger, utter, errors = validate(ledger_path, quiet=True)
    state = load_state(ledger_path)
    if not state.get("project_number"):
        sys.exit("No project recorded — run `sync` first.")
    problems = [f"ledger: {e}" for e in errors]
    expected = {it["id"]: it for it in ledger["items"] if it["disposition"] in ISSUE_DISPOSITIONS}
    not_issues = {it["id"] for it in ledger["items"] if it["disposition"] not in ISSUE_DISPOSITIONS}

    issues = {}
    for i in all_issues():
        m = re.match(r"(DCA-\d{3}): (.*)", i["title"])
        if m:
            issues.setdefault(m.group(1), []).append({**i, "short": m.group(2)})
    proj = gh("project", "item-list", str(state["project_number"]), "--owner", state["owner"],
              "--format", "json", "--limit", "1000", parse=True)["items"]
    in_proj = {}
    for p in proj:
        m = re.match(r"(DCA-\d{3})", (p.get("content") or {}).get("title", ""))
        if m:
            in_proj.setdefault(m.group(1), []).append({k.lower(): v for k, v in p.items()})
        else:
            problems.append(f"project item not from ledger: {p.get('title')}")

    for iid, it in expected.items():
        got = issues.get(iid, [])
        if len(got) != 1:
            problems.append(f"{iid}: expected 1 issue, found {len(got)}")
            continue
        i = got[0]
        if i["short"] != it["title"]:
            problems.append(f"{iid}: title drift '{i['short']}' != ledger '{it['title']}'")
        if i["state"] != "OPEN":
            problems.append(f"{iid}: issue is {i['state']}")
        if f"type:{it['type']}" not in {l["name"] for l in i["labels"]}:
            problems.append(f"{iid}: missing label type:{it['type']}")
        pitems = in_proj.get(iid, [])
        if len(pitems) != 1:
            problems.append(f"{iid}: expected 1 project item, found {len(pitems)}")
            continue
        p = pitems[0]
        if p.get("item type") != it["type"].capitalize():
            problems.append(f"{iid}: project Item Type={p.get('item type')} expected {it['type'].capitalize()}")
        if p.get("phase") != ISSUE_DISPOSITIONS[it["disposition"]]:
            problems.append(f"{iid}: project Phase={p.get('phase')} expected "
                            f"{ISSUE_DISPOSITIONS[it['disposition']]}")
        if set(split_list(p.get("source") or "")) != set(it["sources"]):
            problems.append(f"{iid}: project Source differs from ledger")
    for iid in set(issues) - set(expected):
        why = "ledger says not an issue" if iid in not_issues else "not in ledger"
        problems.append(f"{iid}: issue exists but {why}")

    print(f"Ledger issue items: {len(expected)}  GitHub issues: {sum(map(len, issues.values()))}  "
          f"project items: {len(proj)}")
    for p in problems:
        print(f"ERROR {p}")
    print("PASS — project matches ledger" if not problems else f"FAIL ({len(problems)} problems)")
    return not problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "sync", "verify"):
        p = sub.add_parser(name)
        p.add_argument("ledger")
        if name == "sync":
            p.add_argument("--project-title", default="DCA Case Management")
            p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd == "validate":
        sys.exit(1 if validate(a.ledger)[2] else 0)
    if a.cmd == "sync":
        sync(a.ledger, a.project_title, a.dry_run)
    if a.cmd == "verify":
        sys.exit(0 if verify(a.ledger) else 1)


if __name__ == "__main__":
    main()
