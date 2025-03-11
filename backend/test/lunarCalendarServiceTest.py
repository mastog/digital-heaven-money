from backend.services.lunarCalendarService import get_lunarCalendar


def date_test():
    date_info = get_lunarCalendar()
    print(f"Gregorian calendar date：{date_info['date']}")
    print(f"Lunar date：{date_info['lunar']}")
    print(f"Holiday：{date_info['holiday']}")
    print(f"Star sign：{date_info['star']}")
    print(f"Advisable：{date_info['good']}")
    print(f"Inadvisable：{date_info['bad']}")

if __name__ == "__main__":
    date_test()