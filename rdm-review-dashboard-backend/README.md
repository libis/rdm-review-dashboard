# Review Dashboard Backend API 

This API provides backend functionality for the Review Dashboard application for Dataverse. It is tested with Python 3.8. 

For a list of possible API calls, see localhost:8000/docs. 

For read operations, this api needs access to the PostgreSQL database of Dataverse and the Solr index. 
For reviewer assignment and changes in dataset status, it uses Dataverse Native API. An API key needs to be configured.

For more detailed configuration information, see docs/configuration.md