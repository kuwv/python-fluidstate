import unittest

from fluidstate import (
    ForkedTransition,
    StateMachine,
    state,
    transition,
)


class LoanRequest(StateMachine):
    state('pending')
    state('analyzing')
    state('refused')
    state('accepted')
    initial_state = 'pending'
    transition(
        before='pending',
        event='analyze',
        after='analyzing',
        trigger='input_data',
    )
    transition(
        before='analyzing',
        event='forward_analysis_result',
        guard='was_loan_accepted',
        after='accepted',
    )
    transition(
        before='analyzing',
        event='forward_analysis_result',
        guard='was_loan_refused',
        after='refused',
    )

    def input_data(self, accepted=True):
        self.accepted = accepted

    def was_loan_accepted(self):
        return self.accepted or getattr(self, 'truify', False)

    def was_loan_refused(self):
        return not self.accepted or getattr(self, 'truify', False)


class FluidstateEventSupportsMultipleTransitions(unittest.TestCase):
    """Event chooses one of multiple transitions, based in their guards"""

    def test_it_selects_the_transition_having_a_passing_guard(self):
        request = LoanRequest()
        request.analyze()
        request.forward_analysis_result()
        request.state == 'accepted'

        request = LoanRequest()
        request.analyze(accepted=False)
        request.forward_analysis_result()
        request.state == 'refused'

    def test_it_raises_error_if_more_than_one_guard_passes(self):
        request = LoanRequest()
        request.analyze()
        request.truify = True
        with self.assertRaises(ForkedTransition):
            request.forward_analysis_result()
            # message="More than one transition was allowed for this event",


if __name__ == '__main__':
    unittest.main()
