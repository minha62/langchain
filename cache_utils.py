from cachetools import TTLCache

# Create a centralized cache
cache = TTLCache(maxsize=128, ttl=3600)