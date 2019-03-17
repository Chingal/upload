Manage Tickets
=================
Create an api rest that allows us to manage the transaction creation tickets in a upload application.

Api Root
========
* **URL**: ``/api/``

* **METHOD**: ``GET``

* **Success Response**:
    * **Code**: ``200 OK``
    * **Content**:

.. code-block:: json

	{   
    		"tickets": "http://localhost:8000/api/tickets/",
    		"files": "http://localhost:8000/api/files/"
    	}
  
Obtain Auth Token
=================

* **URL**: ``/api-token-auth/``

* **METHOD**: ``POST``

* **DATA PARAMS**: ``{"username": admin, "password": "********" }``
    
* **Success Response**:
    * **Code**: ``200 OK``
    * **Content**:

.. code-block:: json

	{"token": "xxxxxxx-12345-aaaa-bbbb-9876-xxxx"}


List Tickets
============

* **URL**: ``/api/tickets/``

* **METHOD**: ``GET``

* **Header** *(Authorization)* : *Token* ``xxxxxxx-12345-aaaa-bbbb-9876-xxxx``

* **URL Params Filter**: ``status``, ``start_date``, ``end_date``

.. code-block:: json

    	?status=PENDING
	?start_date=2018-12-12
	?end_date=2018-12-12
	?start_date=2018-11-12&end_date=2018-12-12

* **Success Response**:
    * **Code**: ``200 OK``
    * **Content**:

.. code-block:: json

	   {
                "count": 3,
        	"next": null,
        	"previous": null,
        	"results": [
		    {
                	"url": "http://localhost:8000/api/tickets/1/",
                	"user": "admin",
                	"limit": 5,
                	"status": "PENDING",
                	"files": [
                    	    {
                        	"file": "/media/upload/admin/image1.png",
                        	"ticket": 1
                    	    },
                    	    {
	                       	"file": "/media/upload/admin/image2.png",
        	               	"ticket": 1
                	    }
                	]
            	    }
		]
	   }


Create Ticket
=============

* **URL**: ``/api/tickets/``

* **METHOD**: ``POST``

* **Header** *(Authorization)* : *Token* ``xxxxxxx-12345-aaaa-bbbb-9876-xxxx``
    
* **Data Params:**:
    
.. code-block:: json

	{"limit": 5, "status": "PENDING"}


* **Status**:
    * *PENDING*: The user has not yet uploaded any image.
    * *IN PROGRESS*: The user uploaded an image.
    * *COMPLETED*: The user uploaded all the images.    

* **Success Response**:
    * **Code**: ``200 OK``
    * **Content**:

.. code-block:: json

	{
        	"url": "http://localhost:8000/api/tickets/1/",
        	"user": "admin",
        	"limit": 5,
        	"status": "PENDING",
        	"files": []
	}


Upload Files
=============

* **URL**: ``/api/files/``

* **METHOD**: ``POST``

* **Header** *(Authorization)* : *Token* ``xxxxxxx-12345-aaaa-bbbb-9876-xxxx``
    
* **Data Params:**:
    
.. code-block:: json

	{"ticket": 1, "file": "path"}

* **Success Response**:
    * **Code**: ``200 OK``
    * **Content**:

.. code-block:: json

	{
        	"file": "/media/upload/admin/image.png",
    		"ticket": 1
	}
	
Credits
-------

``Tickets`` was created by Rodrigo Chingal (`@chingal
<https://github.com/chingal>`_)
