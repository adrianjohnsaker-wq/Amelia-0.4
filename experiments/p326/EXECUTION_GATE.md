# P3.26 execution gate

This branch is an implementation review artifact. It is not a sealed registration.

No experiment workflow is configured to run on push. Before calling any external source or running the substrate assay, the following must be completed in a later reviewed commit:

1. seal the input source and prospective selection rule;
2. freeze field equations, arm seeds, dose, lineage count, and stopping rules;
3. bind the implementation and frozen P3.16/P3.17 dependencies by digest;
4. specify the primary analysis and exploratory atlas summaries;
5. record explicit authorization to execute the exploratory assay.

Until those conditions are met, this branch must not acquire beacon rounds or generate an assay result.
