# Contributing

This document describes the expectation of work submitted to the project. Also refer to the [python library standards](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/python_libraries.md), the [general python standards](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/python_general.md), and the [overall standards](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/general_standards.md), which apply in tandem unless overwritten by this document.

This project has no additional standards enforced aside from the aforementioned documents. Please always keep in mind the [definition of done](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/general_standards.md#definition-of-done) when submitting and approving PRs:

1. [Possessing sufficient tests to prove to unfamiliar that the changes made are functional](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/general_standards.md#testing)
2. [Documented well enough for unfamiliar developers to recreate the context of the changes when maintaining affected code](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/general_standards.md#context-documentation)
3. [Documented well enough for consumers to use the modified functionality independently of the developer](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/general_standards.md#consumer-facing-documentation)
    - Consumers in this context are library users, and the docstrings/docsite for new/modified functionality should be kept up-to-date with every PR.
4. [Will not break the build upon merge to main branch](https://github.com/haptemy-consulting/hptstandards/blob/main/project_standards/general_standards.md#version-control)
    - CI in this project is based around tox, which will check pytest as well as black formatting.
5. Solves the goal of any linked Jira sub-tasks/stories
6. If applicable, meets the product owner's definition of done as well for any linked Jira stories
