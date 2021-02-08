import sys
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import user_data
import time

def create():
    main_dir = user_data.main_dir
    chrome_driver_path = user_data.chrome_driver_path
    name_project = sys.argv[1]

    private = ''
    share = False
    share_github = sys.argv[2]
    if share_github == 'y' or share_github == 'Y':
        share = True
        private = sys.argv[3]
    else:
        share  = False

    full_path = main_dir + '/' + name_project

    try:
        os.mkdir(full_path)
        open(full_path + '/' + 'script.py','a').close()
        open(full_path + '/' + 'README.md','a').close()
        gitignore = open(full_path + '/' + '.gitignore','a')
        gitignore.write('venv/')
        gitignore.close()
        command = 'bash -c "python3 -m venv {}/venv"'.format(full_path)
        subprocess.run(command, shell=True)

        if share:
            subprocess.run('bash -c " cd {} && git init"'.format(full_path), shell=True)

            driver = webdriver.Chrome(user_data.chrome_driver_path)
            driver.get('https://www.github.com/login')
            driver.find_element_by_id('login_field').send_keys(user_data.git_username)
            driver.find_element_by_id('password').send_keys(user_data.git_password)
            driver.find_elements_by_xpath('//*[@id="login"]/div[4]/form/input[14]')[0].click()
            
            driver.find_elements_by_xpath('//*[@id="repos-container"]/h2/a')[0].click()
            driver.find_element_by_id('repository_name').send_keys(name_project)

            if private == 'pr' or private == 'PR':
                driver.find_elements_by_xpath('//*[@id="repository_visibility_private"]')[0].click()
            elif private == 'pub' or private == 'PUB':
                driver.find_elements_by_xpath('//*[@id="repository_visibility_public"]')[0].click()
            else:
                print('unknown parameter. Set private')
                driver.find_elements_by_xpath('//*[@id="repository_visibility_private"]')[0].click()

            time.sleep(1)
            driver.find_elements_by_xpath('//*[@id="new_repository"]/div[4]/button')[0].click()
            driver.close()
        else:
            print('Skipped publish on repository')

        command = 'bash -c "cd {}; code ."'.format(full_path)
        subprocess.run(command, shell=True)
    except FileExistsError as identifier:
        print(identifier)
        os._exit

def display_help():
    print('Setup project by PatrykMCoder')
    print('=========HELP===========')
    print('Syntax: python script.py title share-on-github: y/n private-repo pr[private]/pub[public]')
    print('example: python script.py project y pr')
    print('Please create user_data.py file and insert data. Check user_data.py.example')

if __name__ == "__main__":
    if sys.argv[1] == '--help':
        display_help()
    else:
        create()
