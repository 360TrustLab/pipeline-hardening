# Operating decisions for the release pipeline

I treat the release pipeline as a production application. Before narrowing its
role, I want to know what a legitimate release needs and who will recover it
when that understanding turns out to be incomplete.

## The first change

Start with one workflow and its deployment role. Record the trigger, the exact
OIDC subject, the intended S3 prefix, and the engineer responsible for the
workflow. Name a reviewer for changes to the AWS trust policy. A repository
environment also needs configured protection rules; its name in YAML is only
part of the configuration.

The local model compares synthetic claims. It does not authenticate tokens or
establish an AWS decision. Use the README's separate sandbox deployment and
probe before claiming that the real role grants or denies a request.

## Evidence for the decision

Keep the same intended and unrelated requests before and after the change.
The intended release should still work. An unrelated context or resource should
lose access for the expected reason. A missing resource, invalid token, or
other setup error needs investigation rather than being counted as a successful
authorization test.

The current AWS deployment checks intended and unrelated S3 prefixes. Its local
negative-subject comparison is a separate model. A real STS rejection from an
unrelated repository still needs its own sandbox validation.

## Ownership and recovery

Someone has to maintain the pinned actions, runner images, trust configuration,
and verification policy. Keep the required access and recovery instructions
where another engineer can find them. A failed legitimate release should have
a reviewed, narrow recovery path instead of an account-wide permission grant.

For an emergency release, identify the exact source ref and artifact, the
independent approver, the expiry, and the person who will remove temporary
access. This is an operating pattern to design and test. The lab does not
implement an emergency role, runner isolation, or artifact attestation.

An Azure release path needs equivalent ownership and tests, with its own
federated-credential, authorization, and environment configuration.
