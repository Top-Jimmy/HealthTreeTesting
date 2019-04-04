README

HealthTree automated test suite


Clone github repo (only contains test files)



MacOS Setup

Requires
        pip
        homebrew
        java


Install selenium python bindings
        $ pip install selenium

Install chromedriver
        $ brew install chromedriver

Install test runner**
        $ pip install nose

        **If test runner won't install globally, try installing in virtualenv
                https://packaging.python.org/tutorials/installing-packages/

Download Selenium Standalone Server
        https://www.seleniumhq.org/download/




Running Tests

Start selenium server (from directory of .jar)
        $ java -jar selenium-server-standalone-3.x.x.jar -port 5050

Open new window to run tests

** If running out of virtualenv, open it **
        $ source <virtualenv_directory>/bin/activate

Run tests (from directory w/ test suite)

        Run all tests
                $ nosetests

        Run file/class/single test
                $ nosetests test_file.py:TestClass.test_name






 Documentation

 nosetests: https://nose.readthedocs.io/en/latest/

 selenium python bindings: https://www.seleniumhq.org/docs/03_webdriver.jsp

