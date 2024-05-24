pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-token') // Имя учетных данных Jenkins для токена Docker Hub
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // Получаем последний тег
                    def lastTag = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
                    echo "Last tag: ${lastTag}"

                    // Вычисляем следующую версию
                    def versionComponents = lastTag.tokenize('.')
                    def major = versionComponents[0].toInteger()
                    def minor = versionComponents[1].toInteger()
                    def patch = versionComponents[2].toInteger() + 1
                    def newTag = "${major}.${minor}.${patch}"
                    echo "New tag: ${newTag}"

                    // Выполняем тэгирование и пуш
                    sh "git tag v${newTag}"
                    sh "git push origin v${newTag}"

                    // Сохраняем новую версию в переменную окружения
                    env.VERSION = newTag
                }
            }
        }

        stage('Docker Compose Up') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Логинимся в Docker Hub
                    sh "echo ${DOCKER_HUB_CREDENTIALS} | docker login --username rrropppe --password-stdin"

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

