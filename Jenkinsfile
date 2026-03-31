pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Set Up Python') {
      steps {
        script {
          if (isUnix()) {
            sh 'python3 -m venv .venv'
            sh '. .venv/bin/activate; python -m pip install --upgrade pip; pip install -r requirements.txt'
          } else {
            bat 'py -3 -m venv .venv'
            bat '.\\.venv\\Scripts\\python -m pip install --upgrade pip'
            bat '.\\.venv\\Scripts\\pip install -r requirements.txt'
          }
        }
      }
    }

    stage('Run Selenium Tests') {
      steps {
        script {
          if (isUnix()) {
            sh '. .venv/bin/activate; pytest tests --maxfail=1 --disable-warnings --junitxml=reports/test-results.xml'
          } else {
            bat '.\\.venv\\Scripts\\pytest tests --maxfail=1 --disable-warnings --junitxml=reports/test-results.xml'
          }
        }
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
    }
  }
}
