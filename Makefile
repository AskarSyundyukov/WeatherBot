BUILD_NUMBER 	= $(shell git rev-list --count HEAD)
DOCKER_IMAGE    = weather:v${BUILD_NUMBER}

DEPLOY_ENDPOINT = rdms.tplinkdns.com
SSH_USER        = pi
SSH             = ssh -o StrictHostKeyChecking=no -p 45673
SERVER          = ${SSH_USER}@${DEPLOY_ENDPOINT}
BUILD_DIR       = /tmp/weather-builds/${BUILD_NUMBER}


ifndef BOT_TOKEN
  $(error BOT_TOKEN is not set)
endif

ifndef WEATHER_TOKEN
  $(error WEATHER_TOKEN is not set)
endif


.PHONY: all
all: local_run


.PHONY: docker
docker:
	$(info ************ BUILD DOCKER IMAGE ************)
	docker build                                   \
		-f Dockerfile                              \
		-t $(DOCKER_IMAGE)                         \
		--no-cache                                 \
		--build-arg BOT_TOKEN=$(BOT_TOKEN)         \
		--build-arg WEATHER_TOKEN=$(WEATHER_TOKEN) \
		.


.PHONY: local_run
local_run: docker
	$(info ************ RUN DOCKER ************)
	docker stop weather || true
	docker rm weather || true
	docker run -d --name weather --restart always $(DOCKER_IMAGE)


.PHONY: server_files
server_files:
	$(info ************ SYNC REMOTE FILES ************)
	$(SSH) $(SERVER) mkdir -p $(BUILD_DIR)
	rsync -azrh               \
      --exclude '.idea'       \
      --exclude 'venv'        \
      --exclude '__pycache__' \
      -e '$(SSH)'             \
      $(PWD)/ $(SERVER):$(BUILD_DIR)


.PHONY: deploy
deploy: server_files
	$(info ************ REMOTE BUILD STARTED ************)
	$(SSH) $(SERVER) "cd $(BUILD_DIR) &&     \
      BOT_TOKEN=$(BOT_TOKEN)                 \
      WEATHER_TOKEN=$(WEATHER_TOKEN)         \
      make local_run && rm -rf $(BUILD_DIR)"
