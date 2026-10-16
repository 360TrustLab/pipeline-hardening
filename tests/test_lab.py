import unittest
import lab
class TrustBoundaryTests(unittest.TestCase):
    def test_intended_environment_survives_hardening(self):
        self.assertEqual(lab.evaluate()['checks'][0]['after'],'ALLOW')
    def test_branch_and_sibling_lose_authority(self):
        for check in lab.evaluate()['checks'][1:]:self.assertEqual(check['after'],'DENY')
    def test_wrong_issuer_and_missing_claims_fail_closed(self):
        self.assertFalse(lab.trust({},'*'))
        self.assertFalse(lab.trust({'iss':'https://evil.example','aud':lab.AUDIENCE,'sub':lab.SUBJECT},lab.SUBJECT))
