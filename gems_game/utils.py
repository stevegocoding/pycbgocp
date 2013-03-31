import time
import pyglet

class State(object):
    exit_name = "EXIT"
    enter_name = "ENTER"
    changed_name = "CHANGED"

    def __init__(self, id = "machine"):
        self.id = id;
        self.parent = None
        self.children = {}
        self.data = {}
        self.counter = 0
        self.tick = 0

        self.current_state = None
        self.last_state = None

        self.enter_func = None
        self.process_func = None
        self.exit_func = None
        self.draw_func = None

    def assign(self, d):
        self.__dict__.update(d)

    def add_state(self, state):
        state.parent = self
        self.children[state.id] = state

    def set_state(self, id, data):
        self.set_state_ex(id, data, False)

    def set_state_ex(self, id, data, is_return):
        if type(id) is not str:
            print("id is not str")
            return None

        new_state = self.children[id]
        if new_state is None:
            return None

        if is_return:
            data = new_state.data
        elif data is None:
            data = {}
            new_state.data = data

        if self.current_state is not None:
            if self.current_state.exit_func is not None:
                self.current_state.exit_func(self.current_state)

        self.last_state = self.current_state 
        self.current_state = new_state

        if not is_return:
            if data is not None and data.get("return_state", None) is not None:
                self.current_state.return_state = self.children[data.return_state]
            else:
                self.current_state.return_state = None

        self.current_state.tick = 0
        if (self.current_state.enter_func is not None):
            self.current_state.enter_func(self.current_state)

        return self.current_state

    def process(self):
        if self.current_state is None:
            return None
        self.current_state.process_func(self.current_state)
        self.current_state.tick += 1

    def exit(self):
        if self.current_state is not None and \
            self.current_state.exit_func is not None:
                self.current_state.exit_func(self.current_state)


class FixedStepLoop(object):
    """
    A fixed time step loop for pyglet.
    """
    def __init__(self, update_function, step, max_step):
        self.update_function = update_function;
        self.step = step;
        self.max_step = max_step;
        self.simulation_time = 0.0 - self.step;
        self.real_time = 0.0
        self.frame_time = 0.0
        self.step_fraction = 0.0

    def tick(self, T):
        self.real_time += T
        self.frame_time += T

        if (T > self.max_step):
            self.simulation_time = self.real_time - self.max_step;

        while self.simulation_time <= self.real_time:
            self.update_function(self.step)
            self.simulation_time += self.step;

        self.step_fraction = self.frame_time / self.step
        self.frame_time = 0.0

class FPSSync(object):

    def __init__(self, fps):
        self.fps = fps
        self.last_tick = 0
        self.tick = 0
        self.time_stamp = 0
        self.real_time = 0
        self.start()

    def start(self):
        self.time_stamp = time.time()
        self.real_time = self.time_stamp

    def get_frame_count(self, T):
        self.real_time += T
        this_tick = (self.real_time - self.time_stamp) * self.fps
        self.last_tick = self.tick
        self.tick = this_tick
        return self.tick - self.last_tick
