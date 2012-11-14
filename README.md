DEHUMANIZER SETUP

I'm using vagrant, because aalib didn't work very well natively on OS X. Here be instructions to install Vagrant: http://vagrantup.com

    > git clone git://github.com/theonion/dehumanizer.git
    > cd dehumanizer/
    > vagrant up
    > vagrant ssh

This will give you an SSH session to the VM, and drop you into the virtual env. 

From here, you can run the dev server:

    > python manage.py runserver

Run the celery worker (which does the actual processing):

    > python manage.py celery worker -l INFO

Alternatively, you can just run the whole damn thing via supervisor, which will make the site available on port 80:

    > supervisord


TODO:

 - implement 'history'
 - Share Tools
 - caching
 - 'help'