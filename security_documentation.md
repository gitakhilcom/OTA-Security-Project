# Security Documentation

## GitHub Secrets

GitHub Secrets are used to securely store sensitive information required for the project.

The private key is stored securely in GitHub Secrets and is not exposed in repository files.

## Secret Management

Sensitive credentials are stored using GitHub Secrets.

Secrets are not exposed in repository files or commit history.

## Automated Pipeline Secret Injection

To maintain a secure CI/CD pipeline, sensitive credentials are never hardcoded into workflow files or source code. Instead, GitHub Actions securely injects secrets into the runner environment at runtime using GitHub Secrets.

The following workflow snippet illustrates how GitHub Secrets can be securely referenced during CI/CD execution.

### Example GitHub Actions Configuration

yaml
- name: Load Cryptographic Credentials
  env:
    PRIVATE_KEY: ${{ secrets.FIRMWARE_PRIVATE_KEY }}
  run: |
    echo "Secrets securely loaded into the workflow environment."

### Benefits

- Prevents exposure of sensitive credentials in the repository.
- Makes secrets available only during workflow execution.
- Follows security best practices for CI/CD pipelines.
- Reduces the risk of accidental credential leakage.
