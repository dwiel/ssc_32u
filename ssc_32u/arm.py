import time
import random
from pylibftdi import Device

# min, max, home
BOUNDS = {
    0: [1250, 1950, 1600],
    1: [850, 2500, 1000],
    # 2: [1200, 2500, 1200],
    2: [550, 1000, 600],
    3: [700, 2500, 1900],  # 1700 is center
    # 4: [1200, 2450, 1200],
}


class Arm(object):
    def __init__(self, fps, velocity_scale=200, dry_run=False, verbose=False):
        """
        fps: the frames per second that set_multi_velocity must be called to
        keep smooth motion.
        velocity_scale: convert unitless range (-1, 1) to velocity in
        microseconds / second
        """
        if not dry_run:
            self.dev = Device(mode='t')
            self.dev.baudrate = 9600

        self.default_speed = 600
        self.positions = self._home_position()

        self.fps = fps
        self.velocity_scale = velocity_scale

        # position scale is the velocity in (microseconds / second) / FPS to get
        # microseconds per frame
        self.position_scale = velocity_scale / self.fps

        self.dry_run = dry_run
        self.verbose = verbose

    def _home_position(self):
        return {i: BOUNDS[i][2] for i in BOUNDS}

    def _bound_position(self, axis, position):
        if position > BOUNDS[axis][1]:
            return BOUNDS[axis][1]
        if position < BOUNDS[axis][0]:
            return BOUNDS[axis][0]
        return position

    def set_position(self, axis, position, speed=None, time=None):
        """
        pos: position pulse width in microseconds
        speed: microseconds per second
        time: time in milliseconds to execute motion to `pos`
        """

        self.positions[axis] = self._bound_position(axis, position)

        if speed is None and time is None:
            speed = self.default_speed

        if self.verbose:
            print('axis=', axis)
            print('position=', position)
            print('speed=', speed)
            print('time=', time)

        if self.dry_run:
            return

        if speed:
            self.dev.write(
                '#{axis}P{position}S{speed}\r'.format(
                    axis=axis, position=position, speed=speed
                )
            )
        else:
            self.dev.write(
                '#{axis}P{position}T{time}\r'.format(
                    axis=axis, position=position, time=time
                )
            )

    def set_positions(self, positions, speeds=None, scaled=False):
        if scaled:
            positions = {
                axis: self.scaled_position(axis, position)
                for axis, position in positions.items()
            }

        for axis in positions:
            positions[axis] = self._bound_position(axis, positions[axis])
            self.positions[axis] = positions[axis]

        if speeds is None:
            speeds = {axis: self.default_speed for axis in positions}

        if self.verbose:
            print('positions', positions)
            print('speeds   ', speeds)

        if self.dry_run:
            return

        self.dev.write(
            ''.join(
                '#{axis}P{pos}S{speed}'.format(
                    axis=axis,
                    pos=positions[axis],
                    speed=speeds[axis],
                ) for axis in positions
            ) + '\r'
        )

    def scaled_position(self, axis, position):
        if position < 0 or position > 1:
            raise ValueError((
                'position expected to be within 0 and 1.  found: {}'
            ).format(position))

        return BOUNDS[axis][0] + position * (BOUNDS[axis][1] - BOUNDS[axis][0])

    def set_scaled_position(self, axis, position, speed=None):
        self.set_position(
            axis, self.scaled_position(axis, position), speed=speed
        )

    def set_relative_position(self, axis, position_delta, speed=None):
        self.positions[axis] += position_delta
        self.set_position(axis, self.positions[axis], speed=speed)

    def set_velocities(self, velocities):
        """
        Set velocity of all servos in arm.

        set_multi_velocity must be called once every self.fps
        """
        if set(velocities.keys()) != set(self.positions.keys()):
            raise ValueError((
                'velocities.keys must match self.positions.keys:\n'
                '  velocities.keys(): {}\n'
                '  self.position.keys(): {}\n'
            ).format(velocities.keys(), self.positions.keys()))

        if not any(v != 0 for v in velocities.values()):
            return

        self.set_positions(
            {
                axis: self.positions[axis] + (velocity * self.position_scale)
                for axis, velocity in velocities.items()
            },
            {
                axis: max(abs(velocity * self.velocity_scale), 100)
                for axis, velocity in velocities.items()
            },
        )

    def set_velocity(self, axis, velocity):
        velocity *= 10
        self.set_position(
            axis,
            self.positions[axis] + velocity * self.position_scale,
            speed=max(abs(velocity) * self.velocity_scale, 5)
        )

    def go_home(self):
        self.set_positions(self._home_position())

    def go_random(self):
        for axis in BOUNDS:
            self.set_position(
                axis, random.randrange(BOUNDS[axis][0], BOUNDS[axis][1], 1)
            )


if __name__ == '__main__':
    arm = Arm()

    # dev.write('#0P500S400\r')
    # time.sleep(3)

    # dev.write('#0P1600S400\r')
    # dev.write('#1P1000S400\r')
    # dev.write('#2P1200S400\r')
    # dev.write('#3P1500S400\r')
    # dev.write('#4P1200S400\r')

    arm.go_home()

    try:
        a = [BOUNDS[i][2] for i in range(len(BOUNDS))]

        import sys
        while True:
            c = sys.stdin.read(1)
            if c == 'a':
                a[0] += 50
                arm.set_position(0, a[0], 200)
            elif c == 'z':
                a[0] -= 50
                arm.set_position(0, a[0], 200)

    except KeyboardInterrupt as e:
        pass

    arm.go_home()
