.PHONY: bootstrap doctor demos verify promo promo-offline clean-vendor

bootstrap:
	python scripts/bootstrap.py

doctor:
	python scripts/bootstrap.py --doctor-only

demos:
	python scripts/bootstrap.py --skip-pip

verify:
	@bash scripts/verify.sh 2>/dev/null || python -c "import subprocess,sys; sys.exit(subprocess.call(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File','scripts/verify.ps1']))"

promo:
	python scripts/promo_teaser.py

promo-offline:
	python scripts/promo_teaser.py --offline-tts

clean-vendor:
	rm -rf vendor
