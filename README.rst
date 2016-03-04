========
Cibopath
========

Search Cookiecutters on GitHub.

Usage
=====

.. code-block:: text

	Usage: cibopath [OPTIONS] COMMAND [ARGS]...

	  Cibopath - Search Cookiecutters on GitHub.

	Options:
	  -v, --verbose           Print debug information
	  -c, --config-file PATH  Config file to hold settings
	  -V, --version           Show the version and exit.
	  --help                  Show this message and exit.

	Commands:
	  config
	  search
	  update

Config
------

First you need to `create a GitHub access token`_ for Cibopath, so it can
authenticate with the `GitHub API v3`_. `GitHub's rate limiting`_ won't allow
more than 60 unauthenticated requests per hour. So yeah, you definitely want to
have a token set up as there are more than 60 featured `Cookiecutter
templates`_.

The Cibopath access token does **NOT** require any `scopes`_. Please stick to
the defaults when creating the token (**Read-only access to public
repositories**).

Now use the CLI to store your credentials in your home directory (default
``~/.cibopathrc``).

.. code-block:: bash

	$ cibopath config github.username <your-username>
	$ cibopath config github.token <your-access-token>

Feel free to view the contents of the config file via:

.. code-block:: bash

    $ cibopath -v config --list


Update
------

With GitHub authentication in place, you now want to fetch information about
available Cookiecutter templates. Cibopath dumps the data as a JSON file to
disk. You can specify the target location either via user config or CLI.

Save dump-file location to settings:

.. code-block:: bash

	$ cibopath config templates.file ~/.cibopath/templates.json
	$ cibopath -v update

Or specify it on the CLI:

.. code-block:: bash

	$ cibopath -v update --dump-file=~/.cibopath/templates.json


License
=======

Distributed under the terms of the `BSD 3-Clause License`_, Cibopath is free
and open source software

Code of Conduct
===============

Everyone interacting in the Cibopath project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _`BSD 3-Clause License`: LICENSE
.. _`Cookiecutter templates`: https://github.com/audreyr/cookiecutter#available-cookiecutters
.. _`GitHub API v3`: https://developer.github.com/v3/
.. _`GitHub's rate limiting`: https://developer.github.com/v3/#rate-limiting
.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
.. _`create a GitHub access token`: https://help.github.com/articles/creating-an-access-token-for-command-line-use/
.. _`scopes`: https://developer.github.com/v3/oauth/#scopes
