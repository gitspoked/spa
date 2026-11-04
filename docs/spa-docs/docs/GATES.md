# GATES — Gate Definitions and Evidence Requirements

**Status:** Draft — Gate 0  
**Version:** 0.1.0  
**Date:** 2026-11-03  
**Canonical parent:** SPEC-001

## Gate 0 — Structure Exists

**Claim:** The canonical SPEC-001 and PROCESS documents exist and are internally consistent.  
**Required evidence:** Presence of the documents + consistency checklist.  
**Settlement:** Structural only. Does not grant authority.

## Gate 1 — Requirements Drafts Complete

**Claim:** BRD, FRD, and PRD exist, reference SPEC-001, declare authority none, and contain no unresolved load-bearing claims used as premises.  
**Required evidence:** Document set + traceability table + quarantine list.  
**Settlement:** Structural completeness.

## Gate 2 — Architectural Decisions Recorded

**Claim:** At least three ADRs exist covering identity, provisional-vs-settlement, and self-amendment.  
**Required evidence:** ADR files with context, decision, consequences, and alternatives.  
**Settlement:** Structural.

## Gate 3 — First Orchestration Loop with Receipts

**Claim:** A minimal agentic loop has executed: parallel evidence collection → response receipts → deterministic settlement → (optional) LearningEvent.  
**Required evidence:** Receipt log (content-addressed) from the sketch or equivalent.  
**Settlement:** Evidence-driven. May remain INDETERMINATE if only stubs are used.

## Gate 4 — Learning Events Reviewed

**Claim:** At least one LearningEvent has been examined and either produced a settled amendment or been explicitly quarantined.  
**Required evidence:** LearningEvent receipt + amendment settlement or quarantine record.  
**Settlement:** Evidence-driven.

## Amendment of Gates

Any gate definition may be amended only via a settled PASS claim (normally originating from a LearningEvent). Prior gate definitions remain content-addressed.

---

**Disposition:** Initial set. Subject to self-adjustment after Gate 3/4.
