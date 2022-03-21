# B00 plays GBA

## Built with

### Tools

- [Poetry](https://python-poetry.org/)

### [VSCode](https://code.visualstudio.com/)

- [ms-python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [Conventional Commits](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits)
- [EditorConfig](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)

## Getting started

### Installation

Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Clone the repository :
```bash
git clone git@git.inpt.fr:tocard-inc/enseeiht/projet-classification.git
```

Install the dependencies :

```bash
cd projet-classification
poetry run pip install --upgrade pip
poetry install
```

### Usage

Plug your android phone to your computer, ensure adb detects it and that you've granted the permission to your computer.

To run the database generator :
```bash
python3 src/main.py
```

## Contributing

Please use [conventional commits](https://www.conventionalcommits.org/).

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) license.
See [`LICENSE`](https://git.inpt.fr/fainsil/booplaysgba/-/blob/master/LICENSE) for more information.

## Contact

Laureηt \<[laurentfainsin@protonmail.com](mailto:laurentfainsin@protonmail.com)\>
Damien Guillotin  \<[damguillotin@gmail.com](mailto:damguillotin@gmail.com)\>
Pierre-Eliot Jourdan \<[pierreliot.jourdan@etu.inp-n7.fr](mailto:pierreliot.jourdan@etu.inp-n7.fr)\>
