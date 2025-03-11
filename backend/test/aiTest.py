from backend.services.aiService import connect


def ai_test(request):
    print(connect(request))

if __name__ == "__main__":
    ai_test("Introduce yourself")