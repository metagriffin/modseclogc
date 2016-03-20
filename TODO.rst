=====
TODOs
=====


* Support ``SecAuditLogType Concurrent`` mode

* Support `Matcher` and `Renderer` plugin loading

* Create a matcher and renderer expression language? e.g.::

    $ modseclogc --match '( path("XXX") or path("YYY") ) and not cookie("YYY")'

* Add support for audit logs in JSON format (i.e. ``SecAuditLogFormat
  JSON``) added in modsec 2.9.1

* Auto-detect gzip-compressed input

* (?) be able to apply a different renderer to unmatched records
  (beyond NativeRenderer)
