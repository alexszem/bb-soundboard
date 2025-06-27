from backend.crud.usage import get_usage as get_usage_crud, get_usages_by_name as get_usages_by_name_crud, add_usage as add_usage_crud, edit_usage as edit_usage_crud, delete_usage as delete_usage_crud, get_all_usages as get_all_usages_crud
from backend.crud.snippet import get_snippet
from .snippet import play_snippet
import random

# Usage service layer
def add_new_usage(snippet_id: int, usage_name: str):
    # Validate snippet exists before adding usage
    snippet = get_snippet(snippet_id)
    if not snippet:
        raise ValueError("Snippet does not exist.")
    return add_usage_crud(snippet_id, usage_name)

def edit_existing_usage(usage_id: int, usage_name: str):
    edit_usage_crud(usage_id, usage_name)

def delete_existing_usage(usage_id: int):
    delete_usage_crud(usage_id)

def play_random_snippet_by_usage(usage_name: str):
    usages = get_usages_by_name_crud(usage_name)
    if not usages:
        raise ValueError("No snippets found for this usage.")
    random_usage = random.choice(usages)
    play_snippet(random_usage['snippet_id'])

def get_usage(usage_id: int):
    return get_usage_crud(usage_id)

def get_all_usages():
    return get_all_usages_crud()