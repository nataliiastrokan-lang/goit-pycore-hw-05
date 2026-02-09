def caching_fibonacci():
    """
    Creates a Fibonacci function with caching using closure.
    """
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":    
    fib = caching_fibonacci()
    print(fib(10))  # Output: 55    
    print(fib(15))  # Output: 610