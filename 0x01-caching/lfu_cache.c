#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 4

/**
 * struct CacheItem - Structure for a cache item.
 * @key: The key associated with the cache item.
 * @item: The item stored in the cache.
 * @usage_count: The usage count of the cache item.
 * @next: Pointer to the next cache item.
 */
typedef struct CacheItem
{
	char *key;
	void *item;
	int usage_count;
	struct CacheItem *next;
} CacheItem;

/**
 * struct LFUCache - Structure for the LFU cache.
 * @head: Pointer to the head of the linked list of cache items.
 * @size: The current size of the cache.
 */
typedef struct LFUCache
{
	CacheItem *head;
	int size;
} LFUCache;

/**
 * create_cache_item - Creates a new cache item.
 * @key: The key associated with the cache item.
 * @item: The item to store in the cache.
 *
 * Return: Pointer to the newly created cache item.
 */
CacheItem *create_cache_item(const char *key, void *item)
{
	CacheItem *new_item = (CacheItem *)malloc(sizeof(CacheItem));

	if (new_item == NULL)
	{
		return (NULL);
	}
	new_item->key = strdup(key);
	new_item->item = item;
	new_item->usage_count = 1;
	new_item->next = NULL;
	return (new_item);
}

/**
 * init_cache - Initializes the LFU cache.
 *
 * Return: Pointer to the initialized LFU cache.
 */
LFUCache *init_cache(void)
{
	LFUCache *cache = (LFUCache *)malloc(sizeof(LFUCache));

	if (cache == NULL)
	{
		return (NULL);
	}
	cache->head = NULL;
	cache->size = 0;
	return (cache);
}

/**
 * find_lfu_item - Finds the least frequently used item in the cache.
 * @cache: The LFU cache.
 *
 * Return: Pointer to the least frequently used cache item.
 */
CacheItem *find_lfu_item(LFUCache *cache)
{
	CacheItem *current = cache->head;
	CacheItem *lfu_item = current;

	while (current != NULL)
	{
		if (current->usage_count < lfu_item->usage_count)
		{
			lfu_item = current;
		}
		current = current->next;
	}
	return (lfu_item);
}

/**
 * find_cache_item - Finds an item in the cache by key.
 * @cache: The LFU cache.
 * @key: The key associated with the cache item.
 *
 * Return: Pointer to the cache item if found, NULL otherwise.
 */
CacheItem *find_cache_item(LFUCache *cache, const char *key)
{
	CacheItem *current = cache->head;

	while (current != NULL)
	{
		if (strcmp(current->key, key) == 0)
		{
			return (current);
		}
		current = current->next;
	}
	return (NULL);
}

/**
 * add_cache_item - Adds a new item to the cache.
 * @cache: The LFU cache.
 * @key: The key associated with the cache item.
 * @item: The item to store in the cache.
 *
 * Return: 0 on success, -1 on failure.
 */
int add_cache_item(LFUCache *cache, const char *key, void *item)
{
	CacheItem *new_item;

	/* If the cache is full, remove the least frequently used item */
	if (cache->size >= MAX_ITEMS)
	{
		CacheItem *lfu_item = find_lfu_item(cache);

		printf("DISCARD: %s\n", lfu_item->key);

		/* Remove the LFU item from the list */
		if (lfu_item == cache->head)
		{
			cache->head = lfu_item->next;
		}
		else
		{
			CacheItem *current = cache->head;

			while (current != NULL && current->next != lfu_item)
			{
				current = current->next;
			}
			if (current != NULL)
			{
				current->next = lfu_item->next;
			}
		}
		free(lfu_item->key);
		free(lfu_item);
		cache->size--;
	}

	/* Add the new item to the cache */
	new_item = create_cache_item(key, item);
	if (new_item == NULL)
	{
		return (-1);
	}
	new_item->next = cache->head;
	cache->head = new_item;
	cache->size++;

	return (0);
}

/**
 * put_cache - Adds an item to the cache using the LFU algorithm.
 * @cache: The LFU cache.
 * @key: The key associated with the cache item.
 * @item: The item to store in the cache.
 */
void put_cache(LFUCache *cache, const char *key, void *item)
{
	CacheItem *existing_item;

	/* Check if the item already exists in the cache */
	existing_item = find_cache_item(cache, key);
	if (existing_item != NULL)
	{
		existing_item->item = item;
		existing_item->usage_count++;
		return;
	}

	/* Add the new item to the cache */
	if (add_cache_item(cache, key, item) == -1)
	{
		fprintf(stderr, "Failed to add item to cache.\n");
	}
}

/**
 * get_cache - Gets an item from the cache by key.
 * @cache: The LFU cache.
 * @key: The key associated with the cache item.
 *
 * Return: The item if found, NULL otherwise.
 */
void *get_cache(LFUCache *cache, const char *key)
{
	CacheItem *current = cache->head;

	while (current != NULL)
	{
		if (strcmp(current->key, key) == 0)
		{
			current->usage_count++;
			return (current->item);
		}
		current = current->next;
	}
	return (NULL);
}

/**
 * free_cache - Frees the LFU cache.
 * @cache: The LFU cache.
 */
void free_cache(LFUCache *cache)
{
	CacheItem *current = cache->head;

	while (current != NULL)
	{
		CacheItem *temp = current;

		current = current->next;
		free(temp->key);
		free(temp);
	}
	free(cache);
}

/**
 * print_cache - Prints the current state of the cache.
 * @cache: The LFU cache.
 */
void print_cache(LFUCache *cache)
{
	CacheItem *current = cache->head;

	printf("Current cache:\n");
	while (current != NULL)
	{
		printf(
				"%s: %s (usage count: %d)\n", current->key,
				(char *)current->item, current->usage_count
				);
		current = current->next;
	}
}

/**
 * main - Entry point for the LFU cache example usage.
 *
 * Return: 0 on success, 1 on failure.
 */
int main(void)
{
	LFUCache *cache = init_cache();

	if (cache == NULL)
	{
		fprintf(stderr, "Failed to initialize cache.\n");
		return (1);
	}

	/* Test 1: Add items to the cache and print the cache */
	put_cache(cache, "A", "Hello");
	put_cache(cache, "B", "World");
	put_cache(cache, "C", "Holberton");
	put_cache(cache, "D", "School");
	printf("Test 1: After adding items A, B, C, D:\n");
	print_cache(cache);

	/* Test 2: Access an item and print the cache */
	printf("Test 2: Access item B: %s\n", (char *)get_cache(cache, "B"));
	print_cache(cache);

	/* Test 3: Add more items to the cache to trigger LFU eviction */
	put_cache(cache, "E", "Battery");
	printf("Test 3: After adding item E:\n");
	print_cache(cache);

	/* Test 4: Update an item and print the cache */
	put_cache(cache, "C", "Street");
	printf("Test 4: After updating item C:\n");
	print_cache(cache);

	/* Test 5: Access items and print the cache */
	printf("Test 5: Access items A, B, C:\n");
	printf("Item A: %s\n", (char *)get_cache(cache, "A"));
	printf("Item B: %s\n", (char *)get_cache(cache, "B"));
	printf("Item C: %s\n", (char *)get_cache(cache, "C"));
	print_cache(cache);

	/* Test 6: Add more items to the cache to trigger LFU eviction */
	put_cache(cache, "F", "Mission");
	put_cache(cache, "G", "San Francisco");
	put_cache(cache, "H", "H");
	put_cache(cache, "I", "I");
	printf("Test 6: After adding items F, G, H, I:\n");
	print_cache(cache);

	/* Test 7: Access items and print the cache */
	printf("Test 7: Access items I, H:\n");
	printf("Item I: %s\n", (char *)get_cache(cache, "I"));
	printf("Item H: %s\n", (char *)get_cache(cache, "H"));
	print_cache(cache);

	/* Test 8: Add more items to the cache to trigger LFU eviction */
	put_cache(cache, "J", "J");
	put_cache(cache, "K", "K");
	printf("Test 8: After adding items J, K:\n");
	print_cache(cache);

	/* Free the cache */
	free_cache(cache);
	return (0);
}
