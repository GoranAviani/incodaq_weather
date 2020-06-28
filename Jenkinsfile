#!/bin/bash

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            echo lastChanges

         stage 'Deploy'
            sh 'chmod +x ./deployment/deploy_prod.sh'
            sh './deployment/deploy_prod.sh'

    }

    catch (err) {

        throw err
    }

}