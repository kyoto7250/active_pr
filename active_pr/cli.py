import argparse
import datetime
import logging
import os
import re

from active_pr.active import ActiveReporter
from active_pr.api import GithubAPI
from active_pr.version import VERSION

logger = logging.Logger(__name__)
ERROR_CODE: int = 1


def _a_year_ago(today: datetime.date) -> str:
    """
    >>> import datetime
    >>> dt = datetime.datetime(2020, 1, 1)
    >>> _a_year_ago(dt)
    '2019-01-01'
    >>> dt = datetime.datetime(2021, 1, 1)
    >>> _a_year_ago(dt)
    '2020-01-01'
    >>> dt = datetime.datetime(2020, 2, 29)
    >>> _a_year_ago(dt)
    '2019-02-28'
    """
    month = today.month
    day = today.day
    year = today.year

    if month == 2 and day == 29:
        day -= 1

    return (datetime.datetime(year - 1, month, day)).strftime("%Y-%m-%d")


def _valid_date(date: str) -> bool:
    """
    >>> _valid_date('2020-01-01')
    True
    >>> _valid_date('20000-01-01')
    False
    >>> _valid_date('2000-100-01')
    False
    >>> _valid_date('2000-12-100')
    False
    """
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, date))


def _parse_args():
    today = datetime.date.today()
    parser = argparse.ArgumentParser(
        prog="active_pr", description="The parser of active_pr"
    )
    parser.add_argument(
        "-a",
        "--author",
        required=True,
        metavar="username",
        type=str,
        help="(required) an author' name of the search",
    )
    parser.add_argument(
        "-b",
        "--begin",
        default=_a_year_ago(today),
        metavar="YYYY-MM-DD",
        type=str,
        help="a start day of the search",
    )
    parser.add_argument(
        "-e",
        "--end",
        default=today.strftime("%Y-%m-%d"),
        metavar="YYYY-MM-DD",
        type=str,
        help="a end day of the search",
    )
    parser.add_argument(
        "-t",
        "--type",
        default=GithubAPI.BOTH,
        choices=["pr", "issue", GithubAPI.BOTH],
        help="kinds of the action's type",
    )
    parser.add_argument(
        "-s",
        "--state",
        default=GithubAPI.BOTH,
        choices=["closed", "open", GithubAPI.BOTH],
        help="kinds of the action's status",
    )
    parser.add_argument(
        "-g",
        "--github-token",
        metavar="github_xxxxxx",
        default=os.getenv("GITHUB_TOKEN"),
        help="an access token of the github. see: https://github.com/settings/tokens",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"active_pr (version {VERSION})",
        help="show version and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if not _valid_date(args.begin):
        logger.error(
            f"--begin {args.begin} is invalid format. valid format is `YYYY-MM-DD`"
        )
        exit(ERROR_CODE)

    if not _valid_date(args.end):
        logger.error(
            f"--end {args.end} is invalid format. valid format is `YYYY-MM-DD`"
        )
        exit(ERROR_CODE)

    fetcher = GithubAPI(args)
    if err := fetcher():
        logger.error(str(err))
        exit(int(err))

    print(ActiveReporter.report(fetcher.prs + fetcher.issues))


if __name__ == "__main__":
    main()
