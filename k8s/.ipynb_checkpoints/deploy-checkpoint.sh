#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_DIR="./"

check_error() {
  if [ $? -ne 0 ]; then
    echo -e "${RED}Error during command execution. Stopping.${NC}"
    exit 1
  fi
}

check_kubectl() {
  if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed. Install it before proceeding.${NC}"
    exit 1
  fi
}

deploy_components() {
  PROJECT=$1
  MODE=$2

  PROJECT_DIR="$BASE_DIR/$PROJECT"

  echo -e "${YELLOW}Deploying '$PROJECT' in '$MODE' mode...${NC}"

  if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Project directory '$PROJECT_DIR' does not exist.${NC}"
    exit 1
  fi
  
  echo $PROJECT

  if [ "$PROJECT" == "mail-pipeline" ]; then
    echo -e "${GREEN}Deploying mail pipeline system...${NC}"
    COMPONENTS=("roles" "prometheus" "redis" "entrypoint" "parser" "header_analyzer" "attachment_manager" "link_analyzer" "text_analyzer" "image_analyzer" "message_analyzer" "virus_scanner")
  elif [ "$PROJECT" == "tea-store" ]; then
    echo -e "${GREEN}Deploying tea-store system...${NC}"
    COMPONENTS=("prometheus" "recommender" "persistence" "image" "entrypoint" "auth" "gs-algorithm" "webUI")
  else
    echo -e "${RED}Invalid system selected: $PROJECT${NC}"
    exit 1
  fi

  for COMPONENT in "${COMPONENTS[@]}"; do
    if [ "$COMPONENT" == "prometheus" ]; then
      if [ -d "$PROJECT_DIR/$COMPONENT" ]; then
        echo -e "${GREEN}Deploying $COMPONENT (entire directory, always)...${NC}"
        kubectl apply -f "$PROJECT_DIR/$COMPONENT" && check_error
      else
        echo -e "${YELLOW}Skipping $COMPONENT: directory not found.${NC}"
      fi

    elif [ "$MODE" == "local" ]; then
      if [ -d "$PROJECT_DIR/$COMPONENT" ]; then
        echo -e "${GREEN}Deploying $COMPONENT (entire directory)...${NC}"
        kubectl apply -f "$PROJECT_DIR/$COMPONENT" && check_error
      else
        echo -e "${YELLOW}Skipping $COMPONENT: directory not found for local mode.${NC}"
      fi

    elif [ "$MODE" == "global" ]; then
      FILE_PATH="$PROJECT_DIR/$COMPONENT/$COMPONENT.yaml"
      if [ -f "$FILE_PATH" ]; then
        echo -e "${GREEN}Deploying $COMPONENT (single file)...${NC}"
        kubectl apply -f "$FILE_PATH" && check_error
      else
        echo -e "${YELLOW}Skipping $COMPONENT: $COMPONENT.yaml not found for global mode.${NC}"
      fi

    else
      echo -e "${RED}Unknown mode: $MODE${NC}"
      exit 1
    fi
  done

  
  echo -e "${GREEN}Deployment of '$PROJECT' in '$MODE' mode completed successfully!${NC}"
}

undeploy_components() {
  PROJECT=$1

  PROJECT_DIR="$BASE_DIR/$PROJECT"

  echo -e "${YELLOW}Undeploying '$PROJECT'...${NC}"

  COMPONENTS=("prometheus" "recommender" "persistence" "image" "entrypoint" "auth" "gs-algorithm" "webUI" "roles" "prometheus" "redis" "entrypoint" "parser" "header_analyzer" "attachment_manager" "link_analyzer" "text_analyzer" "image_analyzer" "message_analyzer" "virus_scanner")

  for COMPONENT in "${COMPONENTS[@]}"; do
    if [ -d "$PROJECT_DIR/$COMPONENT" ]; then
      echo -e "${GREEN}Removing $COMPONENT...${NC}"
      kubectl delete -f "$PROJECT_DIR/$COMPONENT" --ignore-not-found=true
    elif [ -f "$PROJECT_DIR/$COMPONENT.yaml" ]; then
      echo -e "${GREEN}Removing $COMPONENT...${NC}"
      kubectl delete -f "$PROJECT_DIR/$COMPONENT.yaml" --ignore-not-found=true
    fi
  done

  echo -e "${GREEN}Undeployment of '$PROJECT' completed successfully!${NC}"
}


main() {
  check_kubectl

  if [ $# -ne 2 ]; then
    echo -e "${RED}Usage: $0 <project> <mode>${NC}"
    echo "Example: $0 mail-pipeline global"
    echo "Modes: global, local, undeploy"
    echo "Available projects: mail-pipeline, tea-store"
    exit 1
  fi

  PROJECT=$1
  MODE=$2

  case "$MODE" in
    "global"|"local")
      deploy_components "$PROJECT" "$MODE"
      ;;
    "undeploy")
      undeploy_components "$PROJECT"
      ;;
    *)
      echo -e "${RED}Invalid mode: $MODE${NC}"
      echo "Valid modes: global, local, undeploy"
      exit 1
      ;;
  esac
}

main "$@"
