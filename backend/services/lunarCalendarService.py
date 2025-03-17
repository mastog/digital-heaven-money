import datetime
import cnlunar

from backend.services.translateService import replace_words_list, replace_words


def get_lunarCalendar(datetime):

    lunar_date = cnlunar.Lunar(datetime, godType='8char')

    return {
        "date": lunar_date.date,
        "lunar": str(lunar_date.lunarYear)+"-"+ str(lunar_date.lunarMonth)+"-"+ str(lunar_date.lunarDay)+" "+ ('leap' if lunar_date.isLunarLeapMonth else ''),
        "holiday": replace_words((lunar_date.get_legalHolidays() + "," if lunar_date.get_legalHolidays() else "") + lunar_date.get_otherHolidays()),
        "star": replace_words(lunar_date.starZodiac),
        "good": replace_words_list(lunar_date.goodThing),
        "bad": replace_words_list(lunar_date.badThing)
    }