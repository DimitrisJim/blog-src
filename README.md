### Instructions for the case you drop the blog again and forget how everything was connected.

#### Getting set-up:

This repo as well as the repo's it depends on all have submodules attached, so you'll need to use `--recurse-submodules` (was `--recursive`) when cloning. First, this repo:

```bash
git clone --recurse-submodules git@github.com:DimitrisJim/blog-src.git
```
Then grab the voce theme and the peligan-plugin repositories:
```bash
git clone --recurse-submodules git@github.com:limbenjamin/voce.git
git clone --recurse-submodules git@github.com:getpelican/pelican-plugins
```

Then, since you'll probably be using `conda` create a new env and pip install
pelican. After doing this, running `make html` should build to `output` with no
issues. Remember, output is the submodule pointing to the master branch of
dimitrisjim.github.io, the repo that holds the data for the page.

#### Making changes

Content is in, shocker, the `content/` folder. That's where you can edit those
`.rst` or `.md` files. 

After that is done you can test locally with `make html` which doesn't use the publishconf.py file 
that has extra settings for when publishing.

After that, `make publish` and push the changes.

##### Pushing

Push the submodule first and then push the top level module.

---

### Syntax Highlighting:

See [codehilite][2] which is a Markdown extension. Its responsible for adding
syntax Highlighting to code blocks.


[1]: https://git-scm.com/book/en/v2/Git-Tools-Submodules
[2]: https://python-markdown.github.io/extensions/code_hilite/
