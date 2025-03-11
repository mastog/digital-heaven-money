import datetime
import cnlunar

def get_lunarCalendar():

    lunar_date = cnlunar.Lunar(datetime.datetime.now(), godType='8char')

    return {
        "date": lunar_date.date,
        "lunar": (lunar_date.lunarYear, lunar_date.lunarMonth, lunar_date.lunarDay, 'leap' if lunar_date.isLunarLeapMonth else ''),
        "holiday": (lunar_date.get_legalHolidays(), lunar_date.get_otherHolidays()),
        "star": lunar_date.starZodiac,
        "good": lunar_date.goodThing,
        "bad": lunar_date.badThing
    }


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