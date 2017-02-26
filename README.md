This package is intended to provide some useful abstraction over the low
level [pylibftdi](https://pypi.python.org/pypi/pylibftdi) interface for
controlling robot arms driven by the
[SSC-32U](http://www.lynxmotion.com/p-1032-ssc-32u-usb-servo-controller.aspx)
controller.

The interface is provided with a class Arm.  For now, check out the code
to see what methods are available.  A simple example:

```python
arm = Arm(fps=10, velocity_scale=200)

# put all arm axes in their `home` position
arm.go_home()

# set arm axes `3` to position `2000`
arm.set_position(axis=3, 2000)

# set velocity from `0` to `1`.  must be called at `arm.fps` for smooth
# operation.
arm.set_velocities({
    0: 0.1,
    1: 0.5,
    2: 1.0,
})
```
