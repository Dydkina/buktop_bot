# buktop_bot

## Initial configuration

### [pyenv](https://github.com/pyenv/pyenv)

```shell
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

Then go to proj library if you are not there:

```shell
pyenv install
```

### Install dependencies

```shell
pip install -r requirements.txt
```
