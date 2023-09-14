import argparse
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class CreateRelease:
    def __init__(
        self,
    ) -> None:
        self.latest_release_url = "https://api.github.com/repos/alexraskin/lhbot/tags"
        self.url = f"https://api.github.com/repos/alexraskin/lhbot/releases"

    def create_release(self, version, description):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + str(os.getenv("GITHUB_PAT")),
            "X-GitHub-Api-Version": "2022-11-28",
        }

        self.data = {
            "tag_name": version,
            "target_commitish": "main",
            "name": version,
            "body": description,
            "draft": False,
            "prerelease": False,
            "generate_release_notes": False,
        }
        response = requests.post(self.url, headers=self.headers, json=self.data)
        return json.dumps(response.json(), indent=4, sort_keys=True)

    def get_release(self):
        response = requests.get(self.latest_release_url)
        return response.json()


if __name__ == "__main__":
    create_release = CreateRelease()

    print(
        f"Latest release: ", latest_release := create_release.get_release()[0]["name"]
    )
    print(
        f"New version number:",
        version_number := f"{latest_release.split('.')[0]}.{int(latest_release.split('.')[1]) + 1}",
    )

    argparse = argparse.ArgumentParser()
    argparse.add_argument("--description", help="Description of the release")
    args = argparse.parse_args()
    description = args.description

    print(create_release.create_release(version_number, description))
