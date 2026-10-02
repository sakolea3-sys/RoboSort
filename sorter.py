def sort_object(object_type):
    if object_type == "A":
        print("Object A → Left")
        return "left"

    elif object_type == "B":
        print("Object B → Right")
        return "right"

    else:
        print("Unknown object → Reject")
        return "reject"