import dramatiq

from django_dramatiq.models import Task


def test_admin_middleware_keeps_track_of_tasks(transactional_db, broker, worker):
    # Given an actor
    @dramatiq.actor
    def do_work():
        pass

    # When I send it a delayed message
    do_work.send_with_options(delay=1000)

    # Then a Task should be stored to the database
    task = Task.tasks.get()
    assert task
    assert task.status == Task.STATUS_DELAYED

    # When I join on the broker
    broker.join(do_work.queue_name)
    worker.join()

    # And reload the task
    task.refresh_from_db()

    # The the Task's status should be updated
    assert task.status == Task.STATUS_DONE


def test_admin_middleware_keeps_track_of_failed_tasks(transactional_db, broker, worker):
    # Given an actor that always fails
    @dramatiq.actor(max_retries=0)
    def do_work():
        raise RuntimeError("failed")

    # When I send it a message
    do_work.send()

    # And I join on the broker
    broker.join(do_work.queue_name)
    worker.join()

    # Then a failed Task should be stored to the database
    task = Task.tasks.get()
    assert task
    assert task.status == Task.STATUS_FAILED
