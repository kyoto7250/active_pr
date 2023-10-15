class GithubException(Exception):
    ERROR_CODE = 1
    MESSAGE = "Internal Error in active_pr"

    def __int__(self):
        return self.ERROR_CODE

    def __str__(self):
        return self.MESSAGE
