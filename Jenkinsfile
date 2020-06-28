#!/bin/bash

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            echo lastChanges

        stage 'Update Python Modules and test'
            // Create a virtualenv in this folder, and install or upgrade packages
            // specified in requirements.txt; https://pip.readthedocs.io/en/1.1/requirements.html
            sh 'python3 -m virtualenv env1'
            sh '. env1/bin/activate && pip3 install --upgrade -r requirements.txt && python ./manage.py test'

         stage 'Deploy'
            sh 'chmod +x ./deployment/deploy_prod.sh'
            sh './deployment/deploy_prod.sh'

    }

    catch (err) {

        throw err
    }

}