pipeline {
    agent any
    stages {
        stage('Build image') {
            steps {
                echo 'Starting to build docker image'

                script {
                    // def customImage = docker.build("my-image:${env.BUILD_ID}")
                    sh 'docker build -t qwasolucoes/premier-pet-core:teste-jenkins .' 

                    // customImage.push()
                }
            }
        }
    }
}