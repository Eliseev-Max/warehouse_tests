node {
    stage('checkout') {
        checkout([
        $class: 'GitSCM',
        branches: [[name: '*/main']],
        userRemoteConfigs: [[
            credentialsId: 'jenkins-github',
            url: 'https://github.com/Eliseev-Max/warehouse_tests.git'
            ]]
        ])
    }
    stage('build_image') {
        sh 'docker build -t wh_tests .'
    }
    stage('test') {
        sh """
            docker run -v $WORKSPACE/allure-results/:/app/allure-results wh_tests:latest && echo $WORKSPACE
        """
    }
    stage('report-allure') {
        allure([
            includeProperties: false,
            jdk: '',
            properties: [],
            reportBuildPolicy: 'ALWAYS',
            results: [[path: 'allure-results']]
        ])
    }
}
