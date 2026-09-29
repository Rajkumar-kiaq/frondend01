pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        S3_BUCKET = 'smartproject-s3distfile'
        CLOUDFRONT_DIST_ID = 'E3FLOCILOCAL99'
    }
    
    stages {
        stage('Install Dependencies') {
            steps { 
                sh 'npm ci'
            }
        }
        
        stage('Build Production Bundle') {
            steps {
                sh 'npm run build'
            }
        }   
           
        stage('Sonarqube Analysis') {
            steps {
                script {
                    def scannerhome = tool name: 'sonarqube', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    
                    // Direct token based query parameter validation mapping enabled securely
                    sh """
                    ${scannerhome}/bin/sonar-scanner \
                    -Dsonar.projectKey=frontend \
                    -Dsonar.projectName=frontend-app \
                    -Dsonar.sources=src \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=YOUR_COPIED_API_HASH_TOKEN_HERE
                    """
                }
            }
        }   
      
        stage('Deploy to S3 Bucket') {
            steps {
                echo 'Syncing compiled assets to S3 dist subfolder...'
                sh """ 
                aws s3 sync dist/ s3://${S3_BUCKET}/dist/ --delete --region ${AWS_DEFAULT_REGION}
                """
                echo 'Frontend Assets Uploaded Successfully.'
            }      
        }
        
        stage('CloudFront Cache Invalidation') {
            steps {
                echo 'Skipping remote invalidation stage. Local Floci engine active!'
            }
        }
    }
}
