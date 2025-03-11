import datetime
import cnlunar

translation_dict = {
    '出行': 'travelling',
    '宴会': 'banquet',
    '上官': 'official business',
    '进人口': 'add household members',
    '经络': 'acupuncture',
    '纳财': 'accept wealth',
    '牧养': 'herding',
    '覃恩': 'bestow grace',
    '临政': 'administer governance',
    '庆赐': 'celebration gifts',
    '举正直': 'promote integrity',
    '立券交易': 'sign contracts',
    '纳畜': 'purchase livestock',
    '雪冤': 'clear grievances',
    '宣政事': 'proclaim decrees',
    '施恩': 'grant favors',
    '裁制': 'tailor clothes',
    '酝酿': 'brew alcohol',
    '颁诏': 'issue edicts',
    '恤孤茕': 'care for orphans',
    '招贤': 'recruit talents',
    '搬移': 'relocation',
    '剃头': 'haircut',
    '修置产室': 'renovate delivery room',
    '开渠': 'dig canals',
    '穿井': 'dig well',
    '平治道涂': 'level roads',
    '破屋坏垣': 'demolish walls',
    '伐木': 'cut trees',
    '畋猎': 'hunting',
    '启攒': 'exhume remains',
    '乘船渡水': 'boat crossing',
    '筑堤防': 'build dams',
    '苫盖': 'thatch roofing',
    '整手足甲': 'trim nails',
    '取鱼': 'catch fish',
    '补垣': 'repair walls',
    '整容': 'plastic surgery',
    '开仓': 'open granary',
    '修饰垣墙': 'decorate walls'
}

def translate_terms(terms):
    return [translation_dict.get(term, f"{term}(untranslated)") for term in terms]

def get_lunarCalendar():
    lunar_date = cnlunar.Lunar(datetime.datetime.now(), godType='8char')
    
    return {
        "date": lunar_date.date,
        "lunar": (lunar_date.lunarYear, lunar_date.lunarMonth, lunar_date.lunarDay, 'leap' if lunar_date.isLunarLeapMonth else 'not leap'),
        "holiday": (lunar_date.get_legalHolidays(), lunar_date.get_otherHolidays(), lunar_date.get_otherLunarHolidays()),
        "star": lunar_date.starZodiac,
        "good": translate_terms(lunar_date.goodThing),
        "bad": translate_terms(lunar_date.badThing)
    }

def date_test():
    date_info = get_lunarCalendar()
    print(f"Gregorian calendar date：{date_info['date']}")
    print(f"Lunar date：{date_info['lunar']}")
    print(f"Star sign：{date_info['star']}")
    print("Advisable：")
    print("\n".join(date_info['good']))
    print("\nInadvisable：")
    print("\n".join(date_info['bad']))

if __name__ == "__main__":
    date_test()

