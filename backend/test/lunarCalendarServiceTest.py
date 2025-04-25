import datetime

from backend.services.lunarCalendarService import get_lunarCalendar


def date_test():
    date_info = get_lunarCalendar(datetime.datetime.now() + datetime.timedelta(days=0))
    print(f"Lunar date：{date_info['lunar']}")
    print(f"Advisable：{date_info['good']}")
    print(f"Inadvisable：{date_info['bad']}")

if __name__ == "__main__":
    date_test()