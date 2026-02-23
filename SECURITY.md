# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in DrugMesh, **please do not open a public GitHub issue**.

### How to Report

1. **Email**: Send details to the repository owner via GitHub's private vulnerability reporting.
2. **GitHub Private Advisory**: Use [GitHub's private vulnerability reporting](https://github.com/raimp001/drugmesh/security/advisories/new) to submit a report confidentially.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

### Response Timeline

- **Acknowledgement**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix & Disclosure**: Within 90 days (coordinated disclosure)

## Security Best Practices for Contributors

### Secrets & Credentials
- **Never** commit API keys, passwords, or tokens to the repository
- Use `.env` files locally (already in `.gitignore`)
- Use GitHub Secrets for CI/CD workflows
- Rotate any key that has been accidentally committed immediately

### Dependencies
- Keep dependencies up to date (Dependabot is enabled)
- Pin dependency versions in `requirements.txt`
- Review Dependabot PRs promptly
- Run `pip audit` or `safety check` before releases

### Code Review
- All changes to `main` require a pull request
- No direct pushes to `main`
- At least one review required before merge

### API Security
- All API keys are loaded from environment variables only
- Never log or print API keys
- Use HTTPS for all external API calls
- Validate and sanitise all user inputs

## Known Security Controls

| Control | Status |
|---------|--------|
| `.gitignore` blocks `.env` and secrets | Enabled |
| Dependabot dependency scanning | Enabled |
| GitHub Secret Scanning | Enabled |
| Branch protection on `main` | Enabled |
| CI security workflow (Bandit + Safety) | Enabled |
| Environment variables for all secrets | Implemented |

## Acknowledgements

Thank you to everyone who responsibly discloses security issues.
