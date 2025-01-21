##  Data Science Project - v0.0.1

### :rocket: Performance improvements
- Specify tune-cpu & add more features ([Issue #245](https://github.com))

### :sparkles: Enhancements
- Raise error instead of panic in unsupported serde ([Issue #245](https://github.com))

### :bug: Bug fixes
- Use bytemuck in slice reinterpret for Parquet ArrayChunks ([Issue #245](https://github.com))
- Remove non-existing names from __all__ ([Issue #245](https://github.com))
- Fix return type hint for LazyFrame sink methods ([Issue #245](https://github.com))
- Propagate struct outer nullability eagerly ([Issue #245](https://github.com))
- Address read_database issue with batched reads from Snowflake (#17688)
- Use ETag for HTTP file cache invalidation ([Issue #245](https://github.com))

### :books: Documentation
- Fixed default name for value_counts methods based on normalize parameter ([Issue #245](https://github.com))

### :hammer_and_wrench: Other improvements
- Fix return type hint for LazyFrame sink methods (#17698)
-Pin setuptools to fix failing CI (#17695)
-Name tests so they actually run (#17690)
-Add reduce ComputeNode in new streaming engine (#17389)


Thank you to all our team members for making this possible!