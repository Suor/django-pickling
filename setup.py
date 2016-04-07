from setuptools import setup

setup(
    name='django-pickling',
    version='0.2',
    author='Alexander Schepanovski',
    author_email='suor.web@gmail.com',

    description='Efficient pickling for django models.',
    long_description=open('README.rst').read(),
    url='http://github.com/Suor/django-pickling',
    license='BSD',

    py_modules=['django_pickling'],
    install_requires=['django'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
