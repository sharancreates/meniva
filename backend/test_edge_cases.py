import unittest
from datetime import datetime, date, timedelta
try:
    from .app import create_app
    from .models import db, User, DailyLog
except ImportError:
    from app import create_app
    from models import db, User, DailyLog

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key_for_unit_tests_only'
    ALLOWED_ORIGINS = ['http://localhost:5173']
    DEBUG = False
    SESSION_COOKIE_SECURE = False
    RATELIMIT_ENABLED = False
    LEGACY_DEK_KEY = 'p_Mh8N-YsKDORo4aEg5zYf51CJ8KD0qkmMDEOdrCVo4='

class SeleneEdgeCasesTestCase(unittest.TestCase):
    """
    Automated test cases asserting the canonical edge cases and specifications
    from the Period Tracking App Complete Testing Guide (TC-001 through TC-020).
    """

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _register_user(self, username="edge_user", pin="123456"):
        payload = {
            "username": username,
            "pin": pin,
            "cycle_length_baseline": 28,
            "period_length_baseline": 5
        }
        res = self.client.post('/api/auth/register', json=payload)
        token = res.get_json()['token']
        return token, {'Authorization': f'Bearer {token}'}

    def test_tc_001_log_period_today(self):
        """TC-001: Log period start for today -> Entry saved successfully."""
        token, headers = self._register_user("tc001_user")
        today_str = datetime.now().date().isoformat()
        
        payload = {
            "log_date": today_str,
            "phase": "menstrual",
            "flow_intensity": 60,
            "energy_level": 40
        }
        res = self.client.post('/api/logs/sync', json=payload, headers=headers)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'success')

    def test_tc_002_log_period_future_date_blocked(self):
        """TC-002: Log period start for a future date -> Blocked with HTTP 400."""
        token, headers = self._register_user("tc002_user")
        future_date = (datetime.now().date() + timedelta(days=7)).isoformat()
        
        payload = {
            "log_date": future_date,
            "phase": "menstrual",
            "flow_intensity": 50
        }
        res = self.client.post('/api/logs/sync', json=payload, headers=headers)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("error", data)
        self.assertIn("Future date logging is not permitted", data['error'])

    def test_tc_005_delete_log_entry(self):
        """TC-005: Delete a log entry -> Log removed cleanly from database."""
        token, headers = self._register_user("tc005_user")
        past_date = (datetime.now().date() - timedelta(days=5)).isoformat()
        
        # 1. Create log
        self.client.post('/api/logs/sync', json={
            "log_date": past_date,
            "phase": "follicular",
            "energy_level": 80
        }, headers=headers)

        # 2. Delete log
        res_del = self.client.delete(f'/api/logs?date={past_date}', headers=headers)
        self.assertEqual(res_del.status_code, 200)
        self.assertEqual(res_del.get_json()['status'], 'success')

        # 3. Verify it no longer exists
        res_del_again = self.client.delete(f'/api/logs?date={past_date}', headers=headers)
        self.assertEqual(res_del_again.status_code, 404)

    def test_tc_012_export_to_csv(self):
        """TC-012: Export health logs to RFC 4180 CSV for clinician."""
        token, headers = self._register_user("tc012_user")
        
        # Add a couple past logs
        for i in range(3):
            d = (datetime.now().date() - timedelta(days=10-i)).isoformat()
            self.client.post('/api/logs/sync', json={
                "log_date": d,
                "phase": "menstrual",
                "flow_intensity": 70 - i * 10,
                "pelvic_pain": 30
            }, headers=headers)

        res_csv = self.client.get('/api/logs/export/csv', headers=headers)
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn('text/csv', res_csv.headers['Content-Type'])
        self.assertIn('attachment', res_csv.headers['Content-Disposition'])
        
        csv_text = res_csv.data.decode('utf-8')
        self.assertIn("Date,Cycle Phase,Energy Level,Pelvic Pain", csv_text)
        self.assertIn("Menstrual", csv_text)

    def test_tc_013_idor_authorization_prevention(self):
        """TC-013: Open or delete another user's record ID via API -> 404 / isolated."""
        client_a = self.app.test_client()
        client_b = self.app.test_client()

        res_a = client_a.post('/api/auth/register', json={
            "username": "user_alice", "pin": "123456", "cycle_length_baseline": 28, "period_length_baseline": 5
        })
        headers_a = {'Authorization': f'Bearer {res_a.get_json()["token"]}'}

        res_b = client_b.post('/api/auth/register', json={
            "username": "user_bob", "pin": "123456", "cycle_length_baseline": 28, "period_length_baseline": 5
        })
        headers_b = {'Authorization': f'Bearer {res_b.get_json()["token"]}'}
        
        d = (datetime.now().date() - timedelta(days=2)).isoformat()
        client_a.post('/api/logs/sync', json={
            "log_date": d, "phase": "ovulatory", "energy_level": 90
        }, headers=headers_a)

        # User B attempts to delete Alice's log
        res_del = client_b.delete(f'/api/logs?date={d}', headers=headers_b)
        self.assertEqual(res_del.status_code, 404)

    def test_tc_014_permanent_account_deletion_gdpr(self):
        """TC-014: Permanent GDPR erasure -> User and all records purged from database."""
        token, headers = self._register_user("gdpr_user")
        
        # Add log
        d = (datetime.now().date() - timedelta(days=3)).isoformat()
        self.client.post('/api/logs/sync', json={
            "log_date": d, "phase": "luteal", "sleep_quality": 85
        }, headers=headers)

        # Permanent deletion request
        res_del = self.client.delete('/api/auth/account?permanent=true', headers=headers)
        self.assertEqual(res_del.status_code, 200)
        self.assertIn("permanently erased", res_del.get_json()['message'])

        # Confirm user is completely gone
        user = User.query.filter_by(username="gdpr_user").first()
        self.assertIsNone(user)
        # Confirm logs are completely gone
        logs = DailyLog.query.all()
        self.assertEqual(len(logs), 0)

    def test_tc_015_wrong_pin_5_times_lockout(self):
        """TC-015: Wrong PIN 5 times -> 15-minute lockout enforced (HTTP 423)."""
        token, headers = self._register_user("lockout_user", pin="654321")

        # Attempts 1 to 4 should return 401 with remaining attempts
        for attempt in range(1, 5):
            res = self.client.post('/api/auth/verify-pin', json={"pin": "000000"}, headers=headers)
            self.assertEqual(res.status_code, 401)
            self.assertIn("remaining before temporary lockout", res.get_json()['error'])

        # 5th attempt should trigger 423 lockout
        res_5 = self.client.post('/api/auth/verify-pin', json={"pin": "000000"}, headers=headers)
        self.assertEqual(res_5.status_code, 423)
        data_5 = res_5.get_json()
        self.assertTrue(data_5['locked'])
        self.assertIn("temporarily locked", data_5['error'])

        # 6th attempt (even with CORRECT PIN) should still be rejected while locked out
        res_locked = self.client.post('/api/auth/verify-pin', json={"pin": "654321"}, headers=headers)
        self.assertEqual(res_locked.status_code, 423)
        self.assertTrue(res_locked.get_json()['locked'])

if __name__ == '__main__':
    unittest.main()
