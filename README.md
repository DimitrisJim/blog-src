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
`.rst` or `.md` files. After that is done you can test locally with `make serve`
from what the `Makefile` shows (can't remember ever doing this).

Then just `make html`.

##### Pushing

Since we're working with a submodule, `push`ing gets a flag:

```bash
git push --recurse-submodules=on-demand
```
See **Publishing Submodule Changes** [here][1]. This goes into every submodule
(see `.gitmodules`) and tries to push. If all pushes succeed then the top
level git repository is pushed.

Be careful if you make changes to any cloned repo's (voce, pelican-plugins)
because recloning afterwards will obviously not keep those changes around.

---

I think that's all. Will update again if I find anything else.

[1]: https://git-scm.com/book/en/v2/Git-Tools-Submodules
