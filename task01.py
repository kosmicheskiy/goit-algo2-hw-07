import random
import time

# Клас для реалізації LRU-кешу
class LRUCache:
    def __init__(self, size):
        self.cache = {}
        self.access_order = []
        self.size = size

    def get(self, key):
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.size:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        self.cache[key] = value
        self.access_order.append(key)

    def clear_keys_with_prefix(self, prefix):
        keys_to_remove = [key for key in self.cache if key.startswith(prefix)]
        for key in keys_to_remove:
            self.access_order.remove(key)
            del self.cache[key]

# Функції без використання кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])

def update_no_cache(array, index, value):
    array[index] = value

# Функції з використанням LRU-кешу
cache = LRUCache(size=1000)

def range_sum_with_cache(array, L, R):
    key = f"range:{L}:{R}"
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R + 1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.clear_keys_with_prefix("range:")

# Тестування програми
if __name__ == "__main__":
    N, Q = 100_000, 50_000

    # Генерація масиву та запитів
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = [
        ('Range', random.randint(0, N - 1), random.randint(0, N - 1)) if random.choice([True, False]) 
        else ('Update', random.randint(0, N - 1), random.randint(1, 1000)) 
        for _ in range(Q)
    ]

    # Виконання запитів без кешування
    start_no_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            L, R = sorted((query[1], query[2]))  # Забезпечення правильного порядку
            range_sum_no_cache(array, L, R)
        elif query[0] == 'Update':
            update_no_cache(array, query[1], query[2])
    time_no_cache = time.time() - start_no_cache

    # Виконання запитів з кешуванням
    cache = LRUCache(size=1000)  # Перевизначення кешу
    start_with_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            L, R = sorted((query[1], query[2]))  # Забезпечення правильного порядку
            range_sum_with_cache(array, L, R)
        elif query[0] == 'Update':
            update_with_cache(array, query[1], query[2])
    time_with_cache = time.time() - start_with_cache

    # Результати
    print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")
