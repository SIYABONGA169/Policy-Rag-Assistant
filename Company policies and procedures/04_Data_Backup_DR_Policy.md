# Data Backup and Disaster Recovery Policy

**Company:** Apex Global Technologies
**Effective Date:** 22 October 2026
**Policy Owner:** IT Department
**Applies To:** All company systems, applications, and data stores

## 1. Purpose

This policy establishes requirements for backing up company data and recovering systems in the event of data loss, corruption, cyberattack, or disaster, to minimize business disruption.

## 2. Scope

Applies to all production systems, databases, file shares, email, and cloud services that store or process company or customer data.

## 3. Backup Requirements

- Critical systems must be backed up at minimum **daily**, with incremental or continuous backup where supported.
- Backups must be retained for a minimum of **90 days**, with monthly archives retained for **1 year**, subject to regulatory requirements.
- Backups must be encrypted at rest and in transit.
- At least one backup copy must be stored in a separate location or region from the primary system (e.g., geo-redundant storage, separate Azure region) to protect against site-level disasters.

## 4. Backup Scope

- Server and VM images (full system state)
- Databases and application data
- Microsoft 365 data (Exchange Online mailboxes, SharePoint/OneDrive content, Teams data) via an approved third-party or native backup solution
- Network and security device configurations

## 5. Testing and Validation

- Backup integrity must be verified through regular test restores, at minimum **quarterly**.
- A full disaster recovery (DR) test/failover exercise must be conducted at least **annually**, with results documented and gaps remediated.

## 6. Recovery Objectives

- **Recovery Point Objective (RPO):** maximum acceptable data loss of **24 hours** for all systems.
- **Recovery Time Objective (RTO):** maximum acceptable downtime of **4 hours** for critical systems.
- Systems must be classified by criticality tier, with corresponding RPO/RTO targets documented in the DR plan.

## 7. Roles and Responsibilities

- IT Operations is responsible for executing and monitoring daily backup jobs and alerting on failures.
- IT Security is responsible for ensuring backup data is protected against ransomware and unauthorized access, including immutable/offline copies where appropriate.
- Department heads are responsible for identifying and prioritizing critical data and systems within their area.

## 8. Ransomware Resilience

- At least one backup copy must be immutable or air-gapped (not directly modifiable from production systems) to protect against ransomware encrypting or deleting backups.
- Backup accounts must use separate credentials with MFA and should not have standing administrative access to production systems.

## 9. Incident Response Integration

In the event of data loss or a security incident affecting data integrity, the Incident Response Policy governs the response process; this policy governs the technical recovery mechanism.

## 10. Policy Review

This policy and the associated DR plan will be reviewed at least annually and after any significant infrastructure change or DR test.
