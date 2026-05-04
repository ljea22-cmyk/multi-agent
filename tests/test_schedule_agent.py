import unittest
import sys
from pathlib import Path

# ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from schedule_agent import extract_fields, normalize_period


class TestScheduleAgent(unittest.TestCase):
    def test_extract_fields_basic(self):
        block = """[공지] 시험 안내
대상: 모든 학생
기간: 2026-06-01
준비물: 학생증
내용: 기말고사가 2026-06-01에 있습니다.
"""
        f = extract_fields(block)
        # title should start with the notice header
        self.assertTrue(f['title'].lower().startswith('[공지]'))
        self.assertEqual(f['targets'], '모든 학생')
        self.assertEqual(f['items'], '학생증')

    def test_normalize_period_range(self):
        p = '2026-05-20 ~ 2026-05-21'
        n = normalize_period(p)
        self.assertEqual(n, ('2026-05-20', '2026-05-21'))

    def test_normalize_period_single(self):
        p = '2026-05-10'
        n = normalize_period(p)
        self.assertEqual(n, ('2026-05-10', '2026-05-10'))


if __name__ == '__main__':
    unittest.main()
