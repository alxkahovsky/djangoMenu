from django.shortcuts import render
from django.db import connection, reset_queries
import time
import functools


def query_debugger(func):
    """Функция для подсчета кол-ва запросов к БД,
    но лично я предпочитаю Silk"""
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


@query_debugger
def index(request, menu_item_slug=None):
    return render(request, 'base.html')
