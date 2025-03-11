import datetime
import cnlunar

from backend.services.translateService import replace_words


def get_lunarCalendar():

    lunar_date = cnlunar.Lunar(datetime.datetime.now(), godType='8char')

    return {
        "date": lunar_date.date,
        "lunar": (lunar_date.lunarYear, lunar_date.lunarMonth, lunar_date.lunarDay, 'leap' if lunar_date.isLunarLeapMonth else ''),
        "holiday": (lunar_date.get_legalHolidays(), lunar_date.get_otherHolidays()),
        "star": replace_words(lunar_date.starZodiac),
        "good": replace_words(lunar_date.goodThing),
        "bad": replace_words(lunar_date.badThing)
    }