"""CRH04: a bounded local OIDC condition model, not an STS implementation."""
import argparse, fnmatch, json
from pathlib import Path
ISSUER = 'https://token.actions.githubusercontent.com'
AUDIENCE = 'sts.amazonaws.com'
ORG = '360TrustLab@SYNTHETIC-ORG-ID'
REPO = 'pipeline-hardening@SYNTHETIC-REPO-ID'
SUBJECT = f'repo:{ORG}/{REPO}:environment:conference-sandbox'

def trust(claims, subject_pattern):
    """Only compare sample issuer/audience/subject; do not authenticate tokens."""
    return (claims.get('iss') == ISSUER and claims.get('aud') == AUDIENCE
            and fnmatch.fnmatchcase(claims.get('sub', ''), subject_pattern))

def evaluate():
    cases = [
        ('Intended protected environment', SUBJECT, AUDIENCE),
        ('Feature branch in this repository', f'repo:{ORG}/{REPO}:ref:refs/heads/feature', AUDIENCE),
        ('Another repository in the organization', f'repo:{ORG}/unrelated@OTHER-ID:environment:conference-sandbox', AUDIENCE),
        ('Wrong audience', SUBJECT, 'untrusted.example'),
    ]
    before = f'repo:{ORG}/*'
    checks=[]
    for name, subject, audience in cases:
        claims={'iss':ISSUER,'aud':audience,'sub':subject}
        checks.append({'name':name,'subject':subject,'before':'ALLOW' if trust(claims,before) else 'DENY',
                       'after':'ALLOW' if trust(claims,SUBJECT) else 'DENY'})
    return {'lab':'CRH04 · Pipeline hardening','scope':'LOCAL CONDITION MODEL · synthetic claims · no AWS calls',
            'before':{'subject':before,'workflow_permissions':'write-all (inactive example only)',
                      'action_reference':'mutable tag (inactive example only)'},
            'after':{'subject':SUBJECT,'workflow_permissions':'contents: read; id-token: write on deploy job only',
                     'action_reference':'full commit SHA; checkout credentials not persisted'},
            'checks':checks,'assertions':{'intended_still_allowed':checks[0]['after']=='ALLOW',
              'feature_branch_denied':checks[1]['after']=='DENY','sibling_repository_denied':checks[2]['after']=='DENY',
              'wrong_audience_denied':checks[3]['after']=='DENY'}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='artifacts/report.json');a=p.parse_args()
    report=evaluate();out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    return 0 if all(report['assertions'].values()) else 1
if __name__=='__main__':raise SystemExit(main())
