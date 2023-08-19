# Comparing with other works

An Approach to Identify Source Code Files Impacted by Architectural Technical Debt (ATD) using our method and comparing with existing methods Sas et al. 2022 (https://onlinelibrary.wiley.com/doi/full/10.1002/smr.2398) and Tsoukalas et al. 2023 (https://onlinelibrary.wiley.com/doi/full/10.1002/smr.2564), already Validated by the scientific community. Below is the detailed overview of our research design:

## 1. The Proposed Method

### 1.1 (i) Identification of ATD-Impacted cource code files using change analysis and code metrics:

Our method is divided into five phases:

Phase 1 - Given a git repository, extract historical commit data and modified files in each commit.

Phase 2 - Select the source code files impacted by Architectural Smells and calculate metrics ((AMLOC - Accumulated LOC of each source code file over time), (FOC - frequency of commit occurrence for each source code file), and (CC - cyclomatic complexity of each source code file)).

Phase 3 - Calculate quartiles of the metrics and select the source code files impacted by Architectural Smells (Cyclic Dependency and Hub-like Dependency). In this phase, tools such as Arcan are used to identify Architectural Smells, and DesigniteJava is used to identify Design Smells.

Phase 4 - Analyze critical source code files impacted by Architectural Smells and their dependent source code files with co-change. The dependent source code files are selected using DSM (Dependency Structure Matrix)

Phase 5 - Report potential critical source code files impacted by Architectural Smells.

### 1.2 Testing method on selectect repositories: 

1.2.1 Testing on Apache Cassandra Repository (https://github.com/apache/cassandra):

The outcome of our tests on the Cassandra repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.2 Testing on Apache Kafka Repository (https://github.com/apache/kafka):

The outcome of our tests on the Kafka repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.3 Testing on Apache ActiveMQ Repository (https://github.com/apache/activemq):

The outcome of our tests on the ActiveMQ repository is a set of critical files affected by ATD and the files dependent on these critical files.

1.2.4 Testing on Apache Guava Repository (https://github.com/google/guava):

The outcome of our tests on the Guava repository is a set of critical files affected by ATD and the files dependent on these critical files.

## 2. Comparison of Results from the proposed method and Sas et al. 2022

### 2.1 (iii) Comparison with Sas et al. 2022:

2.1.1 We compared the critical source code files identified by our method with the files impacted by Architectural Smells (Cyclic Dependency and Hub-like Dependency) identified in Sas et al. 2022's work.

2.1.2 In addition to the Cassandra repository, two more repositories analyzed by Sas et al. 2022's work were selected: ActiveMQ and Guava. These selected projects were chosen because they have a large number of .java files (>1500 files), a substantial LOC count for .java files (>300000 lines of code), project lifespan exceeding 10 years, a high number of project commits (>5000 commits), numerous releases (>80 releases), and significant community involvement (>2000 stars and >1000 forks of the  and coloborators > 120).

The objective of comparing the results obtained using our method with the methods of Sas et al. 2022 and Tsoukalas et al. 2023 is to demonstrate that our method produces results that are close to or consistent with those already validated by the scientific community.

Obs: 
- Explain the comparison process between the critical source code files identified by your method and those impacted by Architectural Smells in Sas et al. 2022's work.
- Detail the additional repositories (ActiveMQ and Guava) and their selection criteria.

### 2.2 Specific Comparisons (TODO):

2.2.1 Provide a detailed explanation of the comparison process for each of the repositories: ActiveMQ and Guava.

2.2.2 Describe the process of executing your method on these repositories and comparing the results with Sas et al.'s method (SASM).

## 3. Testing and Comparison with Tsoukalas et al. 2023 on the Kafka Repository (TODO):

3.1 Describe how you applied your method to conduct tests on the Kafka repository.

3.2 Explain how the results were used to compare with Tsoukalas et al. 2023's work on technical debt prioritization.

3.2. Highlight the focus on classes with the highest prioritization of technical debt payments.
