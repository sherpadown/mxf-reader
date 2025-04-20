docker.build:
	docker build --no-cache -t mxf-reader:latest .

docker.run:
	docker run -it --rm mxf-reader:latest --help

docker.run.tests:
	docker run -v "$(PWD)/tests/assets:/assets" -it --rm mxf-reader:latest -f /assets/2D.mxf
