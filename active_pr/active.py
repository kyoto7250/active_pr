import datetime
from dataclasses import dataclass
from typing import Optional

from tabulate import tabulate


@dataclass(order=True)
class Active:
    type: str
    url: str
    repo_name: str
    title: str
    created_at: datetime.date
    closed_at: Optional[datetime.date]


class ActiveReporter:
    @staticmethod
    def report(actives: list[Active]):
        headers: list[str] = ["repo_name", "type", "title", "created_at", "closed_at"]
        actives.sort(key=lambda f: f.created_at)
        table = [
            [
                active.repo_name,
                active.type.upper(),
                f"[{active.title}]({active.url})",
                active.created_at.strftime("%Y-%m-%d"),
                active.closed_at.strftime("%Y-%m-%d") if active.closed_at else None,
            ]
            for active in actives
        ]
        return tabulate(table, headers, tablefmt="github")
