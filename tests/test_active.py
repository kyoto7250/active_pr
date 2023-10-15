import datetime
import unittest

from active_pr.active import Active, ActiveReporter


class TestActiveReporter(unittest.TestCase):
    def test_report(self):
        pr = Active(
            type="pr",
            url="https://example.co.jp",
            repo_name="example/example",
            title="example PR",
            created_at=datetime.datetime(2020, 1, 1),
            closed_at=datetime.datetime(2020, 1, 2),
        )

        issue = Active(
            type="issue",
            url="https://example.co.jp",
            repo_name="example/example",
            title="example Issue",
            created_at=datetime.datetime(2020, 1, 1),
            closed_at=None,
        )

        output = ActiveReporter().report([pr, issue])
        expected = (
            "| repo_name       | type   | title                                  | created_at   | closed_at   |\n"
            "|-----------------|--------|----------------------------------------|--------------|-------------|\n"
            "| example/example | PR     | [example PR](https://example.co.jp)    | 2020-01-01   | 2020-01-02  |\n"
            "| example/example | ISSUE  | [example Issue](https://example.co.jp) | 2020-01-01   |             |"
        )
        assert str(output) == expected
