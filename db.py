import os
from supabase import create_client, Client, table
from dataclasses import dataclass
import posts
from typing import List, Dict
from utils import Error

@dataclass
class SupaBase:
    """Attributes to create an instance of supabase project/user database"""

    URL: str = os.environ.get("SUPABASE_URL")
    KEY: str = os.environ.get("SUPABSE_KEY")
    SUPABASE: Client = create_client(URL, KEY)


SUPABASE_INSTANCE = SupaBase().SUPABASE
PROJECT_TABLE, USER_TABLE = "projects", "users"

def create_table() -> None:
    pass

def insert_project_data(project_list: List[posts.OpenSource]) -> None:
    """Inserts project data to table."""

    for project in project_list:

        insertion_data = {
            "id": project.id,
            "name": project.name,
            "pfp_link": project.pfp_link,
            "description": project.description,
            "link": project.link,
            "username": project.username,
            "languages": project.languages,
            "stars": project.stars,
            "forks": project.forks,
            "contributers": project.contributers,
            "followers": project.followers
        }
        
        project_table_response = (
            table(PROJECT_TABLE)
            .insert(insertion_data)
            .execute()
        )

        if project_table_response.status_code != 200:
            raise Error().request_unsuccessful(
                insertion_data,
                project_table_response.status_code
            )

def insert_user_data(user_id: str) -> None:
    """Inserts user data into table."""

    insertion_data = {
        "user_id": user_id
    }

    user_table_response = (
        table(USER_TABLE)
        .insert(insertion_data)
        .execute()
    )

    if user_table_response.status_code != 200:
        raise Error().request_unsuccessful(
            insertion_data,
            user_table_response.status_code
        )

def update_if_changed(project, project_query, type) -> None:
    """Updates project in project database if difference is detected."""
    
    if project_query["data"][type] != project[type]:
        table(PROJECT_TABLE).update({type: project_query["data"][type]}).eq("id", project["id"]).execute()

# TODO - This will be done in the background every X amount of days
def update_project_data(auth_token: str) -> None:
    """
        Update project data from database to current version
        of project for any differences.
    """

    response = table(PROJECT_TABLE).select("*").execute()
    
    for project in response["data"]:
        # Lets assume structure is project_query["data"]["XYZ"]
        project_query = posts.query_project(auth_token, project["id"])

        update_if_changed(project, project_query, "name")
        update_if_changed(project, project_query, "pfp_link")
        update_if_changed(project, project_query, "description")
        update_if_changed(project, project_query, "link")
        update_if_changed(project, project_query, "username")
        update_if_changed(project, project_query, "languages")
        update_if_changed(project, project_query, "stars")
        update_if_changed(project, project_query, "forks")
        update_if_changed(project, project_query, "contributers")
        update_if_changed(project, project_query, "followers")


def find_depricated_projects() -> List[Dict[str, str | int]]:
    """Returns a list of depricated projects."""

    response = table(PROJECT_TABLE).select("*").execute()

    # TODO- Define depricated projects. What is considered
    # a depricated project?

def delete_depricated_project_data() -> None:
    """Deletes depricated projects from project database."""

    depricated_projects = find_depricated_projects()["data"]

    #response = supabase.table('countries').delete().eq('id', 1).execute()
    for depricated_project in depricated_projects: 
        response = table(PROJECT_TABLE).delete().eq("id", depricated_project["id"])

        if response.status_code != 200:
            raise Error().deletion_error(depricated_project["id"])
        
def query_project_data() -> any:
    """Queries X amount of data from project table."""


def query_specifics() -> any:
    """Queries specific data from either table."""


# TODO - Left swipe updates (view figma)