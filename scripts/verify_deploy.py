"""Real AWS probe. Uses the AWS CLI configured by the OIDC Action; prints no credentials."""
import json,os,subprocess,tempfile
bucket=os.environ['ARTIFACT_BUCKET']
with tempfile.TemporaryDirectory() as td:
    from pathlib import Path
    source=Path(td)/'release.txt';source.write_text('360TrustLab synthetic conference artifact\n')
    results=[]
    for prefix,expected in [('releases',True),('unrelated',False)]:
        p=subprocess.run(['aws','s3api','put-object','--bucket',bucket,'--key',prefix+'/conference.txt','--body',str(source)],capture_output=True,text=True)
        allowed=p.returncode==0
        if not allowed and 'AccessDenied' not in p.stderr:
            raise SystemExit('AWS probe failed for a reason other than authorization. Check setup; no conclusion drawn.')
        results.append({'operation':'s3:PutObject','prefix':prefix,'result':'ALLOW' if allowed else 'DENY','expected':expected})
        if allowed != expected:raise SystemExit(json.dumps({'unexpected_result':results}))
    print(json.dumps({'scope':'REAL AWS SDK/CLI request results','checks':results},indent=2))
