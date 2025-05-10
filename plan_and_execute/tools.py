from langchain_community.tools import DuckDuckGoSearchRun


class Tools:
    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    def get_all(self):
        return [
            self.search
        ]