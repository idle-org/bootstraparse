# bootstraparse
bootstraparse is a personal project started with a specific goal in mind: creating static html pages for direct display from a markdown-like file.
bootstraparse aims to be customisable in that regard, but its first iteration and main focus will be to create a bootstrap-powered html.


You can refer to the `example_userfiles` for an idea of what the parser expects you to feed it and find an example of our automated generation at https://idle-org.github.io/bootstraparse/ for this particular folder. Or you can run the program yourself for the same result!

[![Python application](https://github.com/idle-org/bootstraparse/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/idle-org/bootstraparse/actions/workflows/python-app.yml)

---
## Roadmap
### V1.0.1
- Make the default example site way more useful ☐
- Add the type and return types of all functions ☑
- Add documentation to remaining lone functions ☑
- Write a documentation for the application (use specs.yaml) ☐

### V1.0.2
- Move the WARNING-level output to INFO for config overwrite ☐

### V1.0.3
- Copy un-parsable files to destination folder without modifications ☑
- Add copy behaviour to config file ☑

### V1.1
- Functioning `table` Token ☐
- Functioning `code` Token ☐
- Establish a list of all configurable parameters to implement in the future, and update the roadmap with them. ☐
- Decide level of logic to be implemented, and whether it should be configurable ☐
- Update the uses of remaining files ☐


### V1.2
- Check error messages and add a real debug level to parameters ☐
- Functioning `blockquote` Token ☐
- Remove old regex usage ☐

### V1.3
- Add advanced lookahead logic for `*` ☐

### V1.4
- Add html indentation for human readability of the output. ☐

### V2
- Add a functioning post-context enhancer able to generate menus and elements from arbitrary logic. ☐
- Achieve perfect markdown compatibility with appropriate config parameters ☐
