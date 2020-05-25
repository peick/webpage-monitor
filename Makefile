build-image:
	docker build -t webpage-monitor .

clean:
	find -name "__pycache__" | xargs -r rm -rf
