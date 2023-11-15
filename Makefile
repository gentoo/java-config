build:
	meson setup build

.PHONY: test
test: build
	meson test -C build --verbose

.PHONY: test
test-install: build
	meson install -C build --destdir /var/tmp/java-config-destdir
