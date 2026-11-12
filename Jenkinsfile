pipeline {
	agent any
	environment {
		PROJECT_OWNER = "devaine"
	}
	stages {
		stage("Build") {
			steps {
				// Reference: https://www.jenkins.io/doc/pipeline/steps/credentials-binding/
				withCredentials([
					string(
						credentialsId: 'FORGEJO_REGISTRY'
						variable: "FORGEJO_REGISTRY"
					)
					usernamePassword(
						credentialsId: "FORGEJO_REGISTRY_LOGIN"
						usernameVariable: "FORGEJO_USERNAME"
						passwordVariable: "FORGEJO_PAT"
					)
				])

				// Login to the Forgejo Registry
				sh '''
						printf "$FORGEJO_PAT" | docker login "$FORGEJO_REGISTRY" -u "$FOREGJO_PAT_USER" --password-stdin
					'''


				dir('./server/desec-ip-sync/') {
					sh '''
						docker buildx build -t "$FOREGJO_REGISTRY"/${env.PROJECT_OWNER}/${env.JOB_NAME}
					'''
				}

				// Clean workspace after build
				cleanWs()
			}
		}
	}
	post {
		always {
			cleanWs(
				cleanWhenNotBuilt: false,
				deleteDirs: true,
				disableDeferredWipeout: true,
				notFailBuild: true,
				patterns: [[pattern: ".gitignore", type: "INCLUDE"],
									 [pattern: ".propsfile", type: "EXCLUDE"]]
			)
		}
	}
}
