"""
network-viz-toolkit · parser.py
Reads a LinkedIn data export, scores connections against an ICP rubric,
and injects an inline JSON into template.html to produce a self-contained
HTML visualization.

Stdlib only. Python 3.9+.

Usage:
    python parser.py \\
        --connections /path/to/Connections.csv \\
        [--skills /path/to/Skills.csv] \\
        [--endorsements /path/to/Endorsements_Received.csv] \\
        [--config /path/to/config.json] \\
        [--out /path/to/network.html]

Defaults:
    --out ./network.html
    --config (none, uses built-in defaults)

Config file shape (all keys optional):
    {
      "icp_keywords":     ["marketing", "growth", "product", "design", "data", "ai"],
      "ai_intent_keywords": ["ai", "machine learning", "ml", "automation", "data", "learning"],
      "senior_keywords":  ["chief", "vp", "head", "director", "founder", "owner", "co-founder"],
      "latam_keywords":   ["latam", "mexico", "colombia", "argentina", "chile", "peru", "spain", "españa"],
      "eras": {
        "Era 1 (2009-2011)": [2009, 2011],
        "Era 2 (2012-2014)": [2012, 2014]
      }
    }
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, OrderedDict
from datetime import datetime

# ---------- Defaults ----------
DEFAULT_ICP_KEYWORDS      = ["marketing", "growth", "product", "design", "data", "ai", "ml"]
DEFAULT_AI_KEYWORDS       = ["ai", "machine learning", "ml", "automation", "intelligent", "learning", "data"]
DEFAULT_SENIOR_KEYWORDS   = ["chief", "vp", "head of", "director", "founder", "owner", "co-founder", "cto", "ceo", "cmo", "coo", "cpo", "cfo"]
DEFAULT_LATAM_KEYWORDS    = ["latam", "mexico", "méxico", "colombia", "argentina", "chile", "peru", "perú", "spain", "españa", "miami"]

DATE_FORMATS = [
    "%d %b %Y",     # 15 Mar 2024
    "%d-%b-%y",     # 15-Mar-24
    "%Y-%m-%d",     # 2024-03-15
    "%m/%d/%Y",     # 03/15/2024
    "%d/%m/%Y",     # 15/03/2024
    "%b %d, %Y",    # Mar 15, 2024
]


def parse_date(raw):
    if not raw:
        return None
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def strip_linkedin_preamble(path):
    """LinkedIn exports prefix Connections.csv with a Notes block + blank line.
    Find the real header row (the one that contains 'First Name')."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.readlines()
    header_idx = 0
    for i, line in enumerate(lines):
        if "first name" in line.lower() and "last name" in line.lower():
            header_idx = i
            break
    return "".join(lines[header_idx:])


def read_connections(path):
    raw = strip_linkedin_preamble(path)
    reader = csv.DictReader(raw.splitlines())
    rows = []
    for r in reader:
        first    = (r.get("First Name") or "").strip()
        last     = (r.get("Last Name") or "").strip()
        if not first and not last:
            continue
        company  = (r.get("Company") or "").strip()
        position = (r.get("Position") or "").replace("—", ",").replace("–", ",").strip()
        email    = (r.get("Email Address") or "").strip()
        url      = (r.get("URL") or "").strip()
        connected_raw = (r.get("Connected On") or "").strip()
        connected = parse_date(connected_raw)
        rows.append({
            "first": first, "last": last, "company": company, "position": position,
            "email": email, "url": url,
            "connected": connected,
            "year": connected.year if connected else None
        })
    return rows


def read_skills(path):
    if not path or not os.path.exists(path):
        return Counter()
    counter = Counter()
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            name = (r.get("Name") or r.get("Skill") or "").strip()
            if not name:
                continue
            for col in ("Endorsement Count", "Endorsements", "Number of endorsements", "Count"):
                if col in r and r[col]:
                    try:
                        counter[name] = int(r[col])
                        break
                    except ValueError:
                        pass
            if name not in counter:
                counter[name] = counter.get(name, 0) + 1
    return counter


def read_endorsements(path):
    """Returns dict: lowercased 'first last' -> endorsements received."""
    if not path or not os.path.exists(path):
        return {}
    by_person = Counter()
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            full = (r.get("Endorser") or r.get("Endorsed By") or r.get("Name") or "").strip().lower()
            if full:
                by_person[full] += 1
    return dict(by_person)


def has_keyword(text, keywords):
    t = (text or "").lower()
    return any(k in t for k in keywords)


def score_lead(row, cfg, endorsements_for_person):
    score = 0
    pos = (row.get("position") or "").lower()
    if has_keyword(pos, cfg["ai_intent_keywords"]):
        score += 25
    if has_keyword(pos, cfg["senior_keywords"]):
        score += 20
    if has_keyword(pos, cfg["icp_keywords"]):
        score += 20
    if has_keyword(pos, cfg["latam_keywords"]) or has_keyword(row.get("company", ""), cfg["latam_keywords"]):
        score += 15
    if endorsements_for_person >= 5:
        score += 10
    return min(score, 100)


def auto_detect_eras(years_counter):
    """Given a Counter of {year: count}, return a list of era ranges as
    (label, start, end) tuples. Naive: split into 4 equal-density chunks."""
    if not years_counter:
        return []
    years = sorted(years_counter.keys())
    if len(years) < 4:
        return [(f"Capítulo único ({years[0]}-{years[-1]})", years[0], years[-1])]
    n = len(years)
    chunk = max(1, n // 4)
    eras = []
    for i in range(0, n, chunk):
        block = years[i:i+chunk]
        if not block:
            continue
        eras.append((f"Capítulo {len(eras)+1} ({block[0]}-{block[-1]})", block[0], block[-1]))
    return eras[:5]


def bin_eras(rows, eras):
    counter = OrderedDict((label, 0) for label, _, _ in eras)
    for r in rows:
        if not r["year"]:
            continue
        for label, start, end in eras:
            if start <= r["year"] <= end:
                counter[label] += 1
                break
    return counter


def role_counts(rows):
    keywords = {
        "founders":         ["founder", "owner", "co-founder"],
        "cxo":              ["chief", "cto", "ceo", "cmo", "coo", "cpo", "cfo", "cxo"],
        "directors":        ["director"],
        "managers":         ["manager"],
        "marketing":        ["marketing"],
        "design_creative":  ["design", "creative", "art director"],
        "data_ai":          [" ai ", "data", "machine learning", "ml ", "intelligence"],
        "product":          ["product"],
    }
    out = {k: 0 for k in keywords}
    for r in rows:
        pos = " " + (r.get("position") or "").lower() + " "
        for k, klist in keywords.items():
            if any(kw in pos for kw in klist):
                out[k] += 1
    return out


def top_companies(rows, n=15):
    c = Counter()
    for r in rows:
        comp = r.get("company", "").strip()
        if comp:
            c[comp] += 1
    return dict(c.most_common(n))


def build_insights(rows, skills_counter, endorsements_map, cfg):
    # Per-row scoring + endorsement detection
    for r in rows:
        key = f"{r['first']} {r['last']}".lower()
        end = endorsements_map.get(key, 0)
        r["endorsements"] = end
        r["mutual"] = key in endorsements_map  # we received endorsement; mutuality = both directions
        r["icp_score"] = score_lead(r, cfg, end)

    # Top 30 leads
    top30 = sorted(rows, key=lambda x: x["icp_score"], reverse=True)[:30]

    # Score tier distribution
    tier = {"tier_a_80plus": 0, "tier_b_60_79": 0, "tier_c_40_59": 0, "tier_d_below40": 0}
    for r in rows:
        s = r["icp_score"]
        if s >= 80:   tier["tier_a_80plus"] += 1
        elif s >= 60: tier["tier_b_60_79"] += 1
        elif s >= 40: tier["tier_c_40_59"] += 1
        else:         tier["tier_d_below40"] += 1

    # Years
    by_year = OrderedDict()
    yc = Counter(r["year"] for r in rows if r["year"])
    for y in sorted(yc):
        by_year[str(y)] = yc[y]

    # Eras
    if cfg.get("eras"):
        eras = [(label, span[0], span[1]) for label, span in cfg["eras"].items()]
    else:
        eras = auto_detect_eras(yc)
    era_counts = bin_eras(rows, eras)

    # Era colors. Default palette draws from the SOUND palette set anchored at #DFFF00.
    # Override per-era by passing cfg["era_color"] = { "<label>": "#hex" }.
    default_palette = ["#FF44AB", "#DB75FF", "#DFFF00", "#FF714E", "#FFB70E", "#69A8FF", "#00FDC9", "#34FF6C", "#FA5463"]
    custom = cfg.get("era_color") or {}
    era_color = {}
    for i, label in enumerate(era_counts.keys()):
        era_color[label] = custom.get(label, default_palette[i % len(default_palette)])

    # Warmth signals
    email_count = sum(1 for r in rows if r["email"])
    mutual_count = sum(1 for r in rows if r["mutual"])

    # Cumulative recent invitations: connections in the last 90 days
    today = datetime.today().date()
    recent_count = sum(1 for r in rows if r["connected"] and (today - r["connected"]).days <= 90)

    # Top 30 in viz format
    leads_for_viz = []
    for r in top30:
        # Map this row's connection year to its era
        era = "Sin era"
        for label, start, end in eras:
            if r["year"] and start <= r["year"] <= end:
                era = label
                break
        leads_for_viz.append({
            "first": r["first"], "last": r["last"],
            "company": r["company"], "position": r["position"],
            "icp_score": r["icp_score"],
            "endorsements": r["endorsements"],
            "mutual": r["mutual"],
            "email": bool(r["email"]),
            "recent": bool(r["connected"] and (today - r["connected"]).days <= 90),
            "era": era,
        })

    decisor_keys = ["chief", "cto", "ceo", "cmo", "coo", "cpo", "cfo", "cxo",
                    "vp ", " vp", "head of", "director", "founder", "owner", "co-founder"]
    decisor_count = sum(1 for r in rows if any(k in " " + (r.get("position") or "").lower() + " " for k in decisor_keys))

    insights = {
        "total_connections": len(rows),
        "decisores":         decisor_count,
        "priorizados":       tier["tier_b_60_79"] + tier["tier_c_40_59"] + tier["tier_a_80plus"],
        "mutual_endorsements": mutual_count,
        "email_count":       email_count,
        "reinvitaciones":    recent_count,
        "connections_by_year": by_year,
        "era_distribution":  dict(era_counts),
        "era_color":         era_color,
        "role_keywords":     role_counts(rows),
        "score_distribution": tier,
        "top_skills":        dict(skills_counter.most_common(15)),
        "top_30_leads":      leads_for_viz,
    }
    return insights


DEFAULT_BRAND = {
    "USER_NAME":      "Tu Nombre",
    "BRAND":          "TU MARCA",
    "USER_DOMAIN":    "tu-dominio.com",
    "DIAGNOSTIC_URL": "#",
    "SUBSTACK_URL":   "#",
    "LINKEDIN_URL":   "#",
    "TOOLKIT_REPO":   "https://github.com/nicoborja/network-viz-toolkit",
}


def derive_brand_extras(brand, insights, rows_years):
    brand = dict(brand)  # copy
    brand.setdefault("USER_NAME_UPPER", brand["USER_NAME"].upper())
    total = insights["total_connections"]
    brand.setdefault("TOTAL_CONNECTIONS_LABEL", f"{total:,}".replace(",", ","))
    if rows_years:
        years_min = min(rows_years)
        years_max = max(rows_years)
        span = years_max - years_min + 1
        brand.setdefault("YEARS_SPAN_LABEL", f"{span} años · {years_min}-{years_max}")
        brand.setdefault("YEARS_LABEL_LONG", f"{span} años")
    else:
        brand.setdefault("YEARS_SPAN_LABEL", "")
        brand.setdefault("YEARS_LABEL_LONG", "")
    return brand


def inject_into_template(template_path, insights, out_path, brand=None, years=None):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Brand substitutions
    brand = {**DEFAULT_BRAND, **(brand or {})}
    brand = derive_brand_extras(brand, insights, years or [])
    for key, value in brand.items():
        html = html.replace("{{" + key + "}}", str(value))

    # 2. Data injection (last so JSON values can't accidentally collide with brand keys)
    payload = json.dumps(insights, ensure_ascii=False, indent=2)
    if "{{INSIGHTS_JSON}}" not in html:
        raise RuntimeError("template.html does not contain {{INSIGHTS_JSON}} placeholder")
    html = html.replace("{{INSIGHTS_JSON}}", payload)

    # 3. Sanity check: any remaining {{X}} placeholders?
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if leftover:
        print(f"  WARN: leftover placeholders not substituted: {set(leftover)}", file=sys.stderr)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


def merge_config(user_cfg):
    return {
        "icp_keywords":      user_cfg.get("icp_keywords") or DEFAULT_ICP_KEYWORDS,
        "ai_intent_keywords":user_cfg.get("ai_intent_keywords") or DEFAULT_AI_KEYWORDS,
        "senior_keywords":   user_cfg.get("senior_keywords") or DEFAULT_SENIOR_KEYWORDS,
        "latam_keywords":    user_cfg.get("latam_keywords") or DEFAULT_LATAM_KEYWORDS,
        "eras":              user_cfg.get("eras"),  # may be None
        "era_color":         user_cfg.get("era_color") or {},
        "brand":             user_cfg.get("brand") or {},
    }


def main():
    ap = argparse.ArgumentParser(description="LinkedIn export → eight-panel network viz")
    ap.add_argument("--connections", required=True)
    ap.add_argument("--skills")
    ap.add_argument("--endorsements")
    ap.add_argument("--config", help="Optional JSON file with overrides")
    ap.add_argument("--template", default=os.path.join(os.path.dirname(__file__), "template.html"))
    ap.add_argument("--out", default="network.html")
    ap.add_argument("--insights-out", help="Optional path to also dump raw insights.json")
    args = ap.parse_args()

    user_cfg = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
    cfg = merge_config(user_cfg)

    print(f"Reading {args.connections}...", file=sys.stderr)
    rows = read_connections(args.connections)
    print(f"  {len(rows)} connections parsed.", file=sys.stderr)

    skills = read_skills(args.skills) if args.skills else Counter()
    print(f"  {len(skills)} skills loaded.", file=sys.stderr)

    endorsements = read_endorsements(args.endorsements) if args.endorsements else {}
    print(f"  {len(endorsements)} endorsement records loaded.", file=sys.stderr)

    insights = build_insights(rows, skills, endorsements, cfg)

    if args.insights_out:
        with open(args.insights_out, "w", encoding="utf-8") as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
        print(f"  insights JSON → {args.insights_out}", file=sys.stderr)

    years = sorted([r["year"] for r in rows if r["year"]])
    out = inject_into_template(args.template, insights, args.out,
                               brand=cfg.get("brand"), years=years)
    print(f"\nDone.\n  Network shape: {insights['total_connections']} conexiones · "
          f"{insights['decisores']} decisores · {insights['priorizados']} priorizados.\n  -> {out}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
