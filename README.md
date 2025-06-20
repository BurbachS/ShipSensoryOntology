# MontoFlow – Maritime Ontology Framework for Modeling Ship Sensory Systems
MontoFlow is a modular framework that facilitates the seamless integration of structured data with OWL ontologies, addressing both static population of knowledge bases and dynamic access to live data. It comprises two complementary submodules: MontoFlow–Static, which supports high-precision instantiation of individuals from tabular sources, and MontoFlow–Dynamic, which enables real-time semantic querying of streaming telemetry.

## SHIP – a Ship Sensory Ontology
The SHIP Ontology provides a semantic model for representing onboard sensory systems, their components, and observations. It extends the W3C SSN/SOSA ontology with maritime-specific concepts, such as engine components, sensor properties, aggregated and anomaly observations, and domain-specific value ranges. The ontology is designed to support condition monitoring, predictive maintenance, and real-time diagnostics in maritime environments.
In addition to the ontology, we provide a complementary software framework that automatically instantiates individuals based on real-time ship sensor data. This framework connects to operational databases, interprets raw data streams, and dynamically generates RDF instances for live observations and anomalies.

## Ontology Website
Further documentation is available on the ontology's website:
https://burbachs.github.io/ShipSensoryOntology/documentation/index-en.html

## MontoFlow Usage Guide
**MontoFlow-Static & SHIP Ontology**
To use MontoFlow-Static with the SHIP Ontology, please make sure that the relevant instances (sensors, devices, engine components, etc.) are correctly added to the Property_Matrix/OWL_Property_Matrix.xlsx Excel file. Each sheet corresponds to a class from the SHIP ontology. The first column (Individual) refers to the instance names, the second column (rdf:type) denotes the type (i.e., the parent class), while the remaining columns describe associated object/data properties.

Important Notes:
* OWL_Property_Matrix.xlsx is a template with example data provided for reference only. Users should replace it with their own data.
* Instances used in object property columns should be correctly defined in the corresponding class sheets.
* Data property literal values should include a datatype (e.g., qudt:upperBound "20"^^xsd:float).
* The order of property fields is irrelevant, and new property columns can be added as needed.

Once the OWL_Property_Matrix.xlsx file is correctly completed, you can start the ontology instantiation process by running the following command in your terminal:
<span style="font-family:Courier New; font-size:4em;">python3 MontoFlow_static.py</span>
As a result, a new instantiated TTL file will be created in the root folder:
<span style="font-family:Courier New; font-size:4em;">SHIP_individuals.ttl</span>
For further customization, please refer to the CONFIGURATION section within MontoFlow_static.py.

**MontoFlow-Static & Custom Ontology**
To use MontoFlow-Static with other domains or custom ontologies, the user must create their own Property_Matrix by renaming the sheet tabs to match the relevant ontology classes and adding the corresponding data/object properties as columns.
Column headers should include the property names with prefixes, as defined in the input TTL ontology (e.g., ssn:isProxyFor).
The rest of the process remains the same. To generate the ontology:
<span style="font-family:Courier New; font-size:4em;">python3 MontoFlow_static.py</span>
Important Notes:
* The input ontology should be in TTL format.
* All prefixes and imports must be correctly defined.

## How to use the MontoFlow-Dynamic for real-time data querying
ontop.bat query -p ontop.properties -m mapping.ttl -q CQs/C01_1g.rq

## How to cite
Please cite MontoFlowand the SHIP Ontology as:

Pavle Ivanovic, Simon Burbach, Maria Maleshkova. "MontoFlow/SHIP." Zenodo. https://doi.org/10.5281/zenodo.15390282

## Licence
All resources are licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
