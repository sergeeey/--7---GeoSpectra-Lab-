# CAMP Meeting Pre-Flight Checklist
**Meeting:** Tuesday 2026-05-20, 21:30 Almaty (17:30 UK)  
**Status:** 24 hours to go

---

## ✅ Core Materials (READY)

- [x] **Pitch script:** `reports/CAMP_PITCH_5MIN_v0.1.16.md` (5-minute presentation)
- [x] **Q&A prep:** `reports/CAMP_QA_PREP_v0.1.16.md` (7 tough questions + responses)
- [x] **GitHub README:** DOI badge visible, clear entry point
- [x] **Zenodo DOI:** 10.5281/zenodo.20252651 (persistent citation)
- [x] **Manuscript:** `reports/METHODOLOGY_PAPER_COMPRESSED_v0.1.16.md` (8,950 words)

---

## 🔄 Pending (WAIT FOR TOM)

- [ ] **Discord invite link** — Tom chasing up CAMP owner, expect today/tomorrow
- [ ] **Meeting format confirmation** — presentation length? Q&A style? audience size?

---

## 🎯 Pre-Meeting (DO TOMORROW, 2-3 hours before)

### Technical Check (30 min before)
- [ ] Discord installed and audio/video tested
- [ ] GitHub repo loads correctly (check from clean browser)
- [ ] Figure 7 (`reports/FIGURES/F7_lattice_size_scaling.png`) — open locally, ready to screenshare
- [ ] Table 3 (8 non-claims) — locate in manuscript (lines 348-385)
- [ ] Zenodo DOI link works

### Mental Prep (1 hour before)
- [ ] Re-read pitch script ONCE (don't memorize, internalize structure)
- [ ] Review Q&A prep — focus on Q1 (generalization), Q3 (what FL didn't catch), Q5 (covariant compactification)
- [ ] Remind yourself: **honest uncertainty > false confidence**
- [ ] Frame: "Seeking technical review" NOT "Proving methodology"

---

## 📋 During Meeting Protocol

### Opening (if Tom introduces you)
"Thanks Tom. I'm Sergey — independent researcher, Ronin Institute. Background: programmer/AI engineer, not physicist. Built this workflow to systematically catch discretization artifacts in finite-lattice operators. 5-minute overview, then happy to answer questions."

### Presentation Flow
1. Start with Problem (30 sec) — validation theater hooks attention
2. Solution overview (1 min) — 9-rung ladder
3. S²×S¹ case study (2 min) — numbers + Figure 7
4. Scope boundaries (1 min) — 8 non-claims, honest limitation
5. Ask (30 sec) — 3 questions for the group

### Q&A Stance
- **Listen fully** before answering
- **Repeat question** to confirm understanding
- **Answer directly** — if you don't know, say "I don't know, that's [Track X]"
- **Invite follow-up** — "Does that address your concern or should I clarify?"

### Red Flag Defense
If someone challenges generalization:
> "You're right — N=1 geometry is insufficient. That's exactly why Track C exists. I need ≥2 additional geometries before claiming 'reusable methodology'. Right now it's validated proof-of-concept on S²×S¹."

If someone asks "Why should we care?":
> "Fair question. If you work with discretized operators on compact manifolds, FL offers a systematic falsification protocol. If you don't — this might be interesting methodologically but not directly applicable to your work. What's your current validation workflow?"

---

## 🎤 Voice Notes for Tom (if he asks "how to introduce you")

**Option 1 (minimal):**
"Sergey Boyko, independent researcher at Ronin Institute. He's built a falsification-first validation workflow for spectral operators. Sergey, go ahead."

**Option 2 (with context):**
"Sergey reached out after seeing my covariant compactification work. He's developed a systematic validation methodology for finite-lattice operators — caught some interesting discretization artifacts on S²×S¹. Independent researcher, Ronin affiliation. Over to you, Sergey."

**What NOT to include:** "He's a programmer" (defensive framing). Let work speak for itself.

---

## 📊 Backup Materials (if deep dive requested)

### If they want code walkthrough:
Point to: `src/geospectra/operators/s2_sphere.py` (Dirac operator implementation)  
Key function: `build_s2_dirac_product_discretized_NEW()` — clearest example

### If they want test suite:
Point to: `tests/test_ring_alpha_zero_targeted.py` (ring/alpha=0 targeted follow-up)  
Show: 1349 cases, stratified by s1_size, clear pass/fail criteria

### If they want audit report:
Point to: `reports/INDEPENDENT_CODEX_AUDIT_v0.1.16.md`  
Show: Independent agent review, 0 blockers, 5 minor doc fixes

---

## 🚨 Abort Conditions (when to STOP and reschedule)

**Technical:**
- Discord link doesn't arrive → ask Tom for alternative (Zoom?)
- Audio/video completely broken → request async review instead

**Strategic:**
- Audience is hostile/dismissive from the start → pivot to Q&A only, skip presentation
- Meeting runs over time before your slot → offer to send written summary, schedule follow-up

**Personal:**
- You're exhausted/unfocused → better to reschedule than present poorly

---

## 🎯 Success Criteria (what does "good meeting" look like?)

**Minimum success:**
- [x] Delivered 5-min pitch without major technical errors
- [x] Answered ≥3 questions honestly (including "I don't know" where appropriate)
- [x] Got Tom's feedback on Track C geometry priorities

**Good success:**
- [x] Minimum + identified 1-2 FL blind spots from group feedback
- [x] Made contact with ≥1 other CAMP member for future discussion
- [x] No defensive reactions — stayed in "seeking review" mode

**Excellent success:**
- [x] Good + someone volunteers to review manuscript (Track A candidate)
- [x] Got concrete Track C recommendation (which S³×S¹ lattice config to test first)
- [x] Opened door for future CAMP presentations (Track C results in 90 days)

---

## 📝 Post-Meeting Actions (DO WITHIN 24 HOURS)

- [ ] **Thank-you message to Tom** (LinkedIn) — mention 2-3 specific insights from meeting
- [ ] **Log feedback** in `reports/CAMP_MEETING_NOTES_v0.1.16.md`:
  - Who attended (names if shared)
  - Questions asked (verbatim if possible)
  - FL blind spots identified
  - Track C geometry recommendations
  - Follow-up contacts
- [ ] **Update hypothesis-lab Unknown items (U1-U7)** if meeting answered any
- [ ] **Revise manuscript Section 1.2 (Related Work)** based on feedback
- [ ] **Update Track C priorities** if group suggested different geometry sequence

---

## 🧘 Mental Frame (read before meeting)

**You are NOT:**
- Proving covariant compactification
- Defending a thesis
- Selling a product
- Competing with lattice QCD

**You ARE:**
- Sharing a methodological tool
- Seeking technical review
- Identifying blind spots
- Building relationships with domain experts

**Core message:**
> "FL validated on S²×S¹. Generalization TBD. I'm here to learn what it misses, not prove it's perfect."

**If nervous:**
Remember — Tom invited you. He sees value. This is collaborative, not adversarial.

---

**Checklist status:** 5/7 READY, 2/7 PENDING (Discord link + format confirmation)

**Next action:** Wait for Tom's Discord invite. Revisit this checklist 2-3 hours before meeting tomorrow.

**Final reminder:** Honest uncertainty > false confidence. Invite critique, don't defend against it.
