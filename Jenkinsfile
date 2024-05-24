pipeline {
    agent any

    environment {
        DOCKER_HUB_TOKEN = credentials('docker-hub-token') // Имя учетных данных Jenkins для токена Docker Hub
    }

    stages {
        stage('Checkout') {
            steps {
                script {
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
                    sh "docker build -t rrropppe/weather-app:${env.VERSION} ."

                    // Публикация Docker-образа в Docker Hub
                    sh "docker push rrropppe/weather-app:${env.VERSION}"
                }
            }
        }

        stage('Cleanup Docker Resources') {
            steps {
                script {
                    // Остановка и удаление запущенных контейнеров
                    sh "docker-compose down"

                    // Удаление локальных Docker-образов
                    sh "docker rmi rrropppe/weather-app:${env.VERSION}"
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

