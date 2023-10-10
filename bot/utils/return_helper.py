def helper(mongo_return) -> dict:
    """
    Helper function to return a dict of the mongo return.
    """
    return {
        "id": str(mongo_return["_id"]),
        "guess": mongo_return["lhguess"],
        "guessedBy": mongo_return["guessedBy"],
    }
