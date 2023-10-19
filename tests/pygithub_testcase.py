# thanks: https://gist.github.com/edthrn/ce28cb1a8a86caab0129a302d8c2bc33
from unittest import TestCase

import httpretty


class MockJson:
    def __init__(self, path):
        self.path = path
        self.content = ""

    def __get__(self, instance, owner):
        if instance is None:
            return owner
        with open(self.path) as file:
            setattr(instance, self.content, file.read())

        return getattr(instance, self.content)


class MockGithubResponse:
    closed_issue = MockJson("tests/fixtures/closed_issue_search_result.json")
    issue = MockJson("tests/fixtures/issue_instance.json")
    open_issue = MockJson("tests/fixtures/open_issue_search_result.json")


class PyGithubTestCase(TestCase):
    def setUp(self):
        httpretty.enable()
        httpretty.reset()

        headers = {
            "content-type": "application/json",
            "X-OAuth-Scopes": "admin:org, admin:repo_hook, repo, user",
            "X-Accepted-OAuth-Scopes": "repo",
        }

        fake = MockGithubResponse()
        response_mapping = {
            "https://api.github.com/search/issues?q=state%3Aopen+author%3Ausername+type%3Aissue+created%3A2023-03-01..2023-03-30": fake.open_issue,
            "https://api.github.com/search/issues?q=state%3Aclosed+author%3Ausername+type%3Aissue+created%3A2023-03-01..2023-03-30": fake.closed_issue,
            "https://api.github.com/repos": fake.issue,
            "https://api.github.com/repos/repo_name/example/issues/3668": fake.issue,
        }

        for url, response in response_mapping.items():
            httpretty.register_uri(
                httpretty.GET,
                url,
                response,
                adding_headers=headers,
            )

    def tearDown(self):
        httpretty.disable()
