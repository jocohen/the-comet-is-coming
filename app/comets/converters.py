from datetime import date


class DateConverter:
    regex = "[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])"

    def to_python(self, value: str):
        return date.fromisoformat(value)

    def to_url(self, value: date):
        return value.isoformat()
