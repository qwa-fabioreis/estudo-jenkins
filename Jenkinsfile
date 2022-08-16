pipeline {
agent any
stages {
    stage('Build image') {
        steps {
            echo 'Início do build Docker'
                // def customImage = docker.build("my-image:${env.BUILD_ID}")
            sh 'docker build -t qwasolucoes/premier-pet-core:teste-jenkins .' 
                // customImage.push()
            // dockerfile {
            //     filename 'Dockerfile.build'
            //     dir 'build'
            //     label 'teste-build-image'
            //     additionalBuildArgs  '--build-arg version=1.0.2'
            //     args '-v /tmp:/tmp'
            }
        }
    }
}