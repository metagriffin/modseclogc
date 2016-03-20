========================
ModSecurity Log Compiler
========================

The `modseclogc` is a ModSecurity audit log file manipulation and
analysis tool, command-line or python module based.


Project
=======

* Homepage: https://github.com/metagriffin/modseclogc
* Bugs: https://github.com/metagriffin/modseclogc/issues


Installation
============

.. code:: bash

  $ pip install modseclogc


Examples
========

View a request by unique ID:

.. code:: text

  $ modseclogc --match-id VtU2o38AAQEAAEV6AuwAAAAE modsec.log
  --fc565b0b-A--
  [01/Mar/2016:06:28:51 +0000] VtU2o38AAQEAAEV6AuwAAAAE 127.0.0.1 34882 127.0.0.1 80

  [...snip...]

  --fc565b0b-Z--

Display request IDs that match a path glob:

.. code:: text

  $ modseclogc --match-path /path/to/resource/** --show-id modsec.log
  VtU2o38AAQEAAEV6Au0AAAAE
  VtU2o38AAQEAAEV6AuwAAAAE
  VtU2o38AAQEAAEV5BIgAAAAK

Display the request line and the request payload (modsec audit part
"C") of each audit record:

.. code:: text

  $ modseclogc --show-request-line --show-parts C modsec.log
  OPTIONS /path/to/resource HTTP/1.1
  GET /path/to/resource HTTP/1.1
  POST /path/to/resource HTTP/1.1
  --40382b65-C--
  query=foo+bar&page=1

  GET /path/to/resource HTTP/1.1

Generate a copy of the audit excluding the payloads (modsec audit part
"C") for a specific path glob, and compress the output:

.. code:: text

  $ modseclogc --match-path /path/to/resource/** --unmatched keep \
      --hide-parts C modsec.log | gzip -9 > clean-modsec.log.gz


Details
=======

* By default, all input records are matched and unmatched records are
  dropped. Matched records are modified via the "--match-*" and
  "--inverse" arguments. What happens to unmatched records is
  controlled by the "--unmatched" argument.

* Output operations (show, hide, etc) only apply to matched records
  (note that the "--inverse" argument inverts the matching algorithm,
  not this rule).

* The audit log must be in "Native" format (see ``SecAuditLogFormat``
  modsec option).
