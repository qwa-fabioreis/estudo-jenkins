pipeline {
    agent none stage
    {
        stage('Instalação do alpine') {
            agent{
                docker{
                    image 'alpine'
                }
            }
        }
    }
    steps{
        echo 'Deu certo'
    }
}