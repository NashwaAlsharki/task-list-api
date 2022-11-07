from flask import abort, make_response

# check that id is an integer and that it exists
def get_by_id(cls, id):
    try:
        int(id)
    except ValueError:
        return abort(make_response({"message": f"{id} is not a valid id"}, 400))
    
    model = cls.query.get(id)
    if not model:
        return abort(make_response({"message": f"{id} not found"}, 404))

    return model
