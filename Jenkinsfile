pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent'  // This should match the label in your values.yaml
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: jenkins-agent
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest
    """
        }
    }
    environment {
        GITLAB_URL = 'https://gitlab.com'
        DOCKER_IMAGE = "idoshoshani123/music-manager-frontend"
        DOCKER_IMAGE_TAG = "1.0.${BUILD_NUMBER}"
        PROJECT_ID = "64588632"
        TARGET_BRANCH = 'main'
    }
    stages {
        stage ("Checkout_Code") {
            steps {
                checkout scm
            }
        }

        stage ("Build_docker_image") {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_IMAGE_TAG}", "--no-cache .")
                }
            }
        }

        stage("Push_Docker_Image") {
            when {
                branch "main"
            }
            steps {
                script {
                    docker.withRegistry("https://registry.hub.docker.com", "docker-hub-idoshoshani123") {
                        dockerImage.push("${DOCKER_IMAGE_TAG}")
                    }
                }
            }
        }

        stage("Create merge request") {
            when {
                not {
                    branch TARGET_BRANCH
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'GITLAB_API_TOKEN', variable: 'GITLAB_API_TOKEN')]) {
                        def response = sh(script: '''
                            curl -s -o response.json -w "%{http_code}" --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/merge_requests" \
                            --form "source_branch=${BRANCH_NAME}" \
                            --form "target_branch=${TARGET_BRANCH}" \
                            --form "title=MR from ${BRANCH_NAME} into ${TARGET_BRANCH}" \
                            --form "remove_source_branch=true"
                        ''', returnStdout: true, shell: '/bin/bash').trim()

                        if (response.startsWith("20")) {
                            echo "Merge request created successfully."
                        } else {
                            echo "Failed to create merge request. Response Code: ${response}"
                            try {
                                def jsonResponse = readJSON file: 'response.json'
                                echo "Error message: ${jsonResponse.message}"
                            } catch (Exception e) {
                                echo "Failed to parse JSON response. Error: ${e.message}"
                            }
                            error "Merge request creation failed."
                        }
                    }
                }
            }
        }
    }
}