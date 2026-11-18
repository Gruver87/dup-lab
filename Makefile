.PHONY: bootstrap doctor demos clean-vendor

bootstrap:
	python scripts/bootstrap.py

doctor:
	python scripts/bootstrap.py --doctor-only

demos:
	python scripts/bootstrap.py --skip-pip

clean-vendor:
	rm -rf vendor
