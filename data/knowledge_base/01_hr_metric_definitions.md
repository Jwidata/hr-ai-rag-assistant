# Governed HR Metric Definitions

This document defines core workforce metrics in plain language for ARIS-style HR Data and AI analytics work. Each metric should be governed through a documented definition, agreed source systems, refresh cadence, and business owner.

## Headcount

### Plain English Meaning

Headcount is the number of employees considered active on a specific date. It is usually reported by legal entity, business unit, country, cost center, job family, and manager hierarchy.

### Formula

Headcount = Count of active employee records as of the reporting date

### Business Use

Leaders use headcount to understand workforce size, monitor growth, track hiring progress, and control organizational cost.

### Common Data-Quality Risks

- Different systems use different definitions of active status.
- Future-dated hires or terminations are handled inconsistently.
- Contingent workers are mixed with employees without clear labeling.
- Duplicate employee records inflate totals.

## FTE

### Plain English Meaning

FTE, or full-time equivalent, converts employees into a standardized workload measure. A part-time employee counts as less than 1.0 depending on contracted hours.

### Formula

FTE = Sum of individual FTE values for active employees

Example: two employees at 0.5 FTE each equal 1.0 FTE.

### Business Use

FTE gives a better view of workforce capacity than headcount when part-time structures differ across teams or countries.

### Common Data-Quality Risks

- Missing or outdated standard hours.
- Inconsistent FTE logic across HRIS and Finance reports.
- Temporary reductions in hours not reflected on time.
- Contractors incorrectly included in the FTE population.

## Average Headcount

### Plain English Meaning

Average headcount smooths out workforce movement during a period. It is commonly used as the denominator for attrition metrics.

### Formula

Average Headcount = (Opening Headcount + Closing Headcount) / 2

Some organizations use monthly averages across the full period for better precision.

### Business Use

It helps leaders measure movement rates more fairly when headcount changes during the quarter or year.

### Common Data-Quality Risks

- No agreed rule for averaging.
- Month-end snapshots are missing or misaligned.
- Reorganizations cause reporting breaks in historical trends.

## Attrition Rate

### Plain English Meaning

Attrition rate shows how much of the workforce left during a defined period.

### Formula

Attrition Rate = Number of Exits during Period / Average Headcount during Period

### Business Use

It helps HR and leadership monitor retention health, workforce stability, and talent risk.

### Common Data-Quality Risks

- Exit dates are missing or updated late.
- Internal transfers are wrongly counted as exits.
- The exit population is not aligned with the denominator population.
- Voluntary and involuntary exits are not categorized consistently.

## Voluntary Attrition

### Plain English Meaning

Voluntary attrition measures employee exits initiated by the employee, such as resignations.

### Formula

Voluntary Attrition Rate = Number of Voluntary Exits / Average Headcount

### Business Use

This metric helps identify issues related to engagement, leadership, pay competitiveness, workload, or career growth.

### Common Data-Quality Risks

- Termination reasons are coded inconsistently.
- Resignations and mutual separations are grouped incorrectly.
- Local HR teams use different reason taxonomies.

## Involuntary Attrition

### Plain English Meaning

Involuntary attrition measures exits initiated by the company, such as dismissals, redundancies, or end of probation.

### Formula

Involuntary Attrition Rate = Number of Involuntary Exits / Average Headcount

### Business Use

It helps leaders monitor restructuring impact, performance-management outcomes, and employee-relations risk.

### Common Data-Quality Risks

- Redundancy, dismissal, and end-of-contract categories are mixed.
- Country-level legal reasons are not mapped into a common enterprise taxonomy.

## Retention Rate

### Plain English Meaning

Retention rate shows the percentage of employees who stayed during the reporting period.

### Formula

Retention Rate = 1 - Attrition Rate

or

Retention Rate = Employees Remaining through Period / Starting Employee Population

### Business Use

Leaders use retention rate to understand workforce stability and to compare performance across functions or locations.

### Common Data-Quality Risks

- The starting population is not frozen consistently.
- Maternity leave, long leave, or transfer rules differ across reports.

## New-Hire Attrition

### Plain English Meaning

New-hire attrition measures the percentage of employees who leave within an early period after joining, often 90 days, 6 months, or 12 months.

### Formula

New-Hire Attrition Rate = Number of New Hires Leaving within Defined Period / Total New Hires in Cohort

### Business Use

This metric helps assess hiring quality, onboarding effectiveness, role clarity, and manager support.

### Common Data-Quality Risks

- Hire date and rehire date logic are inconsistent.
- Cohort windows are not defined clearly.
- Internal mobility cases are misclassified as new hires.

## Hiring Plan Achievement

### Plain English Meaning

Hiring plan achievement measures how much of the approved hiring plan has been delivered.

### Formula

Hiring Plan Achievement = Actual Hires / Planned Hires

### Business Use

It helps leaders assess recruiting delivery, workforce execution, and whether growth plans are on track.

### Common Data-Quality Risks

- The approved plan changes but baseline targets are not version controlled.
- Planned roles and actual hires are compared at different levels of detail.
- Backfills and net-new positions are mixed.

## Vacancy Rate

### Plain English Meaning

Vacancy rate shows the share of approved positions that are open and unfilled.

### Formula

Vacancy Rate = Number of Open Approved Positions / Total Approved Positions

### Business Use

It helps leaders identify hiring gaps, operational strain, and workforce capacity risk.

### Common Data-Quality Risks

- Position management is incomplete or not used consistently.
- Frozen roles remain listed as open vacancies.
- Approved position counts do not reconcile with budget structures.

## Time to Fill

### Plain English Meaning

Time to fill measures how long it takes to fill an approved role, usually from requisition approval to accepted offer or start date depending on the agreed definition.

### Formula

Time to Fill = Role Filled Date - Requisition Approval Date

### Business Use

It helps recruiting leaders track process speed, hiring bottlenecks, and workforce capacity risk.

### Common Data-Quality Risks

- No standard definition of filled date.
- Approval dates are missing or captured outside the ATS.
- Reopened requisitions distort cycle time.

## Time to Hire

### Plain English Meaning

Time to hire measures how long it takes to move a candidate through the recruiting process once they enter the pipeline.

### Formula

Time to Hire = Offer Accepted Date - Candidate Application Date

Some teams define it from first recruiter contact or first interview date.

### Business Use

It helps recruiting teams understand candidate-process speed and identify delays in screening, interviews, or approvals.

### Common Data-Quality Risks

- Candidate stage timestamps are incomplete.
- Multiple applications from the same candidate are not handled consistently.
- Candidate withdrawal and requisition pause rules are unclear.

## Governance Guidance

For each metric, HR analytics teams should define:

- Population scope
- Inclusion and exclusion rules
- Source system of record
- Refresh frequency
- Calculation logic
- Metric owner
- Known limitations
