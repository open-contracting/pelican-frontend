# Pelican frontend

## Getting started

Set up the git pre-commit hook:

```bash
pre-commit install
```

[Developer documentation](https://docs.google.com/document/d/1cfunGPyP-QLHOeQT3olFEHJh0J_aieUJZzxirT7Y8wk/edit)

## Django

### Getting started

Install development dependencies:

```bash
pip install pip-tools
pip-sync requirements_dev.txt
```

## Vue

All commands must be run from the `frontend/` directory.

### Getting started

Install dependencies:

```bash
npm install
```

### Develop

Start a development server:

```bash
npm run serve
```

Prepare a production build:

```bash
npm run build
```

### Test

Run tests:

```bash
npm run test
```

Run linters:

```bash
npm run lint
```
