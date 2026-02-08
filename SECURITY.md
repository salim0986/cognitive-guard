# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Cognitive Guard, please report it by emailing security@example.com or by opening a private security advisory on GitHub.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Time

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies by severity

## Security Considerations

### Git Hooks

Cognitive Guard installs a git pre-commit hook. This hook:
- Runs in your local repository only
- Does not send data externally
- Can be reviewed at `.git/hooks/pre-commit`
- Can be bypassed with `--no-verify` if needed

### Data Privacy

Cognitive Guard:
- Does NOT send code to external services
- Does NOT collect personal information
- Stores statistics locally in `.cognitive-guard/` directory
- Does NOT require internet connection

### Safe Practices

When using Cognitive Guard:
- Review the hook script before installation
- Keep your configuration file (`.cognitive-guard.yml`) in version control
- Don't commit secrets in documentation
- Use `ignore` patterns for sensitive files

## Known Limitations

- Hook runs arbitrary Python code (yours via analysis)
- AST parsing requires valid syntax
- Statistics stored in plaintext JSON

## Updates

Security updates will be released as patch versions and announced in the CHANGELOG.
