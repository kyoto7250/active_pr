import datetime
import logging
from argparse import Namespace

from dateutil.tz import tzutc

from active_pr.active import Active
from active_pr.api import GithubAPI

from .pygithub_testcase import PyGithubTestCase

requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)


class TestGithubAPI(PyGithubTestCase):
    def test_prs(self) -> None:
        gh = GithubAPI(args=Namespace(github_token=None))
        active = Active(
            "pr",
            "https://example.co.jp",
            "repo/name",
            "title",
            datetime.date(2020, 1, 1),
            None,
        )
        assert gh.prs == []

        gh.actives["pr"] = [active]
        assert gh.prs == [active]

    def test_issues(self) -> None:
        gh = GithubAPI(args=Namespace(github_token=None))
        active = Active(
            "issue",
            "https://example.co.jp",
            "repo/name",
            "title",
            datetime.date(2020, 1, 1),
            None,
        )
        assert gh.issues == []

        gh.actives["issue"] = [active]
        assert gh.issues == [active]

    def test_call(self) -> None:
        gh = GithubAPI(
            args=Namespace(
                author="username",
                type="issue",
                begin="2023-03-01",
                end="2023-03-30",
                state="closed",
                github_token=None,
            )
        )
        gh()

        assert gh.prs == []
        expected = Active(
            type="issue",
            url="https://example.com/username/example",
            repo_name="repo_name/example",
            title="Example Title",
            created_at=datetime.datetime(2020, 9, 19, 16, 59, 41, tzinfo=tzutc()),
            closed_at=datetime.datetime(2023, 3, 22, 16, 32, 1, tzinfo=tzutc()),
        )
        assert gh.issues == [expected]

        gh = GithubAPI(
            args=Namespace(
                author="username",
                type="issue",
                begin="2023-03-01",
                end="2023-03-30",
                state="open",
                github_token=None,
            )
        )
        gh()
        assert gh.prs == []
        assert gh.issues == []
