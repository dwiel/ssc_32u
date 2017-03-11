IMAGE=ssc_32u

.PHONY: build run

clean:
	@rm -f .*.swp .*.swo
	@rm -f *.pyc

build:
	docker build -f=Dockerfile -t=${IMAGE} .

run: build
	# mount a log file directory that is custom named to this image and
	# date
	docker run --rm -it ${IMAGE}

shell: build
	docker run --rm -it ${IMAGE} /bin/bash

build_test: build
	docker build -f=Dockerfile.test -t=${IMAGE}_test .

test: build_test
	docker run --rm -t ${IMAGE}_test

build_joystick: build
	docker build -f=Dockerfile.joystick -t=${IMAGE}_joystick .

joystick: build_joystick
	docker run --rm -t --device=/dev/ttyUSB0 ${IMAGE}_joystick
