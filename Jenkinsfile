def repoUrl = 'https://github.com/qwa-fabioreis/estudo-jenkins.git'
pipeline {
  agent any
  environment {
        GIT_TAG  = "jenkins.${BUILD_NUMBER}"
    }
  stages {
    stage("push tag") {
      steps {
        withCredentials([[$class: 'UsernamePasswordMultiBinding',
            credentialsId: 'qwa-git',
            usernameVariable: 'GIT_USERNAME',
            passwordVariable: 'GIT_PASSWORD']]) {
            sh '''
                git config --global credential.username $GIT_USERNAME
                git config --global credential.helper '!f() { echo password=$GIT_PASSWORD ; }; f'
            '''
            sh """
                git tag ${GIT_TAG}
                git push ${repoUrl} --tags
            """
            }
      }
    }
  }
}
// https://www.cloudbees.com/blog/how-to-install-and-run-jenkins-with-docker-compose