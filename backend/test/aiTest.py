from backend.services.aiService import connect, communicate


def ai_test(name, description, request):
    print(communicate(name, description, request))

if __name__ == "__main__":
    ai_test("Kobe Bryant","Kobe Bryant, a basketball legend, was born in 1978. Drafted in 1996, he spent 20 seasons with the Lakers, winning 5 championships. His Mamba Mentality inspired many.","Do you know shaq?")