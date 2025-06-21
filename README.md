# MontoFlow – Maritime Ontology Framework for Modeling Ship Sensory Systems
MontoFlow is a modular framework that facilitates the seamless integration of structured data with OWL ontologies, addressing both static population of knowledge bases and dynamic access to live data. It comprises two complementary submodules: MontoFlow–Static, which supports high-precision instantiation of individuals from tabular sources, and MontoFlow–Dynamic, which enables real-time semantic querying of streaming telemetry.

## SHIP – a Ship Sensory Ontology
The SHIP Ontology provides a semantic model for representing onboard sensory systems, their components, and observations. It extends the W3C SSN/SOSA ontology with maritime-specific concepts, such as engine components, sensor properties, aggregated and anomaly observations, and domain-specific value ranges. The ontology is designed to support condition monitoring, predictive maintenance, and real-time diagnostics in maritime environments.
In addition to the ontology, we provide a complementary software framework that automatically instantiates individuals based on real-time ship sensor data. This framework connects to operational databases, interprets raw data streams, and dynamically generates RDF instances for live observations and anomalies.

## Ontology Website
Further documentation is available on the ontology's website:
https://burbachs.github.io/ShipSensoryOntology/documentation/index-en.html

## MontoFlow Usage Guide
### MontoFlow-Static & SHIP Ontology

To use MontoFlow-Static with the SHIP Ontology, please make sure that the relevant instances (sensors, devices, engine components, etc.) are correctly added to the Property_Matrix/OWL_Property_Matrix.xlsx Excel file. Each sheet corresponds to a class from the SHIP ontology. The first column (Individual) refers to the instance names, the second column (rdf:type) denotes the type (i.e., the parent class), while the remaining columns describe associated object/data properties.

Important Notes:
* OWL_Property_Matrix.xlsx is a template with example data provided for reference only. Users should replace it with their own data.
* Instances used in object property columns should be correctly defined in the corresponding class sheets.
* Data property literal values should include a datatype (e.g., qudt:upperBound "20"^^xsd:float).
* The order of property fields is irrelevant, and new property columns can be added as needed.

Once the OWL_Property_Matrix.xlsx file is correctly completed, the ontology instantiation process can be started by running the following command in a terminal:

`python3 MontoFlow_static.py`

As a result, an instantiated ontology (TTL) file will be created in the root folder:

`SHIP_individuals.ttl`

For further customization, please refer to the CONFIGURATION section within `MontoFlow_static.py`.

### MontoFlow-Static & Custom Ontology

To use MontoFlow-Static with other domains or custom ontologies, the user must create their own Property_Matrix by renaming the sheet tabs to match the relevant ontology classes and adding the corresponding data/object properties as columns.

Column headers should include the property names with prefixes, as defined in the input TTL ontology (e.g., ssn:isProxyFor).

The rest of the process remains the same. To generate the instantiated ontology:

`python3 MontoFlow_static.py`

Important Notes:
* The input ontology should be in TTL format, declared in MontoFlow_static.py configuration section
* All prefixes and imports must be correctly defined.


### MontoFlow-Dynamic & SHIP Ontology

To use MontoFlow-Dynamic with the SHIP Ontology, please make sure that Ontop_Property_Matrix.xlsx is correctly populated, based on the general guidelines in the 'MontoFlow-Static & SHIP Ontology' section, with two exceptions:
* The Subclass sheet should be left as it is, as it is required for Class-Subclass mapping.
* Data property literal values should be entered without datatype (defined in R2RML mapping). For instance, the previous example transforms into qudt:upperBound 20.

Once Ontop_Property_Matrix.xlsx is completed, MontoFlow-Dynamic can be initialized with the following terminal command:

`python3 MontoFlow_dynamic.py`

The execution outputs each Property_Matrix sheet into a separate CSV file (located at data/Ship01/owl/) and the corresponding DuckDB database file (DuckDB/ontop.duckdb). The Ontop mapping (mapping.ttl) and ontop.properties files are preconfigured to match the DuckDB view setup.

Important Notes:

* For real-time (raw data) logs, the default data structure is: /yyyy/mm/dd/*.csv, where each CSV log file contains the sensor name (e.g., FuelTank01Sensor.csv).
* The tool automatically creates a datetime "timestamp" column based on the file path, by extracting the date and merging it with the "time" column. Alternatively, a datetime column can be used directly, if already present in the log file.
* MontoFlow-Dynamic assumes that the Ontop CLI and the DuckDB Python module are already installed. Please refer to their official documentation pages for more details.

For further customization, please refer to MontoFlow_dynamic.py

To run the SPARQL queries on real-time data, use the following command:

`ontop.bat query -p ontop.properties -m mapping.ttl -q user_query.rq`

or try one of the CQ examples:

`ontop.bat query -p ontop.properties -m mapping.ttl -q CQs/C01_1g.rq`

### MontoFlow-Dynamic & Custom Ontology
To use MontoFlow-Dynamic with other domains or custom ontologies, the user must again create their own Property_Matrix, following the 'MontoFlow-Dynamic & SHIP Ontology' guidelines. 

The next step includes customization of MontoFlow_dynamic.py, mapping.ttl and ontop.properties to match the custom ontology. The key challenge is linking DuckDB views to R2RML mappings, which requires some familiarity with R2RML and view-based data modeling. However, even without prior knowledge, it is possible to deduce the mapping pattern from provided examples. 

Once the customization is completed, MontoFlow-Dynamic can be initialized with the following terminal command:

`python3 MontoFlow_dynamic.py`

To run the SPARQL queries (e.g., `user_query.rq`) on real-time data and custom ontology, use the terminal command:

`ontop.bat query -p ontop.properties -m mapping.ttl -q user_query.rq`

## How to use the MontoFlow-Dynamic for real-time data querying
ontop.bat query -p ontop.properties -m mapping.ttl -q CQs/C01_1g.rq

## How to cite
Please cite MontoFlowand the SHIP Ontology as:

Pavle Ivanovic, Simon Burbach, Maria Maleshkova. "MontoFlow/SHIP." Zenodo. https://doi.org/10.5281/zenodo.15390282

## Licence
All resources are licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
