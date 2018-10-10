import requests
import yaml

from pyxus.client import NexusClient
from pyxus.resources.entity import Domain
from pyxus.resources.entity import Schema
from pyxus.resources.entity import Instance
from openid_http_client.auth_client.access_token_client import AccessTokenClient

# Configure client

auth_client = None
client = NexusClient(scheme="https", 
                     host="bbp-nexus.epfl.ch", 
                     prefix="staging/v0", 
                     alternative_namespace="https://bbp-nexus.epfl.ch",
                     auth_client=auth_client)

# Domain

domain_name = "genomics"
domain_description = "Genomics data from Biocruces"
organization_name = "sandbox"

# Create domain

# your_domain = Domain.create_new(organization_name, domain_name, domain_description) 
# client.domains.create(your_domain)

# Read domain

# your_domain = client.domains.read(organization_name, domain_name)
# print("Your domain identifer is {}".format(your_domain.data["@id"]))

# Schema

example_person_schema = {
    "@context": [
        "https://bbp-nexus.epfl.ch/staging/v0/contexts/nexus/core/schema/v0.2.0"
    ],
    "@type": "nxv:Schema",
    "shapes": {
        "@type": "sh:NodeShape",
        "description": "schema.org person description.",
        "nodeKind": "sh:BlankNodeOrIRI",
        "targetClass": "schema:Person",
        "property": [
        {
            "path": "schema:email",
            "datatype": "xsd:string",
            "name": "Email",
            "pattern": "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"
        },
        {
            "datatype": "xsd:string",
            "description": "Given name. In the U.S., the first name of a Person. This can be used along with familyName instead of the name property.",
            "name": "givenName",
            "path": "schema:givenName",
            "minCount": "1"
        },
        {
            "datatype": "xsd:string",
            "description": "Family name. In the U.S., the last name of an Person. This can be used along with givenName instead of the name property.",
            "name": "familyName",
            "path": "schema:familyName",
            "minCount": "1"
        }
    ]
  }
}

schema_name = "person"  # Provide the name for the example schema here
schema_version = "v0.1.0"  # Provide the version for the example schema here
content = example_person_schema

# schema = Schema.create_new(organization=organization_name, 
#                            domain=domain_name, 
#                            schema=schema_name,
#                            version=schema_version, 
#                            content=content)
# client.schemas.create(schema)

# schema = client.schemas.read(organization=organization_name, 
#                              domain=domain_name, 
#                              schema=schema_name, 
#                              version=schema_version)
# print("The schema identifier is {}".format(schema.data["@id"]))

# client.schemas.publish(entity=schema,publish=True)

example_person_data = {
    "@context": {
        "Person": "http://schema.org/Person",
        "givenName": "http://schema.org/givenName",
        "familyName": "http://schema.org/familyName"
    },
    "@type": [
        "Person"
    ],
    "familyName": "Nexus",
    "givenName": "Brian"
}

instance = Instance.create_new(organization=organization_name, 
                           domain=domain_name, 
                           schema=schema_name,
                           version=schema_version, 
                           content=example_person_data)
client.instances.create(instance)

example_person_data_id = instance.data["@id"]
example_person_data_rev = instance.get_revision()

filepath = "https://docs.google.com/uc?id=1V8-hGYNMVqlCIrvlTKTxseMfZSGEqbHl"  # Provide the address of the file you want to attach here
r = requests.get(filepath)
file =  r.content

url = "{}/attachment?rev={}".format(example_person_data_id, example_person_data_rev)
file_attachment = {'file': file}
response = requests.put(url, files=file_attachment)






