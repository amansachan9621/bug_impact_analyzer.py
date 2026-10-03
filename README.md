# Git Bug Resolution Impact & Regression Scope Analyzer

A Python-based Software QA tool designed for SoC and Android engineering workflows. It maps resolved Bug IDs and Git patch commits to underlying system architecture, identifying affected modules and automatically recommending targeted regression test cases.

### Features
- **Git Commit Patch Tracking:** Extracts modified files from resolved defect changelists.
- **Module Impact & Blast-Radius Detection:** Maps file paths to hardware HALs, multimedia codecs, and kernel drivers.
- **Automated QA Regression Scoping:** Generates a prioritized list of regression test cases that must be re-validated by the QA engineer.

### Usage
```bash
python bug_impact_analyzer.py BUG-84920
