from setuptools import setup, find_packages

with open('PYPIREADME.md', 'r') as f:
    project_description = f.read()

setup(
    name='document_forger',
    version='1.0.2.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.5.1', 
        'pytesseract>=0.3.7',
        'pillow>=8.1.0', 
        'pandas>=1.2.3',
        'tqdm>=4.59.0',
        'numpy>=1.20.1',
        'torch>=2.3.1',
        'torchvision>=0.18.1',
        'super-image>==0.1.7',
    ],
    entry_points={
        'console_scripts': [
            'document_forger=src.__main__:main',
        ],
    },
    include_package_data=True,
    description='A package for generating forged documents',
    long_description=project_description,
    long_description_content_type='text/markdown',  
    url='https://github.com/visionrd-ai/document-forger.git', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

