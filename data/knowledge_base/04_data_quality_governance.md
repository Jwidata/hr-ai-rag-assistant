# Data Quality and Governance in HR

This document outlines the core controls that make HR reporting, AI use cases, and leadership dashboards trustworthy.

## Data Ownership

Data ownership means specific business or functional owners are accountable for key HR data fields and correction processes. Ownership should be assigned for employee master data, organization structures, compensation attributes, and recruiting data.

## Source of Truth

Source of truth means there is a clearly designated system for each core data element. For example, Workday may be the source of truth for employee master data, while Finance may own budget and actual cost data.

## Employee ID Validation

Employee ID validation checks whether each employee record has a valid, unique, and correctly formatted identifier.

Common checks include:

- Employee ID is not null
- Employee ID matches expected format
- Employee ID exists only once in the active employee population

## Duplicate Employee Checks

Duplicate checks identify cases where the same employee appears multiple times in the same reporting population without a valid business reason.

Typical logic compares employee ID, name, hire date, legal entity, and active status.

## Missing Cost Center Checks

These checks identify employee or position records that do not have a valid cost center assignment.

This matters because missing cost center values break workforce cost analysis, planning, and Finance reconciliation.

## Invalid Manager Hierarchy

Invalid manager hierarchy checks identify records where the manager does not exist, points to self, creates a loop, or belongs to the wrong population.

This matters because many org dashboards, approvals, and span-of-control metrics depend on a clean reporting structure.

## Payroll vs Finance Reconciliation

This control compares payroll outputs with Finance actuals or accruals to confirm that workforce cost reporting is complete and consistent.

Common reconciliation questions include:

- Do payroll totals match labor expense totals within agreed tolerance?
- Are one-time payments handled consistently?
- Are timing differences documented?

## Salary Band Completeness

Salary band completeness checks whether employees in covered populations have valid band assignment, midpoint, minimum, and maximum values.

Without this, compa-ratio and range penetration reporting become unreliable.

## Metric Definition Governance

Metric definition governance means each published KPI has an approved definition, formula, scope, source system, and owner.

This avoids situations where different teams publish different versions of headcount, attrition, or vacancy rate.

## Audit Trail

An audit trail records what changed, when it changed, who changed it, and why. This is important for HR controls, compensation reviews, and compliance-sensitive reporting.

## Data Quality Score

A data quality score is a summarized indicator of data health across selected dimensions such as completeness, validity, consistency, timeliness, and uniqueness.

Example logic:

Data Quality Score = Weighted result of key validation checks across important fields

## Recommended Governance Model

Strong HR data governance usually includes:

- Named data owners and stewards
- Standard validation rules
- Issue logs and remediation tracking
- Agreed source-of-truth mapping
- Controlled metric definitions
- Evidence of reconciliation and auditability
