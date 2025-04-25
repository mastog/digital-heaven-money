import datetime
import cnlunar

from backend.services.translateService import replace_words_list, replace_words


def get_lunarCalendar(datetime):

    lunar_date = cnlunar.Lunar(datetime, godType='8char')

    return {
        "lunar": str(lunar_date.lunarYear)+"-"+ str(lunar_date.lunarMonth)+"-"+ str(lunar_date.lunarDay)+" "+ ('leap' if lunar_date.isLunarLeapMonth else ''),
        "good": replace_words_list(lunar_date.goodThing),
        "bad": replace_words_list(lunar_date.badThing)
    }