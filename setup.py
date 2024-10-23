from setuptools import setup, find_packages

setup(
    name='lct_calculator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',  # Exemplo de dependências
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'lct_calculator = lct_calculator.main:main',  # Comando para rodar o projeto se necessário
        ],
    },
)
