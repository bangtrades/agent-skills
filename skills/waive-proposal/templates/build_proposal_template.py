# -*- coding: utf-8 -*-
"""WaiveLabs Vendor Proposal — build template.
WORKED EXAMPLE below is the Summer Fridays v0.4 (lean) proposal. To reuse:
  1. Copy this file + wlstyle.py + assets/fonts into a build dir.
  2. Stage fonts: cp assets/fonts/* /tmp/fonts/   (wlstyle expects /tmp/fonts)
  3. Edit the CONFIG block and the section CONTENT for the new client.
  4. python3 build_proposal_template.py
Keep the SECTION STRUCTURE; replace the CONTENT. See references/proposal-playbook.md."""
import wlstyle
from wlstyle import *   # helpers: section, data_table, field_table, bullets, callout, make_doc, S, CW
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Spacer
from reportlab.lib.units import inch

# ===================== PER-ENGAGEMENT CONFIG — EDIT THIS =====================
CLIENT = "Summer Fridays"
OUT = "/ABSOLUTE/PATH/TO/<Client>_Vendor_Proposal_v0_1.pdf"   # set per engagement
wlstyle.CLIENT = CLIENT
wlstyle.COVER.update({
    "draft":        "DRAFT V0.1   ·   MONTH YEAR   ·   CONFIDENTIAL — PREPARED FOR " + CLIENT.upper(),
    "title":        "AI Growth Desk",            # the engagement / product name
    "subtitle":     "Vendor Proposal",
    "slogan":       "Ride the Waive.",            # WaiveLabs slogan — keep
    "prepared_for": CLIENT + " — Executive Team & IT",
    "doc_title":    "Vendor Proposal",
    "footer_conf":  "Confidential — for " + CLIENT,
})
# Below: WORKED EXAMPLE (SF v0.4). Replace CONTENT per client; keep the structure.
# =============================================================================

story = [NextPageTemplate("Body"), PageBreak()]
A = story.append
X = story.extend

# ===== 01 ENGAGEMENT SUMMARY =====
X(section(1, "Engagement Summary"))
A(Paragraph(
 "WaiveLabs will design, build, and deliver the <b>Summer Fridays AI Growth Desk</b> — the business-facing "
 "dashboards and governed AI agents covering launch performance, brand health, media, ecommerce, and "
 "AI-platform visibility. The Growth Desk reads from data Summer Fridays makes available through its "
 "Microsoft Fabric environment.", S["lede"]))
A(Spacer(1,8))
A(Paragraph(
 "Summer Fridays IT leads the data platform — the Microsoft Fabric build, data ingestion, modeling, security, "
 "and refresh. WaiveLabs is not hands-on in Fabric and performs no data-migration work. We are given governed "
 "read access to the data each capability needs, and we own everything from that data to the decision-maker's "
 "screen: the Growth Desk application and its AI agents. A working prototype of the Growth Desk is already "
 "live for reference.", S["body"]))

# ===== 02 SCOPE & OWNERSHIP =====
X(section(2, "Scope & Ownership"))
X(data_table(
 ["Area", "Owner", "Notes"],
 [["Microsoft Fabric data platform — ingestion, OneLake, modeling, security, refresh", "Summer Fridays IT", "Led internally; WaiveLabs is not hands-on"],
  ["Governed data access for the Growth Desk", "Summer Fridays IT", "Read access provisioned per capability"],
  ["AI Growth Desk — five capability views + AI agents", "WaiveLabs", "Design, build, test, deliver, support"],
  ["AI agent governance, testing &amp; monitoring", "WaiveLabs", "Per Summer Fridays' AI-agent rules"],
  ["Metric definitions used by the Desk", "WaiveLabs", "Aligned to SF's governed data model"],
  ["Change management for the Desk", "WaiveLabs, with IT visibility", "Documented; IT visibility into releases"]],
 [2.7*inch, 1.55*inch, CW - 4.25*inch],
 note="WaiveLabs performs no Fabric data-engineering or migration work — that is led internally by Summer Fridays IT. "
      "Our surface begins at the governed data SF provides and ends at the dashboards and agents business users see."))

# ===== 03 THE FIVE CAPABILITIES =====
X(section(3, "The Five Capabilities — Our Plan"))
A(Paragraph(
 "The Growth Desk delivers the five capabilities your requirements name. Each is a governed dashboard plus a "
 "scoped AI agent, reading the data Summer Fridays provides.", S["body"]))
A(Spacer(1,8))
X(data_table(
 ["Capability", "What the Growth Desk delivers", "Agent", "Phase"],
 [["1 · Launch Retrospective", "Milestone scorecards (1/2/4-wk, 3-mo): POS, spend, marketing contribution, ROI, EMV, by activation lever, vs benchmark", "A1", "1"],
  ["2 · Brand Health &amp; Investment", "Brand health, marketing effectiveness, budget &amp; spend efficiency, support-plan optimization (spend, tactic, mix)", "A5", "3"],
  ["3 · Media Activation", "YTD + year-to-go media flow &amp; performance: spend, objectives, creative, audiences, KPIs, share of search, CTV/CPA/LTV", "A4", "3"],
  ["4 · Ecommerce", "Cross-channel (SF.com, Amazon, TikTok Shop, affiliates): shopper behavior, LTV, cohorts, basket, NTB vs repeat, competitive", "A3", "2"],
  ["5 · AI Platform Visibility", "How ChatGPT/Claude/Perplexity represent &amp; recommend SF; structured-product data, claim governance, monitoring, optimizations", "A2", "1"]],
 [1.7*inch, CW - 3.3*inch, 0.7*inch, 0.55*inch],
 note="Standard and custom time periods (L52W, L12W, YTD, prior year, last week, custom) and filters (geography, SKU, "
      "franchise, retailer, activation type) apply across the Desk. Each capability ships once SF has provisioned the data it needs."))

# ===== 04 AI AGENTS & GOVERNANCE =====
X(section(4, "AI Agents & Governance"))
A(Paragraph(
 "Every agent is scoped, documented, and tested before any user touches it; grounded only on the data Summer "
 "Fridays approves; and labeled so recommendations are never mistaken for validated fact.", S["body"]))
A(Spacer(1,8))
X(data_table(
 ["Agent", "Purpose", "Audience"],
 [["A1 · Launch Performance", "Q&amp;A over launch scorecards, gates, and benchmarks", "Marketing &amp; NPD"],
  ["A2 · AI-Visibility Monitor", "Tracks how consumer AI platforms represent/recommend SF; internal reporting", "Marketing / ecommerce"],
  ["A3 · Ecommerce Analyst", "Channel, cohort, LTV, basket questions; cohort-level only", "Ecommerce"],
  ["A4 · Media Analyst", "Spend, pacing, creative, and audience performance questions", "Media &amp; marketing"],
  ["A5 · Brand Health &amp; Investment", "Brand-health and investment-optimization questions; scenario support", "Exec &amp; marketing"]],
 [1.85*inch, CW - 3.4*inch, 1.55*inch]))
X(data_table(
 ["Summer Fridays' rule", "WaiveLabs control"],
 [["Only approved data sources", "Agents read only SF-approved governed data; per-agent source allow-list; no open web"],
  ["Respect user permissions", "Queries run under the asking user's identity; same access rules as the dashboards"],
  ["Source traceability", "Every figure cites the measure and source behind it"],
  ["Identify incomplete data", "Agents state when data is missing, stale, or out of scope — never estimate"],
  ["No invented metrics or conclusions", "Closed metric vocabulary; refusal when out of scope; golden-question + adversarial test suites"],
  ["Prompt-injection &amp; misuse protection", "Input/output filtering, scope-bound prompts, full interaction logging with review"],
  ["Recommendations distinguishable from fact", "Validated metrics render as data with sources; any suggestion is visibly labeled an AI recommendation"]],
 [2.0*inch, CW - 2.0*inch],
 note="Each agent ships with the governance file your requirements specify: purpose, approved sources, audience, "
      "access controls, limitations, testing approach and results, and monitoring plan."))

# ===== 05 DELIVERY TIMELINE =====
X(section(5, "Delivery Timeline"))
A(Paragraph(
 "Delivery is phased and paced by data availability from Summer Fridays IT. AI Platform Visibility starts first "
 "— it is the most urgent and the least data-dependent.", S["body"]))
A(Spacer(1,8))
X(data_table(
 ["Phase", "Focus", "Depends on"],
 [["Phase 1 — fast start", "AI Platform Visibility baseline; first Launch Retrospective scorecard", "Catalog/site + launch data access"],
  ["Phase 2", "Ecommerce Dashboard + agent", "Channel data access (SF.com, Amazon, TikTok Shop, affiliates)"],
  ["Phase 3", "Media Activation + Brand Health &amp; Investment v1", "Media + brand-health data access"],
  ["Ongoing", "Iteration, agent expansion, deepening (incrementality / MMM-grade where supportable)", "—"]],
 [1.4*inch, CW - 3.7*inch, 2.3*inch],
 note="Phase timing is confirmed at kickoff against SF's data-access schedule. Depth requiring long history or heavy "
      "modeling is ongoing scope. UAT is run with named SF stakeholders before each capability is accepted."))

# ===== 06 REQUIRED DELIVERABLES — COVERAGE & OWNERSHIP =====
X(section(6, "Required Deliverables — Coverage & Ownership"))
X(data_table(
 ["Required deliverable", "Owner", "Where / how"],
 [["1 · Project roadmap, timeline, milestones, resourcing", "WaiveLabs", "Sections 5 &amp; 7"],
  ["2 · Microsoft Fabric solution architecture", "Summer Fridays IT", "Led internally"],
  ["3 · Data source inventory &amp; integration plan", "Summer Fridays IT", "WaiveLabs specifies the data each capability needs"],
  ["4 · Data model, metrics layer, dashboard approach", "Shared", "SF IT governed model; WaiveLabs dashboards + metric definitions"],
  ["5 · AI agent inventory &amp; governance", "WaiveLabs", "Section 4"],
  ["6 · Security &amp; access control model", "Summer Fridays IT", "Platform-level; WaiveLabs applies SF policy in the Desk + agents"],
  ["7 · Data validation &amp; metric definitions", "Shared", "SF IT data validation; WaiveLabs metric definitions for the Desk"],
  ["8 · Testing, UAT, deployment, support, handoff", "WaiveLabs", "UAT per capability with named SF stakeholders; handoff docs"]],
 [2.65*inch, 1.45*inch, CW - 4.1*inch]))

# ===== 07 COMMERCIAL =====
X(section(7, "Commercial"))
X(data_table(
 ["Element", "Structure"],
 [["Engagement", "A single senior resource delivering the AI Growth Desk — engagement lead / solution architecture, AI engineering, and governance / QA"],
  ["Capacity", "60 hours per month"],
  ["Rate", "$350 / hour"],
  ["Fees", "$21,000 / month (60 hours × $350)"],
  ["Payment schedule", "$10,500 deposit at signing · $21,000 at the end of Month 1 · $21,000 at the end of Month 2 · $10,500 on successful closure — <b>$63,000 total over a three-month initial term</b>"],
  ["Term", "Three-month initial engagement to stand up the five capabilities; continues monthly thereafter by agreement"],
  ["Assumptions", "Summer Fridays provides the Fabric platform and governed data access, stakeholder availability, and third-party data licenses in SF's name"]],
 [1.4*inch, CW - 1.4*inch],
 note="Personnel detail not disclosed at proposal stage."))

# ===== 08 NEXT STEPS =====
X(section(8, "What We Need & Next Steps"))
X(data_table(
 ["#", "Step", "Outcome"],
 [["1", "Proposal review with executive team &amp; IT", "Scope, phasing, and commercial confirmed or adjusted"],
  ["2", "Engagement sign-off", "Start date set"],
  ["3", "Data-access nomination", "SF names data owners; read access provisioned per capability (Phase 1 first)"],
  ["4", "AI-Visibility kickoff", "The move-fast workstream begins immediately"]],
 [0.35*inch, 2.7*inch, CW - 3.05*inch]))
A(Spacer(1,6))
A(Paragraph("This proposal is a working draft prepared for discussion.", S["tnote"]))

doc = make_doc(OUT)
doc.build(story)
print("built", OUT)
