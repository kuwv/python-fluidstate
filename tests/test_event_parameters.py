import unittest
from fluidity import StateMachine, state, transition


class Door(StateMachine):
    state('closed')
    state('open')
    initial_state = 'closed'
    transition(
        source='closed', event='open', target='open', action='open_action'
    )
    transition(
        source='open',
        event='close',
        target='closed',
        action='close_action',
    )

    def open_action(self, when, where):
        self.when = when
        self.where = where

    def close_action(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class EventParameters(unittest.TestCase):
    def test_it_pass_parameters_received_by_event_to_action(self):
        door = Door()
        door.open('now!', 'there!')
        assert hasattr(door, 'when')
        assert door.when == 'now!'
        assert hasattr(door, 'where')
        assert door.where == 'there!'

    def test_it_pass_args_and_kwargs_to_action(self):
        door = Door()
        door.open('anytime', 'anywhere')
        door.close('1', 2, object, test=9, it=8, works=7)
        assert hasattr(door, 'args')
        assert door.args == ('1', 2, object)
        assert hasattr(door, 'kwargs')
        assert door.kwargs == {'test': 9, 'it': 8, 'works': 7}


if __name__ == '__main__':
    unittest.main()