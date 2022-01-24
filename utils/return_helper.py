def _helper(mongo_return) -> dict:
    """
    The _helper function takes the mongo_return and returns a dictionary with the id, guess, and time.

    :param mongo_return: Used to store the data returned from the MongoDB query.
    :return: a dictionary containing the document's id and lhguess.
    
    """
    return {
        "id": str(mongo_return["_id"]),
        "guess": mongo_return["lhguess"],
        "guessedBy": mongo_return["guessedBy"],
    }
