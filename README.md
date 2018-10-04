# Documentation Template

## What is this Repo?

For consistency and ease of use, this project provides a way to quickly spin up documentation for a Python project including:

- Basic Sphinx project structure
- `.github/` template files for more streamlined Pull Requests and Issues

## Get Docs for Cheap

The first step to getting started with your own page is to install the `cookiecutter` library to your Python environment, if you haven't already. You can do this simply with

```
pip install cookiecutter
```

Then, from the command-line, navigate to where you'd like to make the project and use `cookiecutter` on this URL

```
cookiecutter https://github.com/NapsterInBlue/docs-template
```

It's going to ask you for some file-naming information, \[with defaults in square brackets\], and then use that information to build out a directory with the necessary structure. **BE SURE TO ACCEPT THE DEFAULT FOR** `just_accept_default`!
