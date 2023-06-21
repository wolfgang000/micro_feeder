from .main import app
from celery.schedules import crontab


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s("hello"), name="add every 10")

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, test.s("hello"), name="add every 30")

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s("world"), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s("Happy Mondays!"),
    )


@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    z = x + y
    print(z)
    return z


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
