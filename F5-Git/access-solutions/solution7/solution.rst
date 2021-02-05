Solution:  Inline SAML with Kerberos sideband
======================================================================================

This solution documents all the necessary pieces required to create a set of APM policies that updates the AD lastlogontimestamp when only using SAML.  

Keywords: saml, kerberos, ad, active, directory, idp, sp, chaining, inline

DC: single, multi


URL
----
https://sp.acme.com

Objective:
----------

-  Gain an basic understanding of BIG-IP as a SAML IDP and SAML SP

-  Gain an understanding of sideband request

-  Gain an initial understanding of kerberos SSO

.. toctree::
   :maxdepth: 1
   :caption: Content:
   :glob:
  
   guide/guide.rst



Configuration Comments
------------------------

Access Blueprint Revision
----------------------------

  - 4

Postman Collection(s)
-----------------------
  - solution7-create.postman_collection.json
  - solution7-delete.postman_collection.json


APM Profile(s) 
----------------

  - profile_Common_receive-sideband-psp.conf.tar
  - profile_Common_send-sideband-psp.conf.tar


BIG-IP Versions Tested
------------------------
  - 15.1

BIG-IP Components used:
--------------------------


* Virtual Server
 - HTTP Profile 
 - Client-side SSL Profile 
 - Access Profile(s)
      + SAML SP Service
      + SAML IDP Connector
      + SAML IDP Service
      + SAML SP Connector
      + AAA Active Directory 
      + Kerberos SSO





   

