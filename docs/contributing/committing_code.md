## Committing guidelines

Please follow these guidelines when committing code to the repo.

* Never chage the published history of branched by force pushing.

* Limit commits to the most granular change that makes sense. This means, use frequent small commits rather than infrequent large commits. For example, if implementing feature X requires a small change to library Y, first commit the change to library Y, then commit feature X in a separate commit. This goes a long way in helping everyone follow your changes.
  
* Write detailed commit messages in the past tense, not present tense.

  * Good: "Fixed Unicode bug in RSS API."
  * Bad: "Fixes Unicode bug in RSS API."
  * Bad: "Fixing Unicode bug in RSS API."
  
## Reverting commits

When a mistaken commit is discovered, please follow these guidelines:

* If possible, have the original author revert their own commit.

* Don't revert another author's changes without permission from the original author.

* Use git revert -- this will make a reverse commit, but the original commit will still be part of the commit history.

* If the commit introduced a confirmed, disclosed security vulnerability then the commit may be reverted immediately without permission from anyone.

* The release branch maintainer may back out commits to the release branch without permission if the commit breaks the release branch.

* If the original author can't be reached (within a reasonable amount of time -- a day or so) and the problem is severe -- crashing bug, major test failures, etc. -- then ask for objections then revert if there are none.