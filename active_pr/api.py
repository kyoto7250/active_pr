import datetime
from typing import Optional

from github import Auth, Github
from rich.console import Console

from active_pr.active import Active
from active_pr.exception import GithubException


class GithubAPI:
    BOTH: str = "both"

    def __init__(self, args) -> None:
        self.args = args
        self.actives: dict[str, list[Active]] = {}
        self.gh = Github(
            auth=None if args.github_token is None else Auth.Token(args.github_token)
        )

    @property
    def prs(self) -> list[Active]:
        return [] if "pr" not in self.actives else self.actives["pr"]

    @property
    def issues(self) -> list[Active]:
        return [] if "issue" not in self.actives else self.actives["issue"]

    def __call__(self):
        try:
            if self.args.type in [self.BOTH, "issue"]:
                self._fetch(
                    "issue",
                    self.args.state,
                    self.args.author,
                    self.args.begin,
                    self.args.end,
                )

            if self.args.type in [self.BOTH, "pr"]:
                self._fetch(
                    "pr",
                    self.args.state,
                    self.args.author,
                    self.args.begin,
                    self.args.end,
                )
        except GithubException as ge:
            return ge

    def _resolve(self, type: str, pager) -> None:
        if type not in self.actives:
            self.actives[type] = []

        for instance in pager:
            repo_name: str = instance.repository.full_name
            title: str = instance.title
            created_at: datetime.date = instance.created_at
            closed_at: Optional[datetime.date] = instance.closed_at
            url: str = instance.html_url
            self.actives[type].append(
                Active(type, url, repo_name, title, created_at, closed_at)
            )

    def _fetch(self, type: str, state: str, author: str, begin: str, end: str) -> None:
        if type in self.actives:
            raise RuntimeError(f"Already exists: {type}")
        created_range: str = f"{begin}..{end}"
        console = Console()
        with console.status("[bold green]Fetching on tasks..."):
            try:
                if state in [self.BOTH, "open"]:
                    self._resolve(
                        type,
                        self.gh.search_issues(
                            "",
                            state="open",
                            author=author,
                            type=type,
                            created=created_range,
                        ),
                    )
                    console.log(f"open {type}'s are fetched")
                if state in [self.BOTH, "closed"]:
                    self._resolve(
                        type,
                        self.gh.search_issues(
                            "",
                            state="closed",
                            author=author,
                            type=type,
                            created=created_range,
                        ),
                    )
                    console.log(f"closed {type}'s are fetched")

            except Exception as e:
                raise GithubException(e)
