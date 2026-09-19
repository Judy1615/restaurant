from django.shortcuts import render
from django.conf import settings
from google import genai
from menu.models import MenuItem

def suggest(request):
    suggestion = None
    if request.method == 'POST':
        user_input = request.POST.get('preferences', '')

        # نجيب كل الأصناف الموجودة فعلاً في المنيو
        items = MenuItem.objects.all()
        menu_text = "\n".join(
            f"- {item.name} ({item.category.name}): {item.ingredients} - {item.price} EGP"
            for item in items
        )

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        prompt = f"""
دي قايمة الأكل الموجودة في المطعم فقط:
{menu_text}

بناءً على القايمة دي بس (متقترحيش أي حاجة مش موجودة فيها)، اقترحي وجبة واحدة تناسب طلب العميل ده: "{user_input}"
رد باسم الوجبة وسبب مختصر في جملتين بس.
"""
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            suggestion = response.text
        except Exception as e:
            suggestion = f"حصل خطأ: {e}"
    return render(request, 'ai_suggest/suggest.html', {'suggestion': suggestion})