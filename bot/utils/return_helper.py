def helper(mongo_return) -> dict:
    return {
        "id": str(mongo_return["_id"]),
        "guess": mongo_return["lhguess"],
        "guessedBy": mongo_return["guessedBy"],
    }
