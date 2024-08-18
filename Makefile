
ROOT_DIR := .
ROOT_DIR_ABS := $(realpath $(ROOT_DIR))
GRPC_DIR := $(ROOT_DIR_ABS)/src/olimar/internal/grpc
VENV_PATH := $(ROOT_DIR)/.venv


### Detect Linux vs. Windows
ifeq ($(OS), $(LINUX))
	PYTHON 	= $(NO_ECHO)python3
	PIP 	= $(NO_ECHO)pip3
	VENV_SRC_FILE := $(VENV_PATH)/lib/python3.11/site-packages/0src.pth
else
	PYTHON 	= $(NO_ECHO)python
	PIP 	= $(NO_ECHO)pip
	VENV_SRC_FILE := $(VENV_PATH)/Lib/site-packages/0src.pth
endif

### Build Tools
NO_ECHO =
ECHO 	= @echo
MKDIR 	= $(NO_ECHO)mkdir -p
RM 		= $(NO_ECHO)rm -fR
TOUCH 	= $(NO_ECHO)touch
SED     = $(NO_ECHO)sed
CD		= $(NO_ECHO)cd
CAT		= $(NO_ECHO)cat
GIT		= $(NO_ECHO)git
MAKE 	= $(NO_ECHO)make


.PHONY: services example-tests

create-venv:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install virtualenv
	$(PYTHON) -m virtualenv $(VENV_PATH) --python=python3.11
	$(TOUCH) $(VENV_SRC_FILE)
	$(ECHO) $(ROOT_DIR_ABS)/src >> $(VENV_SRC_FILE)

setup:
	$(PYTHON) -m pip install -r requirements.txt

services:
	mkdir -p $(GRPC_DIR)/build
	python -m grpc_tools.protoc -I$(GRPC_DIR)/proto --python_out=$(GRPC_DIR)/build --grpc_python_out=$(GRPC_DIR)/build $(GRPC_DIR)/proto/test_runner_service.proto
	sed -i 's/import test_runner_service_pb2/import olimar.internal.grpc.build.test_runner_service_pb2/g' $(GRPC_DIR)/build/test_runner_service_pb2_grpc.py

services-clean:
	rm -rf $(GRPC_DIR)/build/*

run-server:
	python src/olimar/service.py

run-client:
	python src/olimar/client.py

run:
	.\scripts\run.bat

example-tests:
	pytest $(ROOT_DIR)/example-env/tests/
