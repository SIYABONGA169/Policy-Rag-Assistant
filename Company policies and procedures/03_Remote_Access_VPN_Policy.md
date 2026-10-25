# Remote Access and VPN Policy

**Company:** Apex Global Technologies
**Effective Date:** 22 October 2026
**Policy Owner:** IT Department
**Applies To:** All employees, contractors, and third parties requiring remote access to company systems

## 1. Purpose

This policy defines the requirements for securely connecting to Apex Global Technologies' network and systems from outside company premises.

## 2. Scope

Applies to all remote connections to company resources via VPN, cloud services, or remote desktop, from company-owned or approved personal devices.

## 3. Access Requirements

- Remote access must be requested through IT and approved by the user's manager.
- Remote access requires an active company account with MFA enabled, in line with the Password and MFA Policy.
- Only devices that meet the company's minimum security baseline (up-to-date OS, antivirus/endpoint protection active, disk encryption enabled) may connect remotely.

## 4. VPN Usage

- The company-approved VPN client (e.g., Azure VPN Client) must be used for all remote access to internal resources not otherwise published via secure cloud gateways.
- Split tunneling is **not permitted** — all other traffic must route through the corporate VPN gateway.
- Users must disconnect from VPN when not actively required and must not leave sessions connected unattended for extended periods.

## 5. Device Requirements

- Company-owned devices must have endpoint protection, disk encryption, and current security patches before remote access is granted.
- Personally owned devices (if permitted) must meet the same minimum security requirements and be enrolled in the company's mobile device management (MDM) solution.
- Use of public or unsecured Wi-Fi for remote access is discouraged; where unavoidable, VPN must be active for the full session.

## 6. Conditional Access

- Remote sign-ins are subject to Conditional Access policies, which may require MFA, block access from unapproved locations, or require a compliant device, depending on risk level.
- Access may be automatically blocked or challenged for sign-ins flagged as high risk.

## 7. Prohibited Activities

- Sharing VPN credentials or allowing another person to use an authenticated remote session is prohibited.
- Using remote access to bypass company security controls or access systems outside the scope of the user's role is prohibited.
- Installing unauthorized remote access or remote control software is prohibited.

## 8. Monitoring

Remote access sessions may be logged and monitored for security and compliance purposes, consistent with applicable law.

## 9. Incident Reporting

Any suspected compromise of remote access credentials or a lost/stolen device with remote access configured must be reported to IT immediately.

## 10. Violations

Violation of this policy may result in suspension of remote access privileges and/or disciplinary action.

## 11. Policy Review

This policy will be reviewed at least annually.
