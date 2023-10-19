# active_pr
an active report of PRs in the github.



## install
```bash
pip install active_pr
```

## access token
We should get a reading only github token [here](https://github.com/settings/tokens?type=beta) for access, and set in our env.
```bash
export GITHUB_TOKEN=<your token>
```


## usage
```bash
export | grep "GITHUB_TOKEN"
GITHUB_TOKEN=<github token>

# search created_at='begin..end' and state is the current state.
active_pr \
    --author kyoto7250 \
    --begin 2023-04-01 \
    --end 2023-04-30 \
    --type both \
    --state closed
    # --github-token <github token>


| repo_name             | type   | title                                                                                                                | created_at   | closed_at   |
|-----------------------|--------|----------------------------------------------------------------------------------------------------------------------|--------------|-------------|
| astral-sh/ruff        | PR     | [[`flake8-simplify`] Implement `dict-get-with-none-default` (`SIM910`)](https://github.com/astral-sh/ruff/pull/3874) | 2023-04-04   | 2023-04-04  |
| astral-sh/ruff        | PR     | [Supports more cases in `SIM112`](https://github.com/astral-sh/ruff/pull/3876)                                       | 2023-04-04   | 2023-04-04  |
| dondongwon/LPMDataset | ISSUE  | [Where is the `scrape_scope` column  at `raw_video_links.csv`?](https://github.com/dondongwon/LPMDataset/issues/3)   | 2023-04-25   | 2023-06-07  |

``````


## contribute
If you have suggestions for features or improvements to the code, please feel free to create an issue or PR.
