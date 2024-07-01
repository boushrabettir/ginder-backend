import os
from supabase import create_client, Client
from dataclasses import dataclass

@dataclass
class SupaBase:
    """Attributes to create an instance of supabase project/user database"""

    URL: str = os.environ.get("SUPABASE_URL")
    KEY: str = os.environ.get("SUPABSE_KEY")
    SUPABASE: Client = create_client(URL, KEY)


SUPABASE_INSTANCE = SupaBase().SUPABASE

def create_table() -> None:
    pass

def insert_project_data() -> None:
    pass

def insert_user_data() -> None:
    pass

def update_data() -> None:
    pass

def delete_data_list() -> None:
    pass

def query_data() -> any:
    pass
