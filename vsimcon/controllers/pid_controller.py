from typing import Callable
from .abstract_controller import AbstractController


class PIDController(AbstractController):
    """PID Controller
    """

    def __init__(self,
                 p: float = 0.,
                 i: float = 0.,
                 d: float = 0.,
                 target_value: float = 0.,
                 inverse=False):

        self.kp = p
        self.ki = i
        self.kd = d

        self.set_point = target_value
        self.sample_time = 0.00
        self.current_time = 0
        self.last_time = self.current_time

        self.value_getter = lambda x: 0

        self.inverse = inverse

        self.reset()

    def reset(self):
        """Clears PID computations and coefficients"""

        self.p_term = 0.0
        self.i_term = 0.0
        self.d_term = 0.0
        self.p_term_history = []
        self.i_term_history = []
        self.d_term_history = []
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output_val = 0.0

    def update(self, dt: float):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        target = self.value_getter()
        error = self.set_point - target
        if self.inverse:
            error *= -1

        delta_time = dt
        delta_error = error - self.last_error

        self.p_term_history.append(self.p_term)
        self.i_term_history.append(self.i_term)
        self.d_term_history.append(self.d_term)

        self.p_term = self.kp * error
        self.i_term += error * delta_time

        if (self.i_term < -self.windup_guard):
            self.i_term = -self.windup_guard
        elif (self.i_term > self.windup_guard):
            self.i_term = self.windup_guard

        self.d_term = 0.0
        if delta_time > 0:
            self.d_term = delta_error / delta_time

        # Remember last error for next calculation
        self.last_error = error

        self.output_val = self.p_term + (self.ki * self.i_term) + (self.kd * self.d_term)

    @property
    def output(self):
        return self.output_val

    def connect(self, value_getter: Callable[[float], float]):
        self.value_getter = value_getter

    def set_kp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.kp = proportional_gain

    def set_ki(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.ki = integral_gain

    def set_kd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.kd = derivative_gain

    def set_windup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def set_sample_time(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time
