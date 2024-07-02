from github import Github, Auth
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Error:
    """Custom error class for custom error messages."""

    @staticmethod
    def request_unsuccessful(project_data: Dict[str, str | int] | None,
                             return_code: int) -> None:
        print(f"Insertion request for project '{project_data["id"] | None}' 
              was unsuccessful.
              \nRETURN CODE: '{return_code}'.\n")
        
    @staticmethod
    def return_type_none() -> None:
        print("Request returned type 'NONE'. Please verify query/request and try again.\n")

    @staticmethod
    def deletion_error(id: str) -> None:
        print(f"Unable to delete project {id} from database. Please try again.\n")
        
def fetch_user_languages(auth_token: str) -> List[str]:
    """Fetches users top languages"""

    auth = Auth.Token(auth_token)
    gh = Github(auth=auth)

    unique_languages = {}

    user = gh.get_user()

    for indx, repository in enumerate(user.get_repos(type="public")):
        if indx == 10:
            break

        if repository.owner.login == user.login:
            all_languages = repository.get_languages()
            all_languages = [key for key in all_languages.keys()]

            for lang in all_languages:
                if lang not in unique_languages:
                    unique_languages[lang] = 1
                else:
                    unique_languages[lang] += 1

    # Sort list again in descending order
    unique_languages_list = sorted(
        unique_languages.keys(), key=lambda x: unique_languages[x], reverse=True
    )

    return unique_languages_list