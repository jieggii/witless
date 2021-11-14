def convert_size(size: str):
    if size in ["any", "любое"]:
        return 0

    elif size in ["sm", "small", "маленькое", "короткое"]:
        return 1

    elif size in ["md", "medium", "среднее"]:
        return 2

    elif size in ["lg", "large", "большое", "длинное"]:
        return 3

    else:
        raise ValueError(f"Unknown size {size}")


def remove_duplicates(array):
    return list(set(array))
