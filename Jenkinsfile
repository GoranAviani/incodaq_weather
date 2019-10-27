#!/bin/bash

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            echo lastChanges
            
        stage 'Update Python Modules and test'
            sh 'virtualenv env1'
            sh '. env1/bin/activate && pip3 install --upgrade -r requirements.txt && python ./manage.py test'
 
        stage 'Deploy'
        echo 'Deployment is coming soon'
      
    }

    catch (err) {
        
        throw err
    }

}