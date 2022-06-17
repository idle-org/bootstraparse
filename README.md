# bootstraparse
bootstraparse is a personal project started with a specific goal in mind: creating static html pages for direct display from a markdown-like file.
bootstraparse aims to be customisable in that regard, but its first iteration and main focus will be to create a bootstrap-powered html.


You can refer to the `example_userfiles` for an idea of what the parser expects you to feed it and find an example of our automated generation at https://idle-org.github.io/bootstraparse/ for this particular folder. Or you can run the program yourself for the same result!

- Main
  - [![Python Tests and Lint](https://github.com/idle-org/bootstraparse/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/idle-org/bootstraparse/actions/workflows/python-tests.yml)
- Releases
  - [![Python Tests and Lint](https://github.com/idle-org/bootstraparse/actions/workflows/python-tests.yml/badge.svg?branch=develop)](https://github.com/idle-org/bootstraparse/actions/workflows/python-tests.yml)
- Deploy
  - [![Python Deployment](https://github.com/idle-org/bootstraparse/actions/workflows/python-deploy.yml/badge.svg?branch=main)](https://github.com/idle-org/bootstraparse/actions/workflows/python-deploy.yml)
---
## Release Notes
### V1.0.1
- Remove old regex usage
- Add copy behaviour to config file
- Add the type and return types of all functions
- Add documentation to remaining lone functions
- Copy un-parsable files to destination folder without modifications
- Many bug fixes and improvements

### V1.0.2
- Put out many fires

### V1.0.3
- Put out many more fires
- Fixed continuous integration
- Added doc generation

### V1.0.4
- Made the default example site more useful
- Wrote a barebone documentation for the application


## Roadmap
### V1.0.5
- Improved the roadmap ☑
- Established a list of many configurable parameters to implement in the future, and updated the roadmap with them. ☑
- Add more context to the warning messages ☐
- Test configs more in-depth ☐
- Test overall site generation ☐
- Move the WARNING-level output to INFO for config overwrite ☐
- Better error handling ☐
  - Stack dropping on error ☐
  - Better context for error messages ☐
  - Move error context to the calling function ☐

### V1.0.6
- Option to ignore br behavior ☐
- Make the default example site way more useful ☐
- Add an indentation level to every token for human readability of the final output ☐

### V1.0.7
- Add a way to ignore certain files ☐
- Add a way to ignore certain directories ☐
- Add a way to ignore certain file extensions ☐

### V1.0.8
- Add a post process function ☐
- Add a way to mark lines to be post-processed ☐

### V1.0.9
- Add a benchmark ☐
- Document the syntax.reparse function and behavior better ☐

### V1.1
- Functioning `table` Token ☐
- Functioning `code` Token ☐
- Have the context manager able to analyse the context and depending on some conditions, add post processing hooks ☐
  - Decide if it should be able to be used on multiple files ☐
  - Decide the number and complexity of the hooks ☐
  - Decide on the scope of the hooks (Create navbar, create glossary, create links etc...) ☐
  - Decide if they should be configurable (user side) ☐
- Update the uses of remaining files ☐
- Add a global line count and a line tracker to the parser ☐

### V1.1.1
- Option to save intermediate files ☐
  - Only save files after preparsing ☐
  - Only save files after parsing ☐
  - Only save files after postprocessing ☐
  - Only save files after generating the site ☐
- Option to ignore some steps ☐
  - Ignore preparsing ☐
  - Ignore parsing ☐
  - Ignore postprocessing ☐
  - Ignore generating the site ☐
- Option to set the debug level ☐
- Option to fetch the config file from a remote source ☐
- Option to fetch the template file from a remote source ☐
- Option to switch between different templates ☐ (Why not just use different files tho ?)
- Option to remove destination files before generating ☐
- Option to remove destination directories before generating ☐
- Option to pass some arguments to the parser ☐
- Option to pass some arguments to the post processor ☐
- Option to ignore some markup elements (likely only in context though) ☐
- Option to treat some errors as warnings ☐ (Mostly for the parser and context manager)
- Option to treat some warnings as errors ☐
- Option to change the behaviour of some specific tokens (change br behaviour mainly) ☐

### V1.1.2
- Mark the parsed files with a timestamp or hash in a way that can be used to determine if they have been changed ☐
- Option to ignore files that have not been changed ☐

### V1.2
- Check error messages and add a real debug level to parameters ☐
- Thouroughly test logging, and error messages for the user ☐
- Functioning `blockquote` Token ☐

### V1.3
- Add advanced lookahead logic for `*` ☐
- Functioning `lead` Token ☐

### V1.4
- Add html indentation for human readability of the output. ☐
- Write thourough documentation for the application (use specs.yaml) ☐

### V2
- Add a functioning post-context enhancer able to generate menus and elements from arbitrary logic. ☐
- Achieve perfect markdown compatibility with appropriate config parameters ☐

### V3
- Add Template customisation. ☐
- Add a lot of base templates (released as themes ?). ☐