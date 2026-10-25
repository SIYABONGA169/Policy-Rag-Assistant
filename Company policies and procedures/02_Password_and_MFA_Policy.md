# Password and Multi-Factor Authentication (MFA) Policy

**Company:** Apex Global Technologies
**Effective Date:** 22 October 2026
**Policy Owner:** IT Security
**Applies To:** All employees, contractors, and third parties with access to company accounts or systems

## 1. Purpose

This policy establishes minimum requirements for creating, protecting, and resetting passwords, and for the use of multi-factor authentication (MFA), to reduce the risk of unauthorized account access.

## 2. Password Requirements

- Minimum length: **12 characters** for standard user accounts; **16 characters** for administrative/privileged accounts.
- Passwords must not be based on dictionary words, the user's name, company name, or easily guessable patterns.
- Passwords must not be reused across the last **10** passwords (password history).
- Passwords must be changed every **90 days** for standard user accounts and every **60 days** for administrative/privileged accounts.
- Default/vendor passwords must be changed before any system is put into production use.

## 3. Multi-Factor Authentication (MFA)

- MFA is **mandatory** for all users accessing company systems, including email, VPN, and cloud applications (Microsoft 365, Azure, line-of-business apps).
- Approved MFA methods include authenticator app push notifications, FIDO2 security keys, and Windows Hello for Business. SMS-based MFA should be avoided where a stronger method is available.
- Privileged/administrative accounts must use phishing-resistant MFA (e.g., FIDO2 keys or certificate-based authentication) wherever technically supported.
- Users must not share MFA codes or approve push notifications they did not personally initiate ("MFA fatigue" attacks).

## 4. Account Lockout

- Accounts will be temporarily locked after **5** consecutive failed sign-in attempts.
- Locked accounts may be unlocked via self-service password reset (SSPR) or by contacting the IT helpdesk after identity verification.

## 5. Password Storage and Handling

- Passwords must never be written down in plain sight, stored in unencrypted files, or shared via email/chat.
- Approved password managers may be used to store credentials securely.
- Service account and shared account passwords must be stored in an approved secrets vault (e.g., Azure Key Vault) and rotated regularly.

## 6. Self-Service Password Reset (SSPR)

- All users must register SSPR verification methods (authenticator app and/or phone) within **7 days** of account creation.
- SSPR is available from the sign-in screen on company-managed devices where network connectivity is available.

## 7. Privileged Accounts

- Administrative accounts must be separate from standard user accounts and used only for administrative tasks.
- Privileged Identity Management (PIM) or equivalent just-in-time elevation should be used wherever available, rather than standing administrative access.

## 8. Monitoring and Enforcement

- IT Security will monitor for risky sign-ins, credential compromise indicators, and policy non-compliance via Microsoft Entra ID Protection and related tooling.
- Non-compliant accounts may be subject to forced password reset or temporary suspension pending investigation.

## 9. Violations

Failure to comply with this policy may result in disciplinary action and/or revocation of system access.

## 10. Policy Review

This policy will be reviewed at least annually, or sooner in response to emerging threats or regulatory changes.
