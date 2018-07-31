import datetime

import pytest

import prefect
from prefect.core import Flow, Task, Parameter
from prefect.engine import FlowRunner, signals
from prefect.engine.state import (
    Failed,
    Finished,
    Pending,
    Retrying,
    Running,
    Scheduled,
    Skipped,
    State,
    Success,
    TriggerFailed,
)
from prefect.triggers import manual_only
from prefect.utilities.tests import raise_on_exception


class SuccessTask(Task):
    def run(self):
        return 1


class AddTask(Task):
    def run(self, x, y):  # pylint: disable=W0221
        return x + y


class CountTask(Task):
    call_count = 0

    def run(self):
        self.call_count += 1
        return self.call_count


class ErrorTask(Task):
    def run(self):
        raise ValueError("custom-error-message")


class RaiseFailTask(Task):
    def run(self):
        raise prefect.engine.signals.FAIL("custom-fail-message")
        raise ValueError("custom-error-message")  # pylint: disable=W0101


class RaiseSkipTask(Task):
    def run(self):
        raise prefect.engine.signals.SKIP()
        raise ValueError()  # pylint: disable=W0101


class RaiseSuccessTask(Task):
    def run(self):
        raise prefect.engine.signals.SUCCESS()
        raise ValueError()  # pylint: disable=W0101


class RaiseRetryTask(Task):
    def run(self):
        raise prefect.engine.signals.RETRY()
        raise ValueError()  # pylint: disable=W0101


class ReturnTask(Task):
    called = False

    def run(self, x):
        if self.called is False:
            self.called = True
            raise ValueError("Must call twice.")
        return x


def test_flow_runner_runs_basic_flow_with_1_task():
    flow = prefect.Flow()
    task = SuccessTask()
    flow.add_task(task)
    flow_runner = FlowRunner(flow=flow)
    state = flow_runner.run(return_tasks=[task])
    assert state == Success(result={task: Success(result=1)})


def test_flow_runner_with_no_return_tasks():
    """
    Make sure FlowRunner accepts return_tasks=None and doesn't raise early error
    """
    flow = prefect.Flow()
    task = SuccessTask()
    flow.add_task(task)
    flow_runner = FlowRunner(flow=flow)
    assert flow_runner.run(return_tasks=None)


def test_flow_runner_with_invalid_return_tasks():
    flow = prefect.Flow()
    task = SuccessTask()
    flow.add_task(task)
    flow_runner = FlowRunner(flow=flow)
    with pytest.raises(ValueError):
        flow_runner.run(return_tasks=[1])


def test_flow_runner_runs_basic_flow_with_2_independent_tasks():
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = SuccessTask()

    flow.add_task(task1)
    flow.add_task(task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(flow_state, Success)
    assert flow_state.result[task1] == Success(result=1)
    assert flow_state.result[task2] == Success(result=1)


def test_flow_runner_runs_basic_flow_with_2_dependent_tasks():
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = SuccessTask()

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(flow_state, Success)
    assert flow_state.result[task1] == Success(result=1)
    assert flow_state.result[task2] == Success(result=1)


def test_flow_runner_runs_basic_flow_with_2_dependent_tasks_and_first_task_fails():
    flow = prefect.Flow()
    task1 = ErrorTask()
    task2 = SuccessTask()

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(flow_state, Failed)
    assert isinstance(flow_state.result[task1], Failed)
    assert isinstance(flow_state.result[task2], TriggerFailed)


def test_flow_runner_runs_flow_with_2_dependent_tasks_and_first_task_fails_and_second_has_trigger():
    flow = prefect.Flow()
    task1 = ErrorTask()
    task2 = SuccessTask(trigger=prefect.triggers.all_failed)

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(
        flow_state, Success
    )  # flow state is determined by terminal states
    assert isinstance(flow_state.result[task1], Failed)
    assert isinstance(flow_state.result[task2], Success)


def test_flow_runner_runs_basic_flow_with_2_dependent_tasks_and_first_task_fails_with_FAIL():
    flow = prefect.Flow()
    task1 = RaiseFailTask()
    task2 = SuccessTask()

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(flow_state, Failed)
    assert isinstance(flow_state.result[task1], Failed)
    assert not isinstance(flow_state.result[task1], TriggerFailed)
    assert isinstance(flow_state.result[task2], TriggerFailed)


def test_flow_runner_runs_basic_flow_with_2_dependent_tasks_and_second_task_fails():
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = ErrorTask()

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(flow_state, Failed)
    assert isinstance(flow_state.result[task1], Success)
    assert isinstance(flow_state.result[task2], Failed)


def test_flow_runner_does_not_return_task_states_when_it_doesnt_run():
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = ErrorTask()

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(
        state=Success(result=5), return_tasks=[task1, task2]
    )
    assert isinstance(flow_state, Success)
    assert flow_state.result == 5


def test_flow_run_method_returns_task_states_even_if_it_doesnt_run():
    # https://github.com/PrefectHQ/prefect/issues/19
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = ErrorTask()

    flow.add_edge(task1, task2)

    flow_state = flow.run(state=Success(), return_tasks=[task1, task2])
    assert isinstance(flow_state, Success)
    assert isinstance(flow_state.result[task1], Pending)
    assert isinstance(flow_state.result[task2], Pending)


def test_flow_runner_remains_pending_if_tasks_are_retrying():
    # https://github.com/PrefectHQ/prefect/issues/19
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = ErrorTask(max_retries=1)

    flow.add_edge(task1, task2)

    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1, task2])
    assert isinstance(flow_state, Pending)
    assert isinstance(flow_state.result[task1], Success)
    assert isinstance(flow_state.result[task2], Retrying)


def test_flow_runner_doesnt_return_by_default():
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = SuccessTask()
    flow.add_edge(task1, task2)
    res = flow.run()
    assert res.result == {}


def test_flow_runner_does_return_tasks_when_requested():
    flow = prefect.Flow()
    task1 = SuccessTask()
    task2 = SuccessTask()
    flow.add_edge(task1, task2)
    flow_state = FlowRunner(flow=flow).run(return_tasks=[task1])
    assert isinstance(flow_state, Success)
    assert isinstance(flow_state.result[task1], Success)


def test_required_parameters_must_be_provided():
    flow = prefect.Flow()
    y = prefect.Parameter("y")
    flow.add_task(y)
    flow_state = FlowRunner(flow=flow).run()
    assert isinstance(flow_state, Failed)
    assert isinstance(flow_state.message, prefect.engine.signals.FAIL)
    assert "required parameter" in str(flow_state.message).lower()


def test_missing_parameter_returns_failed_with_no_data():
    flow = prefect.Flow()
    task = AddTask()
    y = prefect.Parameter("y")
    task.set_dependencies(flow, keyword_tasks=dict(x=1, y=y))
    flow_state = FlowRunner(flow=flow).run(return_tasks=[task])
    assert isinstance(flow_state, Failed)
    assert flow_state.result is None


def test_missing_parameter_returns_failed_with_pending_tasks_if_called_from_flow():
    flow = prefect.Flow()
    task = AddTask()
    y = prefect.Parameter("y")
    task.set_dependencies(flow, keyword_tasks=dict(x=1, y=y))
    flow_state = flow.run(return_tasks=[task])
    assert isinstance(flow_state, Failed)
    assert isinstance(flow_state.result[task], Pending)


def test_missing_parameter_error_is_surfaced():
    flow = prefect.Flow()
    task = AddTask()
    y = prefect.Parameter("y")
    task.set_dependencies(flow, keyword_tasks=dict(x=1, y=y))
    msg = flow.run().message
    assert isinstance(msg, prefect.engine.signals.FAIL)
    assert "required parameter" in str(msg).lower()


class TestFlowRunner_get_pre_run_state:
    def test_runs_as_expected(self):
        flow = prefect.Flow()
        task1 = SuccessTask()
        task2 = SuccessTask()
        flow.add_edge(task1, task2)

        state = FlowRunner(flow=flow).get_pre_run_state(state=Pending())
        assert isinstance(state, Running)

    def test_raises_fail_if_required_parameters_missing(self):
        flow = prefect.Flow()
        y = prefect.Parameter("y")
        flow.add_task(y)
        flow_state = FlowRunner(flow=flow).get_pre_run_state(state=Pending())
        assert isinstance(flow_state, Failed)
        assert isinstance(flow_state.message, prefect.engine.signals.FAIL)
        assert "required parameter" in str(flow_state.message).lower()

    @pytest.mark.parametrize("state", [Success(), Failed()])
    def test_raise_dontrun_if_state_is_finished(self, state):
        flow = prefect.Flow()
        task1 = SuccessTask()
        task2 = SuccessTask()
        flow.add_edge(task1, task2)

        with pytest.raises(signals.DONTRUN) as exc:
            FlowRunner(flow=flow).get_pre_run_state(state=state)
        assert "already finished" in str(exc.value).lower()

    def test_raise_dontrun_for_unknown_state(self):
        class MyState(State):
            pass

        flow = prefect.Flow()
        task1 = SuccessTask()
        task2 = SuccessTask()
        flow.add_edge(task1, task2)

        with pytest.raises(signals.DONTRUN) as exc:
            FlowRunner(flow=flow).get_pre_run_state(state=MyState())
        assert "not ready to run" in str(exc.value).lower()


class TestFlowRunner_get_run_state:
    @pytest.mark.parametrize("state", [Pending(), Failed(), Success()])
    def test_raises_dontrun_if_not_running(self, state):
        flow = prefect.Flow()
        task1 = SuccessTask()
        task2 = SuccessTask()
        flow.add_edge(task1, task2)

        with pytest.raises(signals.DONTRUN) as exc:
            FlowRunner(flow=flow).get_run_state(state=state)
        assert "not in a running state" in str(exc.value).lower()


class TestStartTasks:
    def test_start_tasks_ignores_triggers(self):
        f = Flow()
        t1, t2 = SuccessTask(), SuccessTask()
        f.add_edge(t1, t2)
        with raise_on_exception():
            state = FlowRunner(flow=f).run(task_states={t1: Failed()}, start_tasks=[t2])
        assert isinstance(state, Success)


class TestInputCaching:
    def test_retries_use_cached_inputs(self):
        with Flow() as f:
            a = CountTask()
            b = ReturnTask(max_retries=1)
            result = b(a())

        first_state = FlowRunner(flow=f).run(return_tasks=[b])
        assert isinstance(first_state, Pending)
        with raise_on_exception():  # without caching we'd expect a KeyError
            second_state = FlowRunner(flow=f).run(
                return_tasks=[b],
                start_tasks=[b],
                task_states={b: first_state.result[b]},
            )
        assert isinstance(second_state, Success)
        assert second_state.result[b].result == 1

    def test_retries_only_uses_cache_data(self):
        with Flow() as f:
            t1 = Task()
            t2 = AddTask()
            f.add_edge(t1, t2)

        state = FlowRunner(flow=f).run(
            task_states={t2: Retrying(cached_inputs=dict(x=4, y=1))},
            start_tasks=[t2],
            return_tasks=[t2],
        )
        assert isinstance(state, Success)
        assert state.result[t2].result == 5

    def test_retries_caches_parameters_as_well(self):
        with Flow() as f:
            x = Parameter("x")
            a = ReturnTask(max_retries=1)
            result = a(x)

        first_state = FlowRunner(flow=f).run(parameters=dict(x=1), return_tasks=[a])
        assert isinstance(first_state, Pending)
        second_state = FlowRunner(flow=f).run(
            parameters=dict(x=2),
            return_tasks=[a],
            start_tasks=[a],
            task_states={a: first_state.result[a]},
        )
        assert isinstance(second_state, Success)
        assert second_state.result[a].result == 1

    def test_manual_only_trigger_caches_inputs(self):
        with Flow() as f:
            x = Parameter("x")
            inp = SuccessTask()
            t = AddTask(trigger=manual_only)
            result = t(x, inp)

        first_state = FlowRunner(flow=f).run(parameters=dict(x=11), return_tasks=[t])
        assert isinstance(first_state, Pending)
        second_state = FlowRunner(flow=f).run(
            parameters=dict(x=1),
            return_tasks=[t],
            start_tasks=[t],
            task_states={t: first_state.result[t]},
        )
        assert isinstance(second_state, Success)
        assert second_state.result[t].result == 12