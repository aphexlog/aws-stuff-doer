class User:
    def __init__(
        self,
        aws_profile: str | None,
        aws_access_key: str | None,
        aws_secret_key: str | None,
        aws_session_token: str | None,
    ):
        self.aws_profile = aws_profile
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_session_token = aws_session_token

    def __str__(self):
        return f"aws_profile={self.aws_profile}, aws_access_key={self.aws_access_key}, aws_secret_key={self.aws_secret_key}, aws_session_token={self.aws_session_token}"

    def __repr__(self):
        return str(self)
