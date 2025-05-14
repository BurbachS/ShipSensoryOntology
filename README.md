# MontoFlow – Maritime Ontology Framework for Modeling Ship Sensory Systems
MontoFlow is a modular framework that facilitates the seamless integration of structured data with OWL ontologies, addressing both static population of knowledge bases and dynamic access to live data. It comprises two complementary submodules: MontoFlow–Static, which supports high-precision instantiation of individuals from tabular sources, and MontoFlow–Dynamic, which enables real-time semantic querying of streaming telemetry.

## SHIP – a Ship Sensory Ontology
The SHIP Ontology provides a semantic model for representing onboard sensory systems, their components, and observations. It extends the W3C SSN/SOSA ontology with maritime-specific concepts, such as engine components, sensor properties, aggregated and anomaly observations, and domain-specific value ranges. The ontology is designed to support condition monitoring, predictive maintenance, and real-time diagnostics in maritime environments.
In addition to the ontology, we provide a complementary software framework that automatically instantiates individuals based on real-time ship sensor data. This framework connects to operational databases, interprets raw data streams, and dynamically generates RDF instances for live observations and anomalies.

## How to use the MontoFlow-Dynamic for real-time data querying
ontop.bat query -p ontop.properties -m mapping.ttl -q CQs/C01_1g.rq

## How to cite
Please cite MontoFlowand the SHIP Ontology as:

Pavle Ivanovic, Simon Burbach, Maria Maleshkova. "MontoFlow/SHIP." Zenodo. https://doi.org/10.5281/zenodo.15390282

## Licence
All resources are licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
