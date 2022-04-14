class Month(str):
    """
    Month with the year corresponding to it.
    It is epected in the format of %Y-%m.
    """

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")

        splits = v.strip().split("-", 1)

        if len(splits) != 2:
            raise ValueError("Month Format should be: %Y-%m")

        for s in splits:
            if not s.isdecimal():
                raise ValueError(f"{s} is not a number.")

        year, month = tuple(map(int, splits))

        # Twitter was established in 2006
        if year < 2006 or year > 2100:
            raise ValueError(f"{year} is not a valid year.")

        if month < 1 or month > 12:
            raise ValueError(f"{month} is not a valid month.")

        # you could also return a string here pydantic won't care
        # but you could end up with some confusion since the
        # value's type won't match the type annotation exactly
        return cls(f"{year}-{month:02}")

    def __repr__(self):
        return f"Month: {super().__repr__()}"
