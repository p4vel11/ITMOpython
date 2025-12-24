
try:
    import integrate_nogil
    print("✅ Модуль integrate_nogil успешно импортирован!")
    print("Функции:", dir(integrate_nogil))
except Exception as e:
    print("❌ Ошибка:", e)