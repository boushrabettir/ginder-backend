from dataclasses import dataclass
from typing import List, Dict
from github import Github, Auth, Set
import random
import requests
import json
from utils import Error

# Holds the max amount of languages
MAX_LANGUAGE_LENGTH = 3

# Holds the max amount of github projects
MAX_GH_PROJECT_LENGTH = 18


@dataclass
class OpenSource:
    """Data class holding data for an open source object"""

    # Respective id
    id: int

    # Name of repository
    name: str

    # Profile picture link
    pfp_link: str

    # Description
    description: str

    # Link to repository
    link: str

    # Owners Username
    username: str

    # Language(s) used
    languages: List[str]

    # Stars on project
    stars: float

    # Total forks on the repo
    forks: int

    # Total open contributers
    contributers: int

    # Total number of followers of user
    followers: int


@dataclass
class OpenSourceUtilizer:
    """Holds a list of Open Source objects"""

    open_source_list: List[OpenSource]


def random_lang_list(lang: List[str]) -> List[str]:
    """Returns a list of 3 random languages"""

    # Holding the languages of the list
    lang_list_query = []

    while len(lang_list_query) <= MAX_LANGUAGE_LENGTH:
        # Choose a random language from the list
        chosen_language = random.choice(lang)

        if chosen_language not in lang_list_query:
            lang_list_query.append(chosen_language.lower())

    return lang_list_query


def request_user_lang_list(user_languages: List[str]) -> List[str]:
    """Retrieves 3 most used languages by the user"""

    # Holds default languages if the length of user languages is 0
    DEFAULT_LANGUAGES = [
        "rust",
        "python",
        "java",
        "javascript",
        "php",
        "html",
        "css",
        "c++",
        "c#",
    ]

    # If there are no top languages, fetch 3 from the default list
    if len(user_languages) == 0:
        return random_lang_list(DEFAULT_LANGUAGES)

    # Fetch 3 random languages from the user language list
    if len(user_languages) > MAX_LANGUAGE_LENGTH:
        return random_lang_list(user_languages)

    # Fetch the remainder languages if the value is less than the MAX_LANGUAGE_LENGTH
    if len(user_languages) < MAX_LANGUAGE_LENGTH:
        languages_required = abs(len(user_languages) - 3)

        for _ in range(languages_required):
            chosen_language = random.choice(DEFAULT_LANGUAGES)
            user_languages.append(chosen_language)
            DEFAULT_LANGUAGES.remove(chosen_language)

        return user_languages

    # Return the user language list if the length is equal to MAX_LANGUAGE_LENGTH
    return user_languages


def retrieve_top_repo_languages(repository) -> List[str]:
    """Retrieves up to three top languages from the current repository"""

    languages_data = repository.get_languages()

    all_languages = sorted(
        languages_data.keys(), key=lambda x: languages_data[x], reverse=True
    )

    return all_languages[:3]


def request_github_pfp(headers: Dict[str, any], username: str) -> str:
    """Retrieves users Github profile picture link"""

    response = requests.get(f"https://api.github.com/users/{username}", headers=headers)

    try:
        json_response = response.json()

        return json_response["avatar_url"]
    except ValueError as e:
        return json({"error": f"Invalid response, please try again. {e}"}), 500

def query_project(id: str, auth_token: str) -> any:
    """Queries a specific project given their id."""

    headers= {
        "Authorization": f"Bearer {auth_token}"
    }

    response = requests.get(f"https://api.github.com/repos/{id}", headers=headers)

    if not response or type(response) == None:
        raise Error().return_type_none()

    try:
        json_response = response.json()

        return json_response
    except ValueError as e:
        return json({"error": f"Invalid response, please try again. {e}"}), 500

def request_github_projects(
    user_languages: List[str], auth_token: str, all_swipes: Set[bool]
) -> List[OpenSource]:
    """Requests Github Repository information"""

    # Create Open Source Utilizer instance
    open_source_utilizer = OpenSourceUtilizer([])

    auth = Auth.Token(auth_token)

    # Create a github instance
    gh = Github(auth=auth)

    # Hold the user languages in a query variable
    query = user_languages

    # Index variable to traverse through the query list
    indx = 0

    repositories = gh.search_repositories(f"topic:{query[indx]}")

    for repository in repositories:
        id = repository.id
        name = repository.name
        pfp_link = request_github_pfp(
            {"Authorization": f"Bearer {auth_token}"}, repository.owner.login
        )
        description = repository.description
        link = repository.html_url
        username = repository.owner.login
        languages = retrieve_top_repo_languages(repository)
        stars = repository.stargazers_count
        forks = repository.forks
        contributers = repository.get_contributors(anon="true").totalCount
        followers = repository.owner.get_followers().totalCount

        # Create Open Source instance
        open_source_project = OpenSource(
            id,
            name,
            pfp_link,
            description,
            link,
            username,
            languages,
            stars,
            forks,
            contributers,
            followers,
        )

        # Determine whether or not this project has been seen already
        if all_swipes:
            if str(repository.id) not in all_swipes:
                # Add current object to the finalized list
                open_source_utilizer.open_source_list.append(open_source_project)
        else:
            open_source_utilizer.open_source_list.append(open_source_project)

        # Continue adding more projects until the list is at max length
        if len(open_source_utilizer.open_source_list) == MAX_GH_PROJECT_LENGTH:
            break

        # Increase to the next language if there is an even amount
        if (
            len(open_source_utilizer.open_source_list) / 6
            == len(open_source_utilizer.open_source_list) // 6
        ):
            indx += 1

    return open_source_utilizer.open_source_list