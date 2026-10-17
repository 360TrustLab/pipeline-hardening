# Technical references

- [GitHub OIDC subject claims](https://docs.github.com/en/actions/reference/security/oidc)
- [GitHub OIDC with AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [GitHub Actions security](https://docs.github.com/en/actions/reference/security/secure-use)
- [AWS role trust for OIDC](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)

The local check compares issuer, audience, and subject strings. It does not
validate a JWT signature or call STS. The AWS deployment and probe are separate
steps documented in the README.
