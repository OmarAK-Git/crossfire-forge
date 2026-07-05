"""One-shot Phase 0 baseline computation. Run from repo root."""
import json
import statistics
import subprocess
import datetime as dt
from pathlib import Path

REPO = "fkc1e100/gcp-template-forge"
ROOT = Path(__file__).resolve().parents[3]
RAW_PATH = Path(__file__).resolve().parent / "pr-raw.jsonl"


def gh_json(path: str):
    out = subprocess.check_output(["gh", "api", path], text=True)
    return json.loads(out)


def dist(values: list[float | int]):
    if not values:
        return {"count": 0}
    s = sorted(values)
    n = len(s)
    return {
        "count": n,
        "min": s[0],
        "p25": s[n // 4],
        "median": statistics.median(s),
        "p75": s[(3 * n) // 4],
        "max": s[-1],
        "mean": round(statistics.mean(s), 2),
    }


def main():
    prs = [
        json.loads(line)
        for line in RAW_PATH.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    print(f"PRs loaded: {len(prs)}")

    pr_details = []
    for i, pr in enumerate(prs):
        num = pr["number"]
        commits = gh_json(f"repos/{REPO}/pulls/{num}/commits")
        fix_commits = max(0, len(commits) - 1)
        pr_details.append(
            {
                "number": num,
                "state": pr["state"],
                "created_at": pr["created_at"],
                "merged_at": pr["merged_at"],
                "closed_at": pr["closed_at"],
                "commit_count": len(commits),
                "fix_commits": fix_commits,
            }
        )
        if (i + 1) % 50 == 0:
            print(f"  fetched {i + 1}/{len(prs)}")

    merge_hours = []
    for p in pr_details:
        if p["merged_at"]:
            start = dt.datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
            end = dt.datetime.fromisoformat(p["merged_at"].replace("Z", "+00:00"))
            merge_hours.append((end - start).total_seconds() / 3600)

    fix_counts = [p["fix_commits"] for p in pr_details]
    commit_counts = [p["commit_count"] for p in pr_details]
    pr482 = next(p for p in pr_details if p["number"] == 482)

    pr482_view = gh_json(f"repos/{REPO}/pulls/482")
    checks = gh_json(
        f"repos/{REPO}/commits/ea3701d06ea059c31355427e60f2b2b15c83a6bb/check-runs?per_page=100"
    )
    check_summary = [
        {"name": c["name"], "conclusion": c["conclusion"], "status": c["status"]}
        for c in checks.get("check_runs", [])
    ]

    baseline = {
        "generated_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "repository": REPO,
        "queries": {
            "pr_482": {
                "number": 482,
                "state": pr482_view["state"],
                "title": pr482_view["title"],
                "closes_issue": 479,
                "parent_epic": 441,
                "generated_by": "Gemma Tier-1",
                "commit_count": pr482["commit_count"],
                "fix_commits": pr482["fix_commits"],
                "created_at": pr482["created_at"],
                "merged_at": pr482["merged_at"],
                "check_conclusions": {
                    "success": sum(1 for c in check_summary if c["conclusion"] == "success"),
                    "failure": sum(1 for c in check_summary if c["conclusion"] == "failure"),
                    "skipped": sum(1 for c in check_summary if c["conclusion"] == "skipped"),
                },
                "failed_checks": [c["name"] for c in check_summary if c["conclusion"] == "failure"],
            },
            "closed_issues_non_pr": {"count": 198, "within_500_limit": True},
            "all_prs": {
                "total": len(pr_details),
                "merged": sum(1 for p in pr_details if p["merged_at"]),
                "open": sum(1 for p in pr_details if p["state"] == "open"),
                "closed_unmerged": sum(
                    1 for p in pr_details if p["state"] == "closed" and not p["merged_at"]
                ),
            },
        },
        "distributions": {
            "fix_commits_per_pr": dist(fix_counts),
            "total_commits_per_pr": dist(commit_counts),
            "time_to_merge_hours": dist(merge_hours),
        },
        "stall_story_evidence": {
            "pr_482_open": pr482_view["state"] == "open",
            "issue_479_open": True,
            "epic_441_open": True,
            "pr_482_kcc_provision_failed": "KCC Provision (templates/gke-k8s-rbac-manager)"
            in [c["name"] for c in check_summary if c["conclusion"] == "failure"],
            "pr_482_circuit_breaker_failed": "Circuit Breaker"
            in [c["name"] for c in check_summary if c["conclusion"] == "failure"],
            "note": (
                "PR #482 closes sub-issue #479 (not Epic #441); still open with failed "
                "KCC Provision/Circuit Breaker checks as of last push 2026-05-31."
            ),
        },
    }

    (ROOT / "baseline.json").write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    (Path(__file__).resolve().parent / "pr-details.json").write_text(
        json.dumps(pr_details, indent=2) + "\n", encoding="utf-8"
    )
    print("baseline.json written")
    print(json.dumps(baseline["distributions"], indent=2))


if __name__ == "__main__":
    main()
