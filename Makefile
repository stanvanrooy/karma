.PHONY: 

api.test:
	cd api; ptw

api.shell:
	cd api; poetry shell

api.up:
	cd api; python main.py

ui.up:
	cd ui; npm run start

