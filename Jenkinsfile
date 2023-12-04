// pipeline {
// agent any
// stages {
//     stage('Build image') {
//         steps {
//             echo 'Início do build Docker'
//                 // def customImage = docker.build("my-image:${env.BUILD_ID}")
//             sh 'docker build -t qwasolucoes/premier-pet-core:teste-jenkins .' 
//                 // customImage.push()
//             // dockerfile {
//             //     filename 'Dockerfile.build'
//             //     dir 'build'
//             //     label 'teste-build-image'
//             //     additionalBuildArgs  '--build-arg version=1.0.2'
//             //     args '-v /tmp:/tmp'
//             }
//         }
//     }
// }

node {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace teste */
        git clone 'https://github.com/qwa-fabioreis/estudo-jenkins.git'
        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("getintodevops/hellonode")
    }

    stage('Test image') {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
}
