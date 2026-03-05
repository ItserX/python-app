pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
    }

    environment {
        VENV_DIR = '.venv'
    }

    stages {
        stage('build') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    python -m compileall app tests
                '''
            }
        }

        stage('lint') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    flake8 app tests
                '''
            }
        }

        stage('test') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python -m unittest discover -s tests -v
                '''
            }
        }

        stage('deploy') {
            when {
                branch 'master'
            }
            steps {
                sshagent(credentials: ['vm-ssh-key']) {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
                    '''
                }
            }
        }
    }
}
