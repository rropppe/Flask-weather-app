pipeline {
    agent any

    environment {
        DOCKER_HUB_TOKEN = credentials('docker-hub-token') // Имя учетных данных Jenkins для токена Docker Hub
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Проверка подключения к GitHub
                    try {
                        sh 'ping -c 4 github.com'
                        sh 'curl -I https://github.com'
                    } catch (Exception e) {
                        error "Unable to connect to GitHub. Please check your network connection."
                    }

                    // Клонирование репозитория
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], userRemoteConfigs: [[url: 'https://github.com/rropppe/Flask-weather-app.git', credentialsId: '8e4b6871-d3a9-41c8-a31d-484c89754962']]])

                    // Получаем последний тег
                    def lastTag = sh(script: 'git describe --tags `git rev-list --tags --max-count=1`', returnStdout: true).trim()
                    echo "Last tag: ${lastTag}"

                    // Сохраняем последнюю версию в переменную окружения
                    env.VERSION = lastTag
                }
            }
        }

        stage('Docker Compose Up') {
            steps {
                script {
                    // Передаем версию тега в Docker Compose
                    sh "VERSION=${env.VERSION} docker-compose up -d"
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Логинимся в Docker Hub
                    sh "echo ${DOCKER_HUB_TOKEN} | docker login --username rrropppe --password-stdin"

                    // Сборка Docker-образа
                    sh "docker build -t rrropppe/rrropppe:${env.VERSION} ."

                    // Публикация Docker-образа в Docker Hub
                    sh "docker push rrropppe/rrropppe:${env.VERSION}"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
        }
        success {
            echo 'Pipeline succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}

